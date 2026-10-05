#!/usr/bin/env python3
"""Check render dependencies without downloading or modifying the environment."""
import argparse,json,shutil,subprocess,sys
from pathlib import Path
import PIL

def check(project,engine):
    results={'python':{'pass':sys.version_info>=(3,10),'version':sys.version.split()[0]},'pillow':{'pass':True,'version':PIL.__version__}}
    for name in ('ffmpeg','ffprobe'):results[name]={'pass':bool(shutil.which(name)),'path':shutil.which(name)}
    if engine=='canvas':
        if not shutil.which('node'):results['canvas']={'pass':False,'error':'Node.js missing'}
        else:
            script="const fs=require('fs');const p=require('playwright');const file=process.env.MOTION_CHROMIUM_PATH||p.chromium.executablePath();console.log(JSON.stringify({pass:fs.existsSync(file),browser:file,version:require('playwright/package.json').version}));"
            p=subprocess.run(['node','-e',script],cwd=project,capture_output=True,text=True,encoding='utf-8',errors='replace')
            results['canvas']=json.loads(p.stdout) if p.returncode==0 else {'pass':False,'error':p.stderr[-1000:]}
    return {'engine':engine,'pass':all(v['pass'] for v in results.values()),'checks':results,'note':'Availability check only; not an end-to-end render or perceptual review.'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',default='.');p.add_argument('--engine',choices=['pillow','canvas'],default='pillow');a=p.parse_args()
    report=check(Path(a.project).resolve(),a.engine);print(json.dumps(report,indent=2));return 0 if report['pass'] else 1
if __name__=='__main__':raise SystemExit(main())
