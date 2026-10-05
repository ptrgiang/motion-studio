#!/usr/bin/env python3
"""Install/update seven skills with diff, manifest, backup and local-edit protection."""
import argparse,hashlib,json,re,shutil,tempfile
from datetime import datetime,timezone
from pathlib import Path
NAMES=('motion-studio','motion-director','motion-storyboard','motion-design','motion-engineer','motion-audio','motion-review')
MANIFEST='.motion-studio-install.json'
def hashes(root):
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for n in NAMES for p in (root/n).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
def export(source_root,destination,update=False,dry_run=False):
    found={};root=Path(source_root)
    for md in root.glob('*/SKILL.md'):
        txt=md.read_text(encoding='utf-8');fm=re.match(r'^---\s*\n(.*?)\n---',txt,re.S)
        if not fm:continue
        m=re.search(r'^name:\s*[\'\"]?([a-z0-9-]+)[\'\"]?\s*$',fm.group(1),re.M)
        if m and m.group(1) in NAMES:
            if m.group(1) in found:raise ValueError(f'Duplicate skill: {m.group(1)}')
            found[m.group(1)]=md.parent
    missing=set(NAMES)-found.keys()
    if missing:raise ValueError('Missing required skills: '+', '.join(sorted(missing)))
    dst=Path(destination).resolve()
    if any(dst.is_relative_to(s.resolve()) for s in found.values()):raise ValueError('Destination must be outside source skills')
    exists=any((dst/n).exists() or (dst/n).is_symlink() for n in NAMES)
    if any((dst/n).is_symlink() for n in NAMES):raise ValueError('Refusing to replace symlinked skill destinations')
    if exists and not update:raise ValueError('Skills already exist; inspect --dry-run --update')
    old=hashes(dst) if exists else {}
    if exists:
        meta=dst/MANIFEST
        if not meta.is_file():raise ValueError('No installation baseline. Back up old folders and install into a fresh destination; local edits cannot be inferred safely.')
        saved=json.loads(meta.read_text(encoding='utf-8')).get('files')
        if old!=saved:raise ValueError('Installed files differ from baseline; preserve/resolve local edits before update')
    new={}
    for n in NAMES:
        for p in found[n].rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':new[n+'/'+p.relative_to(found[n]).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    diff={'added':sorted(new.keys()-old.keys()),'changed':sorted(k for k in old.keys()&new.keys() if old[k]!=new[k]),'removed':sorted(old.keys()-new.keys())}
    if dry_run:return {'dry_run':True,'diff':diff}
    dst.mkdir(parents=True,exist_ok=True);backup=None;created=[];moved=[]
    if exists:
        backup=dst.parent/('motion-studio-backup-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'));backup.mkdir()
        shutil.copy2(dst/MANIFEST,backup/MANIFEST)
    try:
        with tempfile.TemporaryDirectory(dir=dst,prefix='motion-export-') as td:
            for n in NAMES:shutil.copytree(found[n],Path(td)/n,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.DS_Store'))
            for n in NAMES:
                target=dst/n
                if target.exists():target.rename(backup/n);moved.append(n)
                (Path(td)/n).rename(target);created.append(n)
            temp=Path(td)/MANIFEST;temp.write_text(json.dumps({'version':'1.1.0','files':new},indent=2)+'\n',encoding='utf-8');temp.replace(dst/MANIFEST)
    except Exception:
        for n in created:shutil.rmtree(dst/n)
        for n in moved:(backup/n).rename(dst/n)
        if backup:shutil.copy2(backup/MANIFEST,dst/MANIFEST)
        raise
    return {'installed':len(NAMES),'destination':str(dst),'backup':str(backup) if backup else None,'diff':diff}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--destination',required=True);p.add_argument('--source-root',default=str(Path(__file__).resolve().parents[2]));p.add_argument('--update',action='store_true');p.add_argument('--dry-run',action='store_true');a=p.parse_args()
    try:print(json.dumps(export(a.source_root,a.destination,a.update,a.dry_run),indent=2))
    except (ValueError,OSError) as e:p.exit(1,f'Export failed: {e}\n')
if __name__=='__main__':main()
