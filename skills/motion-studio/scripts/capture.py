#!/usr/bin/env python3
"""Capture local UI states and register source-grounded assets after explicit rights approval."""
import argparse,json,re,subprocess
from pathlib import Path
from studio import local,save
HERE=Path(__file__).resolve().parent

def capture(project,plan='capture-plan.json',run_id='ui',rights=None,provenance=None,approved=False):
    root=Path(project).resolve()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',run_id):raise ValueError('Invalid capture id')
    if not local(root,plan):raise ValueError('Missing or escaping capture plan')
    if not approved or rights not in ('original','licensed','user-provided','public-domain') or not isinstance(provenance,str) or not provenance.strip():raise ValueError('Capture requires approved rights and provenance')
    out=root/'assets'/run_id
    if out.exists():raise ValueError('Capture destination exists; use a new id')
    inventory=json.loads((root/'assets.json').read_text(encoding='utf-8'));asset_id='capture-'+run_id
    if any(a['id']==asset_id for a in inventory['assets']):raise ValueError('Capture asset id exists')
    result=subprocess.run(['node',str(HERE.parent/'assets/capture.mjs'),'--project',str(root),'--plan',plan,'--out',str(out)],cwd=root,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if result.returncode:raise ValueError('Capture failed: '+result.stderr[-2500:])
    metadata=json.loads((out/'capture.json').read_text(encoding='utf-8'))
    # One metadata asset plus each screenshot: hashes survive into pipeline manifests.
    for suffix,file in [('metadata','capture.json')]+[(s['id'],s['file']) for s in metadata['captures']]:
        aid=asset_id+'-'+suffix
        if any(a['id']==aid for a in inventory['assets']):raise ValueError('Capture asset id exists')
        inventory['assets'].append({'id':aid,'path':(out/file).relative_to(root).as_posix(),'role':'capture-metadata' if suffix=='metadata' else 'ui-screenshot','provenance':provenance,'rights':rights,'approved':True,'required':True})
    save(root/'assets.json',inventory);return metadata
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('project');p.add_argument('--plan',default='capture-plan.json');p.add_argument('--run-id',default='ui');p.add_argument('--rights',required=True,choices=['original','licensed','user-provided','public-domain']);p.add_argument('--provenance',required=True);p.add_argument('--approved',action='store_true');a=p.parse_args()
    try:print(json.dumps(capture(a.project,a.plan,a.run_id,a.rights,a.provenance,a.approved),indent=2))
    except (ValueError,OSError) as e:p.exit(1,str(e)+'\n')
