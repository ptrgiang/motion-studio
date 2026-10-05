#!/usr/bin/env python3
"""Create/check a production record; these checks do not certify aesthetics."""
import argparse, json, math
from pathlib import Path

def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')

def init(root):
    root=Path(root)
    if root.exists() and any(root.iterdir()):
        raise ValueError('Refusing to initialize a nonempty project')
    root.mkdir(parents=True, exist_ok=True)
    for d in ('assets','src','reviews','out'): (root/d).mkdir()
    for name, title in [('brief','Brief'),('reference-analysis','Reference analysis'),('style-guide','Style guide'),('shotlist','Shot list'),('audio-plan','Audio plan')]:
        (root/f'{name}.md').write_text(f'# {title}\n\nDraft: populate from observed inputs before passing the relevant gate.\n', encoding='utf-8')
    save(root/'assets.json', {'assets':[]})
    save(root/'spec.json', {'version':1,'fps':30,'duration_frames':450,'seed':42,
        'formats':[{'id':'wide','width':1920,'height':1080,'safe':{'top':72,'right':96,'bottom':72,'left':96}}],
        'shots':[], 'audio_mode':'silent', 'audio_cues':[]})
    save(root/'status.json', {'autonomy':'autonomous','status':'draft','gates':{f'G{i}':{'state':'pending','evidence':[]} for i in range(1,7)},'next_action':'Complete the director brief and asset provenance.'})
    print(f'Initialized {root.resolve()} (draft)')

