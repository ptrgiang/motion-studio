"""Exercise the real preview UI; assertions never claim human playback/listening approval."""
import json,os,subprocess,sys,threading
from pathlib import Path
root=Path(sys.argv[1]).resolve();repo=Path(__file__).resolve().parents[1];sys.path.insert(0,str(repo/'skills/motion-studio/scripts'))
from preview import make_server
from review import import_notes,read
server=make_server(root,'ci');thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
script=r'''
import {createRequire} from 'node:module';import {writeFile} from 'node:fs/promises';
const root=process.argv[2],url=process.argv[3];const {chromium}=createRequire(root+'/package.json')('playwright');const browser=await chromium.launch({headless:true});
try{const page=await browser.newPage({viewport:{width:1360,height:1000},acceptDownloads:true});const faults=[];page.on('pageerror',e=>faults.push(e.message));await page.goto(url);await page.waitForFunction(()=>window.motionPreview&&document.querySelector('#status').textContent.startsWith('Ready'));
 await page.evaluate(()=>window.motionPreview.seek(150));await page.waitForFunction(()=>document.querySelector('#time').textContent.startsWith('Frame 150'));
 await page.locator('#next').click();await page.waitForFunction(()=>window.motionPreview.frame===151);await page.locator('#previous').click();await page.waitForFunction(()=>window.motionPreview.frame===150);
 await page.locator('#show-safe').check();if(!await page.locator('#safe').isVisible())throw Error('Safe overlay unavailable');
 await page.locator('#format').selectOption('vertical');await page.waitForFunction(()=>document.querySelector('#scene').contentDocument.querySelector('#stage').style.width==='540px');
 await page.evaluate(()=>window.motionPreview.seek(150));
 const camera=await page.evaluate(async()=>{const w=document.querySelector('#scene').contentWindow;await w.renderFrame(150,JSON.parse(JSON.stringify((await (await fetch('/__motion/config')).json()).spec)),'vertical');const d=w.document;const card=d.querySelector('#card').getBoundingClientRect(),cursor=d.querySelector('#cursor').getBoundingClientRect(),ripple=d.querySelector('#ripple').getBoundingClientRect();if(cursor.x<card.x||cursor.y<card.y||cursor.x>card.right||cursor.y>card.bottom)throw Error('Cursor misses focused UI');return {cursor_x:cursor.x,cursor_y:cursor.y,ripple_center_x:ripple.x+ripple.width/2,ripple_center_y:ripple.y+ripple.height/2};});
 if(Math.abs(camera.cursor_x-camera.ripple_center_x)>.1||Math.abs(camera.cursor_y-camera.ripple_center_y)>.1)throw Error('Click geometry drift');
 const warnings=await page.evaluate(async()=>{const d=document.querySelector('#scene').contentDocument;const module=await import('/src/readability.mjs');const a=d.createElement('div');a.dataset.read='small-fixture';a.textContent='Tiny fixture';a.style.cssText='position:absolute;left:100px;top:300px;font-size:5px';const b=a.cloneNode(true);b.dataset.read='overlap-fixture';d.querySelector('#stage').append(a,b);const r=module.inspectLayout(d,{width:540},150);a.remove();b.remove();const holds=module.readingHolds({fps:30,shots:[{id:'short',start:0,end:3,copy:'This is deliberately too much copy to read'}]});if(!holds[0].warning)throw Error('Short hold was not detected');return r.warnings;});
 if(!warnings.some(w=>w.kind==='small_text'&&w.id==='small-fixture')||!warnings.some(w=>w.kind==='overlap'&&w.ids.includes('small-fixture')))throw Error('Readability diagnostics failed');
 await page.locator('#note').fill('Observed preview fixture note');await page.locator('#add-note').click();if(await page.locator('#notes li').count()!==1)throw Error('Note not recorded');
 await page.locator('#mode').selectOption('export');await page.locator('#film').evaluate(v=>new Promise(resolve=>{if(v.readyState>=1)return resolve();v.addEventListener('loadedmetadata',resolve,{once:true});}));const media=await page.locator('#film').evaluate(v=>({duration:v.duration,width:v.videoWidth,height:v.videoHeight,time:v.currentTime}));if(media.duration!==15||media.width!==540||media.height!==960||Math.abs(media.time-5)>.05)throw Error('Export preview mismatch');
 await page.locator('#play').click();await page.waitForFunction(()=>!document.querySelector('#film').paused);await page.locator('#play').click();await page.waitForFunction(()=>document.querySelector('#film').paused);
 const downloaded=page.waitForEvent('download');await page.locator('#export-notes').click();await (await downloaded).saveAs(root+'/out/ci/preview-test-notes.json');
 const checked=await page.locator('#observed-temporal').isChecked();if(checked)throw Error('Playback observation was inferred');await page.screenshot({path:root+'/out/ci/preview-test.png',fullPage:true});if(faults.length)throw Error(faults.join('\n'));
 await writeFile(root+'/out/ci/preview-browser-test.json',JSON.stringify({frame_step:true,format_switch:true,safe_overlay:true,camera_click_mapping:camera,readability_fixture:true,encoded_media_metadata:media,notes_export:true,perceptual_approval:false},null,2));
}finally{await browser.close();}
'''
file=root/'preview-browser-test.mjs';file.write_text(script)
try:
 subprocess.run(['node',str(file),str(root),f'http://127.0.0.1:{server.server_port}'],check=True,cwd=root,timeout=150)
 result=import_notes(root,'ci',root/'out/ci/preview-test-notes.json');assert result['status']=='review_pending';assert result['open_defects']
finally:server.shutdown();server.server_close();thread.join()
print('Preview UI, camera mapping, readability fixtures and bound pending notes passed')
