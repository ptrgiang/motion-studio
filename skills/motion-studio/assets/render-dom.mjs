// Render the whole DOM stage; pixel checks come from screenshot PNGs, not a canvas digest.
import {mkdir,readFile,writeFile,access} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {runtime,serve,argumentsOf,inside,ready,offline} from './browser-runtime.mjs';
const opts=argumentsOf(process.argv.slice(2));for(const k of ['spec','html','format','out'])if(!opts[k])throw Error('Missing --'+k);
const project=path.dirname(path.resolve(opts.spec));const spec=JSON.parse(await readFile(opts.spec,'utf8'));const fmt=spec.formats.find(f=>f.id===opts.format);if(!fmt)throw Error('Unknown format');
const html=path.resolve(opts.html);if(!html.startsWith(project+path.sep))throw Error('HTML outside project');
const out=path.resolve(opts.out);await mkdir(out,{recursive:true});const frames=opts.frames?opts.frames.split(',').map(Number):Array.from({length:spec.duration_frames},(_,i)=>i);
if(!frames.length||frames.some(f=>!Number.isInteger(f)||f<0||f>=spec.duration_frames)||new Set(frames).size!==frames.length)throw Error('Invalid frame list');
for(const f of frames){try{await access(path.join(out,`frame-${String(f).padStart(6,'0')}.png`));throw Error('Output exists; use a fresh run');}catch(e){if(e.code!=='ENOENT')throw e;}}
const server=await serve(project);let browser;
try{
 browser=await runtime(project).chromium.launch({headless:true,...(process.env.MOTION_CHROMIUM_PATH?{executablePath:process.env.MOTION_CHROMIUM_PATH}:{})});
 const context=await browser.newContext({viewport:{width:fmt.width,height:fmt.height},deviceScaleFactor:1});await offline(context,server.origin);const page=await context.newPage();const faults=[];
 page.on('pageerror',e=>faults.push(e.message));page.on('response',r=>{if(r.status()>=400)faults.push('HTTP '+r.status()+' '+r.url());});page.on('requestfailed',r=>faults.push('Request failed: '+r.url()));
 await page.goto(server.origin+'/'+path.relative(project,html).split(path.sep).join('/'));await page.waitForFunction(()=>window.motionReady!==undefined,{timeout:30000});await page.evaluate(async()=>await window.motionReady);await ready(page,spec.fonts?.map(f=>f.css)||[]);
 const stage=page.locator('#stage');const digest=buffer=>createHash('sha256').update(buffer).digest('hex');const results={},layout=[];
 const draw=async frame=>{
  await page.evaluate(async({frame,spec,format})=>{if(typeof window.renderFrame!=='function')throw Error('Missing renderFrame');await window.renderFrame(frame,spec,format);}, {frame,spec,format:fmt.id});
  const bounds=await stage.boundingBox();if(!bounds||Math.round(bounds.width)!==fmt.width||Math.round(bounds.height)!==fmt.height)throw Error('Stage dimensions do not match spec');
  if(faults.length)throw Error(faults.join('\n'));return await stage.screenshot({animations:'disabled',caret:'hide'});
 };
 const samples=new Set([0,spec.duration_frames-1,...spec.shots.flatMap(s=>[s.start,Math.min(s.end-1,s.start+18)]),...Object.values(spec.events||{})]);
 for(const frame of frames){const pixels=await draw(frame);results[frame]=digest(pixels);await writeFile(path.join(out,`frame-${String(frame).padStart(6,'0')}.png`),pixels);
  if(samples.has(frame)){
   const evidence=await page.evaluate(()=>[...document.querySelectorAll('[data-qc]')].filter(e=>e.getClientRects().length&&getComputedStyle(e).opacity!=='0').map(e=>{const b=e.getBoundingClientRect();return {id:e.dataset.qc,x:b.x,y:b.y,width:b.width,height:b.height,text:e.textContent};}));
   const failures=evidence.filter(e=>e.x<fmt.safe.left-1||e.y<fmt.safe.top-1||e.x+e.width>fmt.width-fmt.safe.right+1||e.y+e.height>fmt.height-fmt.safe.bottom+1);layout.push({frame,elements:evidence,failures});
  }
 }
 const checks=[];for(const frame of [...samples].filter(f=>frames.includes(f)).reverse())checks.push({frame,same:digest(await draw(frame))===results[frame]});
 if(checks.some(c=>!c.same))throw Error('DOM seek order changed screenshot pixels');
 const target=Math.min(spec.duration_frames-1,spec.fps);const direct=digest(await draw(target));for(let f=0;f<=target;f++)await draw(f);if(direct!==digest(await draw(target)))throw Error('DOM sequential/direct mismatch');
 await writeFile(path.join(out,'layout-check.json'),JSON.stringify({format:fmt.id,samples:layout,pass:layout.every(s=>!s.failures.length),note:'Tagged element bounds only; not an aesthetic, glyph or contrast certificate.'},null,2));
 if(layout.some(s=>s.failures.length))throw Error('Tagged layout exceeds safe bounds; inspect layout-check.json');
 await writeFile(path.join(out,'render-check.json'),JSON.stringify({engine:'dom',format:fmt.id,algorithm:'sha256-lossless-screenshot-png',frameCount:frames.length,checks,sequentialCheck:{frame:target,same:true},runtime:{node:process.version,browser:browser.version()},note:'Same-runtime screenshot comparison; cross-platform pixel equality is not promised.'},null,2));
}finally{if(browser)await browser.close();await server.close();}
