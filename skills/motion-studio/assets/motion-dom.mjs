// Original frame-based primitives. No mutable animation state or wall clocks.
export const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
export const progress=(frame,start,end)=>{if(!Number.isFinite(frame)||!(end>start))throw Error('Invalid phase');return clamp((frame-start)/(end-start));};
export const easeOut=t=>1-(1-t)**3;
export const easeInOut=t=>t<.5?4*t*t*t:1-(-2*t+2)**3/2;
export function keyframes(entries,easing=easeInOut){
 if(!Array.isArray(entries)||!entries.length)throw Error('Keyframes required');
 const keys=entries.map(([frame,value],i)=>{if(!Number.isFinite(frame)||(i&&frame<=entries[i-1][0]))throw Error('Ordered finite keyframes required');return [frame,Array.isArray(value)?value.slice():value];});
 const vector=Array.isArray(keys[0][1]);const width=vector?keys[0][1].length:1;
 for(const [,v] of keys)if(vector?(!Array.isArray(v)||!width||v.length!==width||v.some(x=>!Number.isFinite(x))):!Number.isFinite(v))throw Error('Inconsistent keyframe values');
 const copy=v=>vector?v.slice():v;
 return frame=>{if(!Number.isFinite(frame))throw Error('Finite frame required');if(frame<=keys[0][0])return copy(keys[0][1]);
  for(let i=1;i<keys.length;i++)if(frame<keys[i][0]){const [a,x]=keys[i-1],[b,y]=keys[i];const t=easing(progress(frame,a,b));if(!Number.isFinite(t))throw Error('Invalid easing');return vector?x.map((v,j)=>v+(y[j]-v)*t):x+(y-x)*t;}
  return copy(keys.at(-1)[1]);};
}
export function shotAt(frame,shots){const shot=shots.find(s=>frame>=s.start&&frame<s.end);return shot?{...shot,local:frame-shot.start,duration:shot.end-shot.start}:null;}
export function eventFrame(spec,id){const frame=spec.events?.[id];if(!Number.isInteger(frame))throw Error('Missing event: '+id);return frame;}
export function beatClock(fps,bpm,offsetFrame=0){
 if(!Number.isFinite(fps)||fps<=0||!Number.isFinite(bpm)||bpm<=0||!Number.isFinite(offsetFrame))throw Error('Invalid beat clock');const length=fps*60/bpm;
 return {frame:beat=>offsetFrame+beat*length,position:frame=>(frame-offsetFrame)/length,pulse:(frame,decay=6)=>{if(!Number.isFinite(frame)||!Number.isFinite(decay)||decay<=0)throw Error('Invalid beat pulse');if(frame<offsetFrame)return 0;const p=(frame-offsetFrame)/length;const fraction=Math.abs(p-Math.round(p))<1e-9?0:p-Math.floor(p);return Math.exp(-decay*fraction);}};
}
export function put(element,{x=0,y=0,scale=1,rotate=0,opacity=1}={}){
 if([x,y,scale,rotate,opacity].some(v=>!Number.isFinite(v)))throw Error('Finite transform values required');
 element.style.transform=`translate(${x}px,${y}px) rotate(${rotate}deg) scale(${scale})`;element.style.opacity=String(clamp(opacity));element.style.display=opacity<=0?'none':'';
}
export function kinetic(element,text){element.replaceChildren();return [...new Intl.Segmenter(undefined,{granularity:'grapheme'}).segment(text)].map(({segment})=>{const span=document.createElement('span');span.textContent=segment===' '?'\u00a0':segment;span.style.display='inline-block';element.append(span);return span;});}
export function revealLetters(letters,frame,start,{stagger=2,duration=12,travel=30}={}){letters.forEach((el,i)=>{const p=easeOut(progress(frame,start+i*stagger,start+i*stagger+duration));put(el,{y:(1-p)*travel,opacity:p});});}
