#!/usr/bin/env python3
"""Export the seven Motion Studio skills without overwriting user skills."""
import argparse, re, shutil, tempfile
from pathlib import Path
NAMES=('motion-studio','motion-director','motion-storyboard','motion-design','motion-engineer','motion-audio','motion-review')
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--destination',required=True);p.add_argument('--source-root',default=str(Path(__file__).resolve().parents[2]));a=p.parse_args()
    found={};root=Path(a.source_root)
    for md in root.glob('*/SKILL.md'):
        txt=md.read_text(encoding='utf-8');fm=re.match(r'^---\s*\n(.*?)\n---',txt,re.S)
        if not fm:continue
        m=re.search(r'^name:\s*[\'\"]?([a-z0-9-]+)[\'\"]?\s*$',fm.group(1),re.M)
        if m and m.group(1) in NAMES:
            if m.group(1) in found:p.error(f'Duplicate skill name: {m.group(1)}')
            found[m.group(1)]=md.parent
    missing=set(NAMES)-found.keys()
    if missing:p.error('Missing required skills: '+', '.join(sorted(missing)))
    dst=Path(a.destination).resolve()
    if any((dst/n).exists() for n in NAMES):p.error('Destination already contains a member; refusing overwrite')
    if any(dst.is_relative_to(s.resolve()) for s in found.values()):p.error('Destination must be outside source skills')
    dst.mkdir(parents=True,exist_ok=True);created=[]
    try:
        with tempfile.TemporaryDirectory(dir=dst,prefix='motion-export-') as td:
            for n in NAMES:shutil.copytree(found[n],Path(td)/n,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.DS_Store'))
            for n in NAMES:
                (Path(td)/n).rename(dst/n);created.append(dst/n)
    except Exception:
        for target in created:shutil.rmtree(target)
        raise
    print(f'Exported {len(NAMES)} skills to {dst}; invoke /motion-studio in Claude Code after transferring to the intended machine.')
if __name__=='__main__':main()
