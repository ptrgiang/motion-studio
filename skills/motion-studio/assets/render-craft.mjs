// Canvas production adapter with cut-safe temporal exposure and atomic frame writes.
import {mkdir,readFile,writeFile,rename,access} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {runtime,serve,argumentsOf,ready,offline} from './browser-runtime.mjs';
import {shutterFrames} from './motion-craft.mjs';
const o=argumentsOf(process.argv.slice(2));for(const k of ['spec','html','format','out'])if(!o[k])throw Error('Missing --'+k);
const project=path.dirname(path.resolve(o.spec)),spec=JSON.parse(await readFile(o.spec,'utf8')),fmt=spec.formats.find(f=>f.id===o.format);if(!fmt)throw Error('Unknown format');
const html=path.resolve(o.html);if(!html.startsWith(project+path.sep))throw Error('HTML outside project');
const out=path.resolve(o.out);await mkdir(out,{recursive:true});const frames=o.frames?o.frames.split(',').map(Number):Array.from({length:spec.duration_frames},(_,i)=>i);
if(!frames.length||frames.some(f=>!Number.isInteger(f)||f<0||f>=spec.duration_frames)||new Set(frames).size!==frames.length)throw Error('Invalid frame list');
const exposure={samples:spec.render?.samples??1,shutter:spec.render?.shutter??.5,cuts:spec.render?.cuts??[],duration:spec.duration_frames};shutterFrames(0,exposure);
for(const f of frames){try{await access(path.join(out,`frame-${String(f).padStart(6,'0')}.png`));throw Error('Output exists; use a fresh run');}catch(e){if(e.code!=='ENOENT')throw e;}}
const server=await serve(project);let browser;const hash=b=>createHash('sha256').update(b).digest('hex');
try{
 browser=await runtime(project).chromium.launch({headless:true,args:['--disable-lcd-text'],...(process.env.MOTION_CHROMIUM_PATH?{executablePath:process.env.MOTION_CHROMIUM_PATH}:{})});
 const context=await browser.newContext({viewport:{width:fmt.width,height:fmt.height},deviceScaleFactor:1});await offline(context,server.origin);const page=await context.newPage(),faults=[];page.on('pageerror',e=>faults.push(e.message));page.on('requestfailed',r=>faults.push(r.url()));
 await page.goto(server.origin+'/'+path.relative(project,html).split(path.sep).join('/'));await page.evaluate(async()=>{if(window.motionReady)await window.motionReady;});await ready(page,spec.fonts?.map(f=>f.css)||[]);
 const draw=async frame=>{
  const samples=shutterFrames(frame,exposure);const encoded=await page.evaluate(async({samples,spec,fmt})=>{
   const c=document.querySelector('canvas');if(!c)throw Error('Canvas missing');const acc=document.createElement('canvas');acc.width=fmt.width;acc.height=fmt.height;const a=acc.getContext('2d');
   for(let i=0;i<samples.length;i++){await window.renderFrame(samples[i],spec,fmt.id);if(c.width!==fmt.width||c.height!==fmt.height)throw Error('Canvas size mismatch');a.globalAlpha=1/(i+1);a.drawImage(c,0,0);}
   return acc.toDataURL('image/png').split(',')[1];
  },{samples,spec,fmt});if(faults.length)throw Error(faults.join('\n'));return Buffer.from(encoded,'base64');
 };
 const hashes={};for(const f of frames){const pixels=await draw(f),file=path.join(out,`frame-${String(f).padStart(6,'0')}.png`);hashes[f]=hash(pixels);await writeFile(file+'.partial',pixels);await rename(file+'.partial',file);if(hash(await readFile(file))!==hashes[f])throw Error('Frame write did not persist');if(f%120===0)console.log('frame',f);}
 const samples=[...new Set([frames[0],frames.at(-1),...spec.shots.flatMap(s=>[s.start,Math.min(s.end-1,s.start+18)]),...Object.values(spec.events||{})])].filter(f=>frames.includes(f));
 const checks=[];for(const f of samples.reverse()){await draw((f+31)%spec.duration_frames);const same=hash(await draw(f))===hashes[f];checks.push({frame:f,same});}if(checks.some(c=>!c.same))throw Error('Temporal render depends on seek order');
 const target=Math.min(spec.fps,spec.duration_frames-1),direct=hash(await draw(target));for(let f=0;f<=target;f++)await draw(f);if(hash(await draw(target))!==direct)throw Error('Sequential/direct mismatch');
 await writeFile(path.join(out,'render-check.json'),JSON.stringify({engine:'canvas-craft',frameCount:frames.length,checks,sequentialCheck:{frame:target,same:true},exposure,blend:'sRGB Canvas source-over equal-weight temporal samples; not linear-light',algorithm:'sha256-lossless-png',runtime:{node:process.version,browser:browser.version()},note:'Determinism and write integrity only; perceptual review required'},null,2));
}finally{if(browser)await browser.close();await server.close();}
