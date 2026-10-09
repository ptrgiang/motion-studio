"""A stateful composition must fail seek validation and retain frame diagnostics."""
import json,subprocess,sys,tempfile,shutil,os
from pathlib import Path
project=Path(sys.argv[1]).resolve();assets=Path(__file__).resolve().parents[1]/'skills/motion-studio/assets'
with tempfile.TemporaryDirectory() as td:
 root=Path(td);(root/'src').mkdir();shutil.copy2(project/'spec.json',root/'spec.json');shutil.copy2(project/'package.json',root/'package.json');os.symlink(project/'node_modules',root/'node_modules',target_is_directory=True)
 for name in ['render-craft.mjs','motion-craft.mjs','browser-runtime.mjs']:shutil.copy2(assets/name,root/'src'/name)
 (root/'src/canvas-starter.html').write_text('''<canvas></canvas><script>let counter=0;window.motionReady=Promise.resolve();window.renderFrame=(f,s,id)=>{let c=document.querySelector('canvas'),v=s.formats.find(x=>x.id===id);c.width=v.width;c.height=v.height;let x=c.getContext('2d');x.fillStyle='rgb('+((++counter*17)%255)+',30,90)';x.fillRect(0,0,c.width,c.height);};</script>''')
 fmt=json.loads((root/'spec.json').read_text())['formats'][0]['id'];out=root/'frames'
 p=subprocess.run(['node',str(root/'src/render-craft.mjs'),'--spec',str(root/'spec.json'),'--html',str(root/'src/canvas-starter.html'),'--format',fmt,'--out',str(out),'--frames','0,30,60'],cwd=root,capture_output=True,text=True)
 if p.returncode==0:raise AssertionError('Stateful renderer was incorrectly accepted')
 diagnostic=json.loads((out/'seek-diagnostic.json').read_text())
 if not any(not x['same'] and x['expected']!=x['actual'] for x in diagnostic):raise AssertionError('Missing failing-frame hashes')
 print('Stateful composition rejected with retained frame diagnostics')
