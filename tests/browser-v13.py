"""Real-browser integration for the original local app and DOM capture contracts."""
import json,subprocess,sys,tempfile
from pathlib import Path
from PIL import Image
root=Path(sys.argv[1]).resolve();repo=Path(__file__).resolve().parents[1]
script='''
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const root=process.argv[2];const {serve,offline,ready}=await import(pathToFileURL(root+'/src/browser-runtime.mjs'));const {chromium}=createRequire(root+'/package.json')('playwright');const server=await serve(root);const browser=await chromium.launch({headless:true});
try {const context=await browser.newContext({viewport:{width:1000,height:700}});await offline(context,server.origin);const page=await context.newPage();await page.goto(server.origin+'/src/promo-product.html');await ready(page);
 await page.locator('#note').fill('Persistent browser test');await page.locator('#save').click();if(await page.locator('#notes li').textContent()!=='Persistent browser test')throw Error('Save did not work');await page.reload();if(await page.locator('#notes li').textContent()!=='Persistent browser test')throw Error('Local persistence failed');await page.locator('#theme').click();if(!await page.locator('body.dark').count())throw Error('Theme did not change');
}finally{await browser.close();await server.close();}
'''
file=root/'browser-test.mjs';file.write_text(script,encoding='utf-8');subprocess.run(['node',str(file),str(root)],check=True,cwd=root)
meta=json.loads((root/'assets/ui/capture.json').read_text());assert {c['id'] for c in meta['captures']}=={'draft','saved','dark'}
for c in meta['captures']:
    with Image.open(root/'assets/ui'/c['file']) as im:assert im.size==(2000,1400)
    for target in c['targets'].values():
        for key,value in target['css'].items():assert abs(target['pixels'][key]-value*2)<.01
command=['node',str(root/'src/render-dom.mjs'),'--spec',str(root/'spec.json'),'--html',str(root/'src/promo.html'),'--format','wide','--frames','449,90,150,0,240']
with tempfile.TemporaryDirectory() as t:
    subprocess.run(command+['--out',str(Path(t)/'selected')],check=True,cwd=root)
    report=json.loads((Path(t)/'selected/render-check.json').read_text());assert all(c['same'] for c in report['checks']);assert report['sequentialCheck']['same']
    html=root/'src/promo.html';original=html.read_text();html.write_text(original+'<img src="https://example.invalid/missing.png">')
    try:
        bad=subprocess.run(command+['--out',str(Path(t)/'offline-failure')],cwd=root,capture_output=True,text=True,timeout=75);assert bad.returncode!=0,'Offline asset request incorrectly passed'
    finally:html.write_text(original)
(root/'browser-test.json').write_text(json.dumps({'functional_save':True,'local_persistence':True,'theme_toggle':True,'capture_dimensions':True,'dpr_geometry':True,'shuffled_dom_seek':True,'offline_missing_asset_failure':True,'note':'Technical integration checks; no playback or listening approval.'},indent=2))
print('Functional app, capture geometry, DOM seeking and offline failure passed')
