#!/usr/bin/env python3
"""Bind observations to exact inputs and exported bytes. Assertions are not automatic perception."""
import argparse,hashlib,json,re
from pathlib import Path

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,value):Path(path).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def confined(root,relative):
    if not isinstance(relative,str) or not relative or Path(relative).is_absolute():raise ValueError('Expected relative path')
    p=(root/relative).resolve()
    if not p.is_relative_to(root):raise ValueError('Path escapes project')
    return p

def snapshot(project):
    root=Path(project).resolve();paths=['spec.json','assets.json']
    paths += [p.relative_to(root).as_posix() for p in (root/'src').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    paths += [a['path'] for a in read(root/'assets.json')['assets']]
    paths += [n for n in ('capture-plan.json','package.json','package-lock.json','requirements.txt') if (root/n).exists()]
    hashes={name:(digest(confined(root,name)) if confined(root,name).is_file() else None) for name in sorted(set(paths))}
    fingerprint=hashlib.sha256(json.dumps(hashes,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'fingerprint':fingerprint,'hashes':hashes}

def run_path(project,run_id):
    root=Path(project).resolve()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,63}',run_id):raise ValueError('Unsafe run id')
    return confined(root,'out/'+run_id)

def identity(project,run_id,current=True):
    root=Path(project).resolve();out=run_path(root,run_id);m=read(out/'manifest.json')
    if not m.get('input_snapshot'):raise ValueError('Run has no v1.4 input snapshot; render a fresh run')
    if current and snapshot(root)!=m['input_snapshot']:raise ValueError('Stale render: source, spec or asset changed; render and review again')
    films={}
    if not m.get('exports'):raise ValueError('No exports')
    for e in m['exports']:
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',e['format']) or e['format'] in films or e['film']!=e['format']+'/film.mp4':raise ValueError('Invalid export path/format')
        f=confined(out,e['film'])
        if digest(f)!=e['sha256']:raise ValueError('Export bytes changed')
        if not e.get('technical_pass'):raise ValueError('Technical QC did not pass')
        qc=read(out/e['format']/'qc.json')
        if not qc.get('technical_pass') or not qc.get('full_decode_pass') or qc.get('film_sha256')!=e['sha256']:raise ValueError('QC does not match export')
        films[e['format']]=e['sha256']
    return {'input_fingerprint':m['input_snapshot']['fingerprint'],'manifest_sha256':digest(out/'manifest.json'),'film_hashes':films}

def init(project,run_id):
    out=run_path(project,run_id);bound=identity(project,run_id);p=out/'review-v1.4.json'
    if p.exists():raise ValueError('Review exists; import notes or use another run')
    spec=read(Path(project)/'spec.json')
    doc={'version':'1.4.0','binding':bound,'observations':{f:{'visual':False,'temporal':False,'audio':spec['audio_mode']=='silent','note':'Intentional silence; visual/temporal inspection pending.' if spec['audio_mode']=='silent' else ''} for f in bound['film_hashes']},'defects':[]}
    write(p,doc);return doc

def validate_notes(doc,spec,bound):
    if doc.get('version')!='1.4.0' or doc.get('binding')!=bound:raise ValueError('Notes belong to a different input/export version')
    if set(doc.get('observations',{}))!=set(bound['film_hashes']):raise ValueError('Observe every requested format')
    for f,o in doc['observations'].items():
        if any(type(o.get(k)) is not bool for k in ('visual','temporal','audio')):raise ValueError('Observation flags must be explicit booleans')
        if not isinstance(o.get('note'),str) or len(o['note'])>10000:raise ValueError('Invalid observation note')
        if any(o[k] for k in ('visual','temporal','audio')) and not o['note'].strip():raise ValueError('Describe what was actually observed')
    ids=set()
    if not isinstance(doc.get('defects'),list):raise ValueError('Defects must be a list')
    for d in doc['defects']:
        if not isinstance(d.get('id'),str) or not d['id'] or d['id'] in ids:raise ValueError('Unique defect IDs required')
        ids.add(d['id'])
        if d.get('format') not in bound['film_hashes'] or type(d.get('frame')) is not int or not 0<=d['frame']<spec['duration_frames']:raise ValueError('Invalid defect format/frame')
        if d.get('status') not in ('open','resolved') or not isinstance(d.get('note'),str) or not d['note'].strip():raise ValueError('Describe defect and status')
        if d['status']=='resolved' and not d.get('resolution'):raise ValueError('Resolved defect needs observed resolution')

def import_notes(project,run_id,notes):
    out=run_path(project,run_id);doc=read(notes);bound=identity(project,run_id);validate_notes(doc,read(Path(project)/'spec.json'),bound)
    p=out/'review-v1.4.json'
    if p.exists():
        n=1
        while (out/f'review-backup-{n}.json').exists():n+=1
        write(out/f'review-backup-{n}.json',read(p))
    write(p,doc);return assess(project,run_id)

def assess(project,run_id):
    out=run_path(project,run_id);bound=identity(project,run_id);doc=read(out/'review-v1.4.json');validate_notes(doc,read(Path(project)/'spec.json'),bound)
    pending=[f'{f}:{k}' for f,o in doc['observations'].items() for k in ('visual','temporal','audio') if not o[k]]
    defects=[d['id'] for d in doc['defects'] if d['status']=='open']
    report={'binding':bound,'status':'review_complete' if not pending and not defects else 'review_pending','pending':pending,'open_defects':defects,'note':'Human/agent observation assertions; no automatic aesthetic approval. Pipeline manifest remains a draft.'}
    write(out/'review-assessment.json',report);return report

def compare(project,before,after):
    a=identity(project,before,False);b=identity(project,after);old=read(run_path(project,before)/'manifest.json')['input_snapshot']['hashes'];new=read(run_path(project,after)/'manifest.json')['input_snapshot']['hashes']
    report={'before':a,'after':b,'changed_inputs':[k for k in sorted(set(old)|set(new)) if old.get(k)!=new.get(k)],'note':'Export/input comparison only. Before observations are not inherited; inspect both films to verify a repair.'}
    write(run_path(project,after)/'before-after.json',report);return report

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['init','import','assess','compare']);p.add_argument('project');p.add_argument('--run-id',required=True);p.add_argument('--notes');p.add_argument('--before');a=p.parse_args()
    try:
        if a.command=='init':r=init(a.project,a.run_id)
        elif a.command=='import':
            if not a.notes:raise ValueError('--notes required')
            r=import_notes(a.project,a.run_id,a.notes)
        elif a.command=='compare':
            if not a.before:raise ValueError('--before required')
            r=compare(a.project,a.before,a.run_id)
        else:r=assess(a.project,a.run_id)
        print(json.dumps(r,indent=2,ensure_ascii=False))
    except (ValueError,OSError,KeyError,TypeError) as e:p.exit(1,str(e)+'\n')
