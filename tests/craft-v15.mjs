import assert from 'node:assert/strict';
import {springTrack,spring,pose,project,contour,morph,shutterFrames} from '../skills/motion-studio/assets/motion-craft.mjs';
const keys=[[1,100],[1.4,20],[2,80]],v=t=>springTrack(t,0,keys);for(const at of [1,1.4,2]){assert.ok(Math.abs(v(at+1e-7)-v(at-1e-7))<.001);const e=1e-5;assert.ok(Math.abs((v(at)-v(at-e))/e-(v(at+e)-v(at))/e)<.1);}
assert.ok(Math.abs(spring(20)-1)<1e-6);assert.equal(spring(-1),0);assert.ok(Math.abs(spring(20,12,1.5)-1)<1e-6);
assert.equal(pose(.5,[{t:0,zoom:1},{t:1,zoom:4}]).zoom,2);
const camera=pose(0,[{t:0}]),opts={width:1000,height:500};assert.equal(project([0,0,0],camera,opts).x,500);assert.ok(project([100,0,500],camera,opts).scale<project([100,0,0],camera,opts).scale);assert.equal(project([0,0,-1000],camera,opts),null);
const a=contour('circle',100,100),b=contour('rounded',400,200);assert.deepEqual(morph(a,b,0),a);assert.deepEqual(morph(a,b,1),b);assert.throws(()=>morph(a,b.slice(1),.5));
assert.deepEqual(shutterFrames(30,{samples:4,shutter:.5,cuts:[30],duration:60}),[30,30,30,30]);assert.ok(shutterFrames(31,{samples:4,shutter:.5,cuts:[30],duration:60}).every(x=>x>=30&&x<=31));assert.throws(()=>shutterFrames(1,{samples:0,duration:5}));
console.log('Craft continuity, camera, topology and exposure tests passed');
