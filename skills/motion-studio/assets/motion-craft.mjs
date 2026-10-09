// Original Motion Studio craft primitives. Coordinates: +x right, +y down, +z away.
export const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
export const mix=(a,b,p)=>p===0?a:p===1?b:a+(b-a)*p;
export const smooth=p=>{p=clamp(p);return p*p*p*(p*(p*6-15)+10);};
export const phase=(t,a,b)=>smooth((t-a)/(b-a));
export function spring(t,frequency=12,damping=.8){
 if(t<=0)return 0;if(!(frequency>0&&damping>0))throw Error('Invalid spring');
 const w=frequency;if(damping===1)return 1-(1+w*t)*Math.exp(-w*t);
 if(damping<1){const d=w*Math.sqrt(1-damping*damping);return 1-Math.exp(-damping*w*t)*(Math.cos(d*t)+damping*w/d*Math.sin(d*t));}
 const q=Math.sqrt(damping*damping-1),r1=-w*(damping-q),r2=-w*(damping+q);return 1+(r2*Math.exp(r1*t)-r1*Math.exp(r2*t))/(r1-r2);
}
// Sum step responses: value AND velocity survive target changes. No integration state.
export function springTrack(t,initial,keys,frequency=12,damping=.8){let v=initial,last=initial;for(const [at,target] of keys){v+=(target-last)*spring(t-at,frequency,damping);last=target;}return v;}
export function random(id,seed=1){let x=Math.imul(id+1,0x45d9f3b)^seed;x=Math.imul(x^(x>>>16),0x45d9f3b);return ((x^(x>>>16))>>>0)/4294967296;}
export function pose(t,keys){
 if(!keys.length)throw Error('Empty camera path');const fields=['x','y','z','rx','ry','rz','zoom'];
 let a=keys[0],b=a;for(let i=1;i<keys.length;i++){if(keys[i].t<=a.t)throw Error('Camera keys must increase');b=keys[i];if(t<=b.t)break;a=b;}
 const p=a===b?0:phase(t,a.t,b.t),o={};for(const k of fields){const av=a[k]??(k==='zoom'?1:0),bv=b[k]??(k==='zoom'?1:0);if(k==='zoom'&&(av<=0||bv<=0))throw Error('Zoom must be positive');o[k]=k==='zoom'?Math.exp(mix(Math.log(av),Math.log(bv),p)):mix(av,bv,p);}return o;
}
export function rotate([x,y,z],rx=0,ry=0,rz=0){let q=y*Math.cos(rx)-z*Math.sin(rx);z=y*Math.sin(rx)+z*Math.cos(rx);y=q;q=x*Math.cos(ry)+z*Math.sin(ry);z=-x*Math.sin(ry)+z*Math.cos(ry);x=q;return [x*Math.cos(rz)-y*Math.sin(rz),x*Math.sin(rz)+y*Math.cos(rz),z];}
export function project(point,camera,{width,height,focal=900,near=8}){
 const p=rotate([point[0]-camera.x,point[1]-camera.y,point[2]-camera.z],-camera.rx,-camera.ry,-camera.rz),depth=focal+p[2];
 if(depth<=near)return null;const scale=focal/depth*camera.zoom;return {x:width/2+p[0]*scale,y:height/2+p[1]*scale,scale,depth};
}
// Same angular ordering for both contours; rounded rectangle uses a superellipse.
export function contour(kind,w,h,count=96){if(!Number.isInteger(count)||count<8||w<=0||h<=0)throw Error('Invalid contour');const n=kind==='circle'?2:kind==='rounded'?5:null;if(!n)throw Error('Unknown contour');return Array.from({length:count},(_,i)=>{const a=i/count*Math.PI*2,c=Math.cos(a),s=Math.sin(a);return [Math.sign(c)*Math.abs(c)**(2/n)*w/2,Math.sign(s)*Math.abs(s)**(2/n)*h/2];});}
export function morph(a,b,p){if(a.length!==b.length)throw Error('Contours need equal topology');return a.map((v,i)=>v.map((x,j)=>mix(x,b[i][j],p)));}
export function path(ctx,points,close=true){ctx.beginPath();points.forEach((p,i)=>i?ctx.lineTo(p.x??p[0],p.y??p[1]):ctx.moveTo(p.x??p[0],p.y??p[1]));if(close)ctx.closePath();}
// Affine triangles texture a projected quad, including genuine perspective distortion.
export function textureQuad(ctx,img,quad,alpha=1){
 const source=[[0,0],[img.width,0],[img.width,img.height],[0,img.height]];
 for(const ids of [[0,1,2],[0,2,3]]){const s=ids.map(i=>source[i]),d=ids.map(i=>quad[i]);
  const det=s[0][0]*(s[1][1]-s[2][1])+s[1][0]*(s[2][1]-s[0][1])+s[2][0]*(s[0][1]-s[1][1]);
  const coeff=v=>[(v[0]*(s[1][1]-s[2][1])+v[1]*(s[2][1]-s[0][1])+v[2]*(s[0][1]-s[1][1]))/det,(v[0]*(s[2][0]-s[1][0])+v[1]*(s[0][0]-s[2][0])+v[2]*(s[1][0]-s[0][0]))/det,(v[0]*(s[1][0]*s[2][1]-s[2][0]*s[1][1])+v[1]*(s[2][0]*s[0][1]-s[0][0]*s[2][1])+v[2]*(s[0][0]*s[1][1]-s[1][0]*s[0][1]))/det];
  const x=coeff(d.map(p=>p.x)),y=coeff(d.map(p=>p.y));ctx.save();path(ctx,d);ctx.clip();ctx.globalAlpha=alpha;ctx.setTransform(x[0],y[0],x[1],y[1],x[2],y[2]);ctx.drawImage(img,0,0);ctx.restore();
 }
}
// Exposure is trailing, never mixes across a declared cut or outside the film.
export function shutterFrames(frame,{samples=1,shutter=.5,cuts=[],duration}){
 if(!Number.isInteger(samples)||samples<1||samples>16||shutter<0||shutter>1||frame<0||frame>=duration)throw Error('Invalid exposure');
 const start=Math.max(0,...cuts.filter(c=>c<=frame));return Array.from({length:samples},(_,i)=>Math.max(start,frame-shutter*(samples===1?0:i/(samples-1))));
}
