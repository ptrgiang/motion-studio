#!/usr/bin/env python3
"""Package a supplied font and license; inspect cmap coverage of requested glyphs."""
import argparse,hashlib,json,re,shutil
from pathlib import Path
from fontTools.ttLib import TTFont
from studio import save

def pack(project,font_file,license_file,family='MotionFont',text='Motion',approved=False):
    root=Path(project).resolve();font=Path(font_file).resolve();license=Path(license_file).resolve()
    if not approved:raise ValueError('Pass --approved only after confirming font/license rights')
    if not re.fullmatch('[A-Za-z][A-Za-z0-9_-]{0,40}',family):raise ValueError('Invalid font family')
    if not font.is_file() or font.suffix.lower() not in ('.ttf','.otf','.woff','.woff2') or not license.is_file() or not license.read_text(encoding='utf-8').strip():raise ValueError('Font and license files required')
    with TTFont(font) as face:covered=set((face.getBestCmap() or {}).keys())
    missing=sorted({c for c in text if not c.isspace() and ord(c) not in covered})
    if missing:raise ValueError('Missing font glyphs: '+''.join(missing))
    dest=root/'assets/fonts';dest.mkdir(parents=True,exist_ok=True);output=dest/(family+font.suffix.lower());terms=dest/(family+'-LICENSE.txt')
    if output.exists() or terms.exists():raise ValueError('Font destination exists')
    spec=json.loads((root/'spec.json').read_text(encoding='utf-8'));inventory=json.loads((root/'assets.json').read_text(encoding='utf-8'))
    if any(a['id'] in ('font-'+family,'font-license-'+family) for a in inventory['assets']):raise ValueError('Font id exists')
    shutil.copy2(font,output);shutil.copy2(license,terms)
    for aid,path,role in [('font-'+family,output,'font'),('font-license-'+family,terms,'font-license')]:inventory['assets'].append({'id':aid,'path':path.relative_to(root).as_posix(),'role':role,'provenance':'Supplied font with packaged license; approval asserted by caller','rights':'licensed','approved':True,'required':True})
    spec.setdefault('fonts',[]).append({'family':family,'path':output.relative_to(root).as_posix(),'license_path':terms.relative_to(root).as_posix(),'css':f'400 32px {family}','checked_text':text,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()})
    save(root/'spec.json',spec);save(root/'assets.json',inventory);return spec['fonts'][-1]
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('project');p.add_argument('font_file');p.add_argument('--license-file',required=True);p.add_argument('--family',default='MotionFont');p.add_argument('--text',default='Motion');p.add_argument('--approved',action='store_true');a=p.parse_args()
    try:print(json.dumps(pack(a.project,a.font_file,a.license_file,a.family,a.text,a.approved),indent=2,ensure_ascii=False))
    except (ValueError,OSError) as e:p.exit(1,str(e)+'\n')
