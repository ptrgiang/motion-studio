#!/usr/bin/env python3
"""Prepare a six-second browser craft study. Study art is not a client film."""
import argparse,json,shutil
from pathlib import Path
from pipeline import demo,ASSETS

def prepare(root):
 root=Path(root).resolve();demo(root)
 for name in ('motion-craft.mjs','render-craft.mjs','browser-runtime.mjs'):shutil.copy2(ASSETS/name,root/'src'/name)
 shutil.copy2(ASSETS/'craft-study.html',root/'src/canvas-starter.html')
 p=root/'spec.json';s=json.loads(p.read_text());s['render']={'adapter':'craft','samples':3,'shutter':.5,'cuts':[]};p.write_text(json.dumps(s,indent=2)+'\n')
 (root/'motion-plan.json').write_text(json.dumps({'motif':'One contour becomes a dimensional plaque','signature':'Angularly matched shape morph during an orbit','rests':[],'cuts_seconds':[],'seams':[{'frame':60,'carrier':'same contour','exit':'circle in depth','entry':'same topology grows into plaque','reason':'The subject changes material, not identity'}]},indent=2)+'\n')
 print('Craft study ready; install pinned project runtime then run pipeline.py --engine canvas')
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('project');a=p.parse_args();prepare(a.project)
