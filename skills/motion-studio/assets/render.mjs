// Resolve Playwright from the production project, not the installed skill directory.
import {createRequire} from 'node:module';
import {readFile,mkdir,writeFile,access} from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const args=process.argv.slice(2),opts={};
for(let i=0;i<args.length;i+=2){if(!args[i]?.startsWith('--')||args[i+1]===undefined)throw Error('Use --spec --html --format --out [--frames]');opts[args[i].slice(2)]=args[i+1];}
for(const key of ['spec','html','format','out'])if(!opts[key])throw Error(`Missing --${key}`);
const spec=JSON.parse(await readFile(opts.spec,'utf8')),fmt=spec.formats.find(x=>x.id===opts.format);
if(!fmt)throw Error('Unknown format');
const require=createRequire(path.join(process.cwd(),'package.json'));
const {chromium}=require('playwright');
const frames=opts.frames?opts.frames.split(',').map(Number):Array.from({length:spec.duration_frames},(_,i)=>i);
if(!frames.length||frames.some(f=>!Number.isInteger(f)||f<0||f>=spec.duration_frames))throw Error('Invalid frame list');
const out=path.resolve(opts.out);await mkdir(out,{recursive:true});
for(const f of new Set(frames)){try{await access(path.join(out,`frame-${String(f).padStart(6,'0')}.png`));throw Error('Output frame exists; use a new version directory');}catch(e){if(e.code!=='ENOENT')throw e;}}
const browser=await chromium.launch({headless:true});
try{
 const page=await browser.newPage({viewport:{width:fmt.width,height:fmt.height},deviceScaleFactor:1});
 await page.goto(pathToFileURL(path.resolve(opts.html)).href);
 await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(im=>im.decode()));});
 const hashes={},checks=[];
 const draw=async frame=>page.evaluate(async({frame,spec,format})=>{await window.renderFrame(frame,spec,format);if(!window.frameHash)throw Error('Renderer must expose decoded pixel frameHash');return window.frameHash();},{frame,spec,format:fmt.id});
 for(const frame of frames){
  const hash=await draw(frame);const file=path.join(out,`frame-${String(frame).padStart(6,'0')}.png`);
  await page.locator('canvas').screenshot({path:file});hashes[frame]=hash;
 }
 // Reverse order checks catch hidden previous-state dependencies.
 for(const frame of [...new Set(frames)].reverse())checks.push({frame,same:(await draw(frame))===hashes[frame]});
 if(checks.some(c=>!c.same))throw Error('Seek order changed decoded pixels');
 // Compare sequential traversal with direct rendering for a short early representative frame.
 const target=Math.min(spec.duration_frames-1,Math.round(spec.fps));const direct=await draw(target);
 for(let f=0;f<=target;f++)await draw(f);
 const sequential=await page.evaluate(()=>window.frameHash());
 if(direct!==sequential)throw Error('Sequential/direct seek mismatch');
 await writeFile(path.join(out,'render-check.json'),JSON.stringify({format:fmt.id,frameCount:frames.length,checks,sequentialCheck:{frame:target,same:true},runtime:{node:process.version,browser:browser.version(),playwright:require('playwright/package.json').version},note:'Within-runtime pixel hash test; does not certify aesthetics/audio.'},null,2));
 console.log(`Rendered ${frames.length} frames with seek checks: ${out}`);
}finally{await browser.close();}
