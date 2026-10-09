import assert from 'node:assert/strict';import {pathToFileURL} from 'node:url';
const m=await import(pathToFileURL(process.argv[2]));const viewport={width:1000,height:700},box={x:400,y:100,width:400,height:280};
const keys=[[0,[0,0,1000,700]],[30,[50,170,760,430]],[60,[0,0,1000,700]]];const a=m.cameraAt(30,keys,viewport,box);const target={x:90,y:381,width:144,height:52};const point=m.targetPoint(target,a);assert.equal(point.x,a.x+162*a.scale);assert.equal(point.y,a.y+407*a.scale);
for(const frame of [60,0,30,15,59,1])assert.deepEqual(m.cameraAt(frame,keys,viewport,box),m.cameraAt(frame,keys,viewport,box));assert.throws(()=>m.cameraPose(viewport,[0,0,1001,700],box));assert.throws(()=>m.cameraAt(0,[[0,[0,0,100,100]],[0,[0,0,100,100]]],viewport,box));
const image={style:{}};m.applyCamera(image,a,box);assert.equal(image.style.position,'absolute');assert.equal(image.style.transform,'none');console.log('Camera confinement, coordinate mapping and arbitrary-frame evaluation passed');
