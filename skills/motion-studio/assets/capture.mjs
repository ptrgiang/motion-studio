// Capture explicit UI states in fresh headless contexts. No credential/session discovery.
import {mkdir,readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {runtime,serve,inside,ready,offline,argumentsOf} from './browser-runtime.mjs';
const opts=argumentsOf(process.argv.slice(2));for(const k of ['project','plan','out'])if(!opts[k])throw Error('Missing --'+k);
const project=path.resolve(opts.project);const plan=JSON.parse(await readFile(inside(project,opts.plan),'utf8'));const out=path.resolve(opts.out);
const integer=v=>Number.isInteger(v)&&v>0;const hash=data=>createHash('sha256').update(data).digest('hex');
if(!integer(plan.viewport?.width)||!integer(plan.viewport?.height)||!Number.isFinite(plan.dpr)||plan.dpr<=0||plan.dpr>4||!Array.isArray(plan.states)||!plan.states.length)throw Error('Invalid capture plan dimensions/states');
const seen=new Set();for(const s of plan.states){if(!/^[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}$/.test(s.id)||seen.has(s.id)||!s.targets||typeof s.targets!=='object'||Array.isArray(s.targets))throw Error('Invalid capture state');seen.add(s.id);}
const source=inside(project,plan.source);const sourceHash=hash(await readFile(source));await mkdir(out,{recursive:false});const server=await serve(project);let browser;
try{
 browser=await runtime(project).chromium.launch({headless:true,...(process.env.MOTION_CHROMIUM_PATH?{executablePath:process.env.MOTION_CHROMIUM_PATH}:{})});const captures=[];
 for(const state of plan.states){
  const context=await browser.newContext({viewport:plan.viewport,deviceScaleFactor:plan.dpr});await offline(context,server.origin);const page=await context.newPage();const faults=[];page.on('pageerror',e=>faults.push(e.message));page.on('requestfailed',r=>faults.push('Request failed: '+r.url()));page.on('response',r=>{if(r.status()>=400)faults.push('HTTP '+r.status());});
  await page.goto(server.origin+'/'+path.relative(project,source).split(path.sep).join('/'));if(plan.ready)await page.locator(plan.ready).waitFor();await ready(page,plan.fonts||[]);
  for(const action of state.actions||[]){const target=page.locator(action.selector);if(action.type==='fill')await target.fill(String(action.value));else if(action.type==='click')await target.click();else if(action.type==='select')await target.selectOption(String(action.value));else throw Error('Unsupported capture action: '+action.type);}
  if(state.ready)await page.locator(state.ready).waitFor();await ready(page,plan.fonts||[]);
  const targets={};for(const [id,selector] of Object.entries(state.targets)){const box=await page.locator(selector).boundingBox();if(!box||box.x<0||box.y<0||box.x+box.width>plan.viewport.width+.5||box.y+box.height>plan.viewport.height+.5)throw Error('Missing/offscreen target '+id);targets[id]={selector,css:box,pixels:Object.fromEntries(Object.entries(box).map(([k,v])=>[k,v*plan.dpr]))};}
  if(faults.length)throw Error(faults.join('\n'));const png=await page.screenshot({animations:'disabled',caret:'hide'});const file=state.id+'.png';await writeFile(path.join(out,file),png);captures.push({id:state.id,file,sha256:hash(png),viewport:plan.viewport,dpr:plan.dpr,targets});await context.close();
 }
 await writeFile(path.join(out,'capture.json'),JSON.stringify({version:1,source:plan.source,source_sha256:sourceHash,plan_sha256:hash(await readFile(inside(project,opts.plan))),browser:browser.version(),captures},null,2));
}catch(e){await writeFile(path.join(out,'failed.json'),JSON.stringify({error:String(e)}));throw e;}
finally{if(browser)await browser.close();await server.close();}
