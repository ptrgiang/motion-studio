import {keyframes,easeInOut} from './motion-dom.mjs';
const finite=v=>typeof v==='number'&&Number.isFinite(v);
export function cameraPose(viewport,region,box){
 const [x,y,width,height]=region;
 if([viewport.width,viewport.height,box.width,box.height,width,height].some(v=>!finite(v)||v<=0)||[x,y,box.x,box.y].some(v=>!finite(v)))throw Error('Invalid camera geometry');
 if(x<0||y<0||x+width>viewport.width+.001||y+height>viewport.height+.001)throw Error('Camera region outside capture');
 const scale=Math.min(box.width/width,box.height/height);
 return {scale,x:box.x+(box.width-width*scale)/2-x*scale,y:box.y+(box.height-height*scale)/2-y*scale,imageWidth:viewport.width*scale,imageHeight:viewport.height*scale};
}
export function cameraAt(frame,keys,viewport,box){
 if(!keys?.length)throw Error('Camera keyframes required');for(const [,region] of keys)cameraPose(viewport,region,box);
 return cameraPose(viewport,keyframes(keys,easeInOut)(frame),box);
}
export function targetPoint(target,pose){return {x:pose.x+(target.x+target.width/2)*pose.scale,y:pose.y+(target.y+target.height/2)*pose.scale};}
export function applyCamera(image,pose,box){image.style.position='absolute';image.style.width=pose.imageWidth+'px';image.style.height=pose.imageHeight+'px';image.style.left=pose.x-box.x+'px';image.style.top=pose.y-box.y+'px';image.style.transform='none';}