def integer(x): return isinstance(x,int) and not isinstance(x,bool)
def finite(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def local(root,path):
    if not isinstance(path,str) or not path: return False
    p=Path(path)
    return not p.is_absolute() and (root/p).resolve().is_relative_to(root.resolve()) and (root/p).is_file()

def validate(root):
    root=Path(root); errors=[]
    spec=json.loads((root/'spec.json').read_text(encoding='utf-8')); inventory=json.loads((root/'assets.json').read_text(encoding='utf-8'))
    if not isinstance(spec,dict) or not isinstance(inventory,dict): return ['Spec and inventory must be objects']
    if not integer(spec.get('version')) or spec.get('version')!=1: errors.append('Unsupported spec version')
    for key in ('fps','duration_frames'):
        if not integer(spec.get(key)) or spec[key]<=0: errors.append(f'{key} must be a positive integer')
    if not integer(spec.get('seed')): errors.append('seed must be an integer')
    n=spec.get('duration_frames') if integer(spec.get('duration_frames')) else 0
    assets=inventory.get('assets'); ids=set()
    if not isinstance(assets,list): errors.append('assets must be an array');assets=[]
    for a in assets:
        if not isinstance(a,dict): errors.append('Asset must be an object');continue
        aid=a.get('id')
        if not isinstance(aid,str) or not aid or aid in ids: errors.append('Asset ids must be unique nonempty strings')
        else: ids.add(aid)
        for key in ('required','approved'):
            if not isinstance(a.get(key),bool): errors.append(f'{aid}: {key} must be boolean')
        if not isinstance(a.get('provenance'),str) or not a['provenance'].strip(): errors.append(f'{aid}: provenance missing')
        if a.get('rights') not in ('user-provided','licensed','original','public-domain','unknown'): errors.append(f'{aid}: rights value invalid')
        if a.get('required') and (not local(root,a.get('path')) or a.get('approved') is not True or a.get('rights')=='unknown'):
            errors.append(f'{aid}: required asset absent, unapproved or rights unknown')
    formats=spec.get('formats');fmt=set()
    if not isinstance(formats,list) or not formats: errors.append('At least one format required');formats=[]
    for f in formats:
        if not isinstance(f,dict): errors.append('Format must be an object');continue
        fid=f.get('id')
        if not isinstance(fid,str) or not fid or fid in fmt: errors.append('Format ids must be unique nonempty strings')
        else: fmt.add(fid)
        if any(not integer(f.get(k)) or f[k]<=0 for k in ('width','height')): errors.append(f'{fid}: invalid dimensions');continue
        safe=f.get('safe',{})
        if not isinstance(safe,dict) or any(not integer(safe.get(k)) or safe[k]<0 for k in ('top','right','bottom','left')): errors.append(f'{fid}: invalid safe insets')
        elif safe['left']+safe['right']>=f['width'] or safe['top']+safe['bottom']>=f['height']: errors.append(f'{fid}: safe area empty')
    shots=spec.get('shots');previous=0;sids=set()
    if not isinstance(shots,list) or not shots: errors.append('At least one shot required');shots=[]
    byid={a['id']:a for a in assets if isinstance(a,dict) and isinstance(a.get('id'),str)}
    for s in shots:
        if not isinstance(s,dict): errors.append('Shot must be an object');continue
        sid=s.get('id')
        if not isinstance(sid,str) or not sid or sid in sids: errors.append('Shot ids must be unique nonempty strings')
        else: sids.add(sid)
        start,end=s.get('start'),s.get('end')
        if not integer(start) or not integer(end) or start!=previous or end<=start or end>n: errors.append(f'{sid}: invalid, overlapping or gapped frame range')
        if integer(end): previous=end
        for key in ('purpose','entry_state','exit_state'):
            if not isinstance(s.get(key),str) or not s[key].strip(): errors.append(f'{sid}: {key} missing')
        if not isinstance(s.get('copy'),str): errors.append(f'{sid}: copy must be a string (empty allowed)')
        layouts=s.get('layouts',{})
        if not isinstance(layouts,dict) or any(not layouts.get(f) for f in fmt): errors.append(f'{sid}: layout required for every format')
        aids=s.get('asset_ids')
        if not isinstance(aids,list) or any(not isinstance(a,str) for a in aids): errors.append(f'{sid}: asset_ids must be strings');aids=[]
        for aid in aids:
            a=byid.get(aid)
            if a is None: errors.append(f'{sid}: unknown asset {aid}')
            elif not local(root,a.get('path')) or a.get('approved') is not True or a.get('rights')=='unknown': errors.append(f'{sid}: used asset {aid} is missing/unapproved/unknown rights')
        transitions=s.get('transitions',[])
        if not isinstance(transitions,list): errors.append(f'{sid}: transitions must be an array');transitions=[]
        for tr in transitions:
            if not isinstance(tr,dict) or not integer(tr.get('start')) or not integer(tr.get('end')) or not 0<=tr['start']<tr['end']<=n: errors.append(f'{sid}: invalid transition range')
    if previous!=n: errors.append('Shots must cover the full duration')
    if (root/'audio-cues.json').exists(): errors.append('Remove audio-cues.json: spec.json.audio_cues is the only cue timeline')
    mode=spec.get('audio_mode')
    if mode not in ('silent','designed'): errors.append('audio_mode must explicitly be silent or designed')
    cues=spec.get('audio_cues');cids=set()
    if not isinstance(cues,list): errors.append('audio_cues must be an array');cues=[]
    if mode=='silent' and cues: errors.append('Silent film cannot contain audio cues')
    if mode=='designed' and not cues: errors.append('Designed audio requires at least one cue')
    for c in cues:
        if not isinstance(c,dict): errors.append('Cue must be an object');continue
        cid=c.get('id')
        if not isinstance(cid,str) or not cid or cid in cids: errors.append('Cue ids must be unique nonempty strings')
        else: cids.add(cid)
        start,duration=c.get('start_frame'),c.get('duration_frames')
        if not integer(start) or not integer(duration) or duration<=0 or start<0 or start+duration>n: errors.append(f'{cid}: cue out of timeline')
        if not local(root,c.get('path')): errors.append(f'{cid}: audio file missing or outside project')
        matched=[a for a in assets if isinstance(a,dict) and a.get('path')==c.get('path')]
        if not any(a.get('approved') is True and a.get('rights') not in ('unknown',None) for a in matched): errors.append(f'{cid}: audio must have an approved provenance asset')
        if c.get('role','sfx') not in ('sfx','music','voice'): errors.append(f'{cid}: unknown audio role')
        for key in ('fade_in_seconds','fade_out_seconds'):
            if key in c and (not finite(c[key]) or c[key]<0): errors.append(f'{cid}: invalid {key}')
        for key in ('source_offset_seconds','gain_db'):
            if not finite(c.get(key)) or (key=='source_offset_seconds' and c[key]<0): errors.append(f'{cid}: invalid {key}')
        for key in ('visual_event_frame','intentional_offset_frames'):
            if not integer(c.get(key)): errors.append(f'{cid}: {key} must be an integer')
        if integer(c.get('visual_event_frame')) and not 0<=c['visual_event_frame']<n: errors.append(f'{cid}: visual event outside film')
    target=spec.get('audio_target',{})
    if not isinstance(target,dict): errors.append('audio_target must be an object')
    else:
        for key,lo,hi in [('integrated_lufs',-70,-5),('true_peak_db',-9,0)]:
            if key in target and (not finite(target[key]) or not lo<=target[key]<=hi): errors.append(f'audio_target: invalid {key}')
    return errors

def samples(root):
    root=Path(root);spec=json.loads((root/'spec.json').read_text(encoding='utf-8'));n=spec['duration_frames'];frames={0,n-1}
    for s in spec['shots']:
        frames.update((s['start'],(s['start']+s['end']-1)//2,s['end']-1))
        for tr in s.get('transitions',[]):
            # Every frame across short transitions; stride for long moves plus endpoints.
            a,b=tr['start'],tr['end'];stride=max(1,(b-a)//30)
            frames.update(range(a-1,b+1,stride));frames.update((a-1,a,b-1,b))
    for c in spec.get('audio_cues',[]): frames.add(c['visual_event_frame'])
    print(json.dumps({'fps':spec['fps'],'frames':sorted(f for f in frames if 0<=f<n)},indent=2))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['init','validate','samples']);p.add_argument('project');a=p.parse_args()
    try:
        if a.command=='init':init(a.project)
        elif a.command=='samples':samples(a.project)
        else:
            errors=validate(a.project);print(json.dumps({'structural_pass':not errors,'errors':errors,'note':'Does not certify visual, audio or factual quality.'},indent=2));return 1 if errors else 0
    except (OSError,ValueError,KeyError,TypeError) as e: p.exit(2,f'Error: {e}\n')
    return 0
if __name__=='__main__':raise SystemExit(main())
