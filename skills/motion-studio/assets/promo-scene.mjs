import {cameraAt,targetPoint,applyCamera} from './camera-ui.mjs';
import {put,progress,easeOut,shotAt,eventFrame,keyframes,beatClock} from './motion-dom.mjs';
const el=id=>document.getElementById(id);let capture,images,spec;
window.motionReady=(async()=>{
 spec=await fetch('../spec.json').then(r=>r.json());capture=await fetch('../assets/ui/capture.json').then(r=>{if(!r.ok)throw Error('Run capture.py before rendering');return r.json();});images={};
 for(const c of capture.captures){const image=new Image();image.src='../assets/ui/'+c.file;await image.decode();images[c.id]=image;}
 el('product').src=images.draft.src;await el('product').decode();
 await document.fonts.load('400 50px MotionFont','Small ideas. Worth keeping.');await document.fonts.ready;
})();
window.renderFrame=async(frame,current,format)=>{
 await window.motionReady;spec=current;const f=spec.formats.find(f=>f.id===format);const vertical=f.height>f.width;const safe=f.safe;const left=safe.left,top=safe.top,width=f.width-safe.left-safe.right,height=f.height-safe.top-safe.bottom;
 const shot=shotAt(frame,spec.shots);if(!shot)throw Error('Frame outside shots');const stage=el('stage');stage.style.width=f.width+'px';stage.style.height=f.height+'px';
 const brand=el('brand'),eyebrow=el('eyebrow'),headline=el('headline'),support=el('support'),card=el('card'),footer=el('footer'),cursor=el('cursor'),ripple=el('ripple');
 delete card.dataset.uiControl;delete card.dataset.uiControlPx;
 for(const node of [brand,eyebrow,headline,support,card,footer,cursor,ripple])put(node,{opacity:0});
 const set=(node,x,y,w,size)=>{node.style.left=x+'px';node.style.top=y+'px';if(w!==undefined)node.style.width=w+'px';if(size)node.style.fontSize=size+'px';};
 set(brand,left,top);put(brand);set(footer,left,f.height-safe.bottom-20,width);put(footer);
 const start=shot.start;const enter=easeOut(progress(frame,start+3,start+21));const titleY=vertical?top+85:top+75;
 set(eyebrow,left,titleY-30,width);eyebrow.textContent=['KEEP THE THOUGHT','CAPTURED FROM THE APP','A DIFFERENT VIEW','LOCAL BY DESIGN','MAKE ROOM FOR IDEAS'][spec.shots.findIndex(s=>s.id===shot.id)];put(eyebrow,{opacity:enter});
 headline.style.transformOrigin='left top';const titleWidth=vertical?width/1.008:width*.46;set(headline,left,titleY,titleWidth,vertical?42:46);headline.textContent=shot.copy;put(headline,{y:18*(1-enter),opacity:enter});
 support.textContent=['One small place for a useful idea.','Write a thought. Save it locally.','Switch between light and dark.','Your notes remain in this browser.','Write it. Save it. Keep it.'][spec.shots.findIndex(s=>s.id===shot.id)];
 set(support,left,titleY+(vertical?155:130),titleWidth,vertical?19:20);put(support,{y:10*(1-enter),opacity:enter});
 if(shot.id!=='hook'&&shot.id!=='end'){
  const state=shot.id==='write'?(frame<eventFrame(spec,'saveNote')?'draft':'saved'):shot.id==='theme'?(frame<eventFrame(spec,'darkView')?'saved':'dark'):'saved';
  const picture=images[state];el('product').src=picture.src;await el('product').decode();
  const cardWidth=vertical?width:width*.49;const x=vertical?left:left+width*.51;const y=vertical?top+365:top+80;const cardHeight=cardWidth*.7;set(card,x,y,cardWidth);card.style.height=cardHeight+'px';put(card,{y:14*(1-enter),opacity:enter});
  const stateMeta=capture.captures.find(c=>c.id===state);const box={x,y:y+14*(1-enter),width:cardWidth,height:cardHeight};
  const pose=cameraAt(frame,shot.camera||[[shot.start,[0,0,stateMeta.viewport.width,stateMeta.viewport.height]]],stateMeta.viewport,box);applyCamera(el('product'),pose,box);
  if(shot.id==='write'||shot.id==='theme'){
   const event=eventFrame(spec,shot.id==='write'?'saveNote':'darkView');const targetName=shot.id==='write'?'save':'theme';const target=stateMeta.targets[targetName].css;
   // CSS viewport coordinates scale to the displayed screenshot; DPR does not change CSS geometry.
   const {x:tx,y:ty}=targetPoint(target,pose);card.dataset.uiControl=targetName;card.dataset.uiControlPx=target.height*pose.scale;
   const path=keyframes([[event-22,[tx+45,ty+35]],[event-2,[tx,ty]],[event+6,[tx,ty]]],easeOut);const [cx,cy]=path(frame);
   set(cursor,cx,cy);put(cursor,{scale:frame===event ? .85 : 1,opacity:frame>=event-22&&frame<=event+8?1:0});
   set(ripple,tx-13,ty-13);const click=progress(frame,event,event+12);put(ripple,{scale:1+click,opacity:frame>=event&&frame<event+12?1-click:0});
  }
 }else if(shot.id==='end'){
  const clock=beatClock(spec.fps,spec.rhythm.bpm,spec.rhythm.offset_frame);const accent=1+.008*clock.pulse(frame);put(headline,{scale:accent,opacity:enter});
 }
};
