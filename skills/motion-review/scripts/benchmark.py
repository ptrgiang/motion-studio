#!/usr/bin/env python3
"""Prepare blind calibration media; validate evidence-bound human/agent reviews."""
import argparse,hashlib,importlib.util,json,math,random,shutil,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
DIMENSIONS=('hierarchy','readability','continuity','timing','purpose')
DEFECTS={'kinetic-typography':'Middle word falls outside the safe stage.','mask-reveal':'Reveal stops before the whole headline is visible.','match-cut':'Circle jumps sideways at the cut.','camera-move':'Camera overshoots and loses the intended focus.','ui-interaction':'Saved feedback is delayed after the press.','state-transition':'Object jumps back instead of retaining its final state.'}
def write(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def recipes(source_root=None):
    root=Path(source_root) if source_root else HERE.parent.parent
    for p in root.glob('*/SKILL.md'):
        if 'name: motion-design\n' in p.read_text(encoding='utf-8'):
            s=importlib.util.spec_from_file_location('benchmark_recipes',p.parent/'scripts/recipes.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
    raise ValueError('Install sibling motion-design or pass --source-root')
def prepare(destination,render=False,seed=120,source_root=None):
    dest=Path(destination).resolve()
    if dest.exists():raise ValueError('Benchmark directory exists; use a fresh destination')
    dest.mkdir(parents=True);private=dest/'private';public=dest/'public';private.mkdir();public.mkdir()
    r=recipes(source_root);pairs=[(n,v) for n in r.RECIPES for v in ('intentional','flawed')];random.Random(seed).shuffle(pairs)
    answer={};cases=[]
    for i,(name,variant) in enumerate(pairs):
        cid=f'case-{i+1:02d}';project=r.create(name,private/cid,variant,source_root);spec=json.loads((project/'spec.json').read_text());folder=public/cid;folder.mkdir()
        shutil.copy2(project/'brief.md',folder/'brief.md')
        pipeline=r.load_pipeline(source_root);composition=pipeline.module(project/'src/pillow_composition.py');media=[]
        for fmt in spec['formats']:
            for frame in (0,18,30,48,59,60,66,90,119):
                file=folder/f'{fmt["id"]}-{frame:03d}.png';composition.render_frame(frame,spec,fmt['id'],project).save(file)
                media.append({'path':str(file.relative_to(public)),'sha256':digest(file),'kind':'still','format':fmt['id'],'frame':frame})
        if render:
            pipeline.execute(project,'pillow','benchmark')
            for fmt in spec['formats']:
                file=folder/f'{fmt["id"]}.mp4';shutil.copy2(project/'out/benchmark'/fmt['id']/'film.mp4',file)
                media.append({'path':str(file.relative_to(public)),'sha256':digest(file),'kind':'video','format':fmt['id']})
        cases.append({'id':cid,'fps':spec['fps'],'duration_frames':120,'media':media})
        write(folder/'review.json',{'case_id':cid,'reviewer':None,'observed':{'stills':False,'playback':False},'scores':{k:None for k in DIMENSIONS},'observations':[]})
        answer[cid]={'recipe':name,'variant':variant,'intended_defect':DEFECTS[name] if variant=='flawed' else None}
    write(public/'manifest.json',{'version':'1.2.0','mode':'video-and-stills' if render else 'stills-only','cases':cases})
    write(private/'answer-key.json',answer)
    (public/'README.md').write_text('Review only this public directory. Fill each review.json after observation. Cite manifest media path + SHA256 + integer frame for each scored dimension. Watch both videos before timing/continuity scores. Stills cannot establish playback quality. Keep unavailable scores null. These are silent procedural calibration studies, not professional gold standards.\n')
    return public

def assess(public):
    public=Path(public).resolve();manifest=json.loads((public/'manifest.json').read_text());reports=[]
    for case in manifest['cases']:
        errors=[];review=json.loads((public/case['id']/'review.json').read_text());media={m['path']:m for m in case['media']};evidence={k:[] for k in DIMENSIONS}
        observed=review.get('observed',{});scores=review.get('scores',{})
        if review.get('case_id')!=case['id']:errors.append('Wrong case id')
        if set(scores)!=set(DIMENSIONS):errors.append('Scores must contain exactly the rubric dimensions')
        if set(observed)!= {'stills','playback'} or any(type(v) is not bool for v in observed.values()):errors.append('Observed flags must be booleans')
        for m in case['media']:
            p=(public/m['path']).resolve()
            if not p.is_relative_to(public) or not p.is_file() or digest(p)!=m['sha256']:errors.append('Missing or stale media: '+m['path'])
        observations=review.get('observations',[])
        if not isinstance(observations,list):errors.append('Observations must be a list');observations=[]
        for o in observations:
            if not isinstance(o,dict):errors.append('Malformed observation');continue
            m=media.get(o.get('media'));frame=o.get('frame');dimension=o.get('dimension')
            valid=(m is not None and o.get('sha256')==m['sha256'] and type(frame) is int and 0<=frame<case['duration_frames'] and dimension in evidence and isinstance(o.get('finding'),str) and bool(o['finding'].strip()))
            if valid and m['kind']=='still':valid=frame==m['frame']
            if not valid:errors.append('Observation requires matching media hash, frame, dimension and finding')
            else:evidence[dimension].append(m)
        for k,v in scores.items():
            if v is None:continue
            if type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=5:errors.append('Score must be finite 0..5: '+k);continue
            if not isinstance(review.get('reviewer'),str) or not review['reviewer'].strip():errors.append('Scored review requires reviewer attribution')
            if not evidence.get(k):errors.append('Score requires evidence: '+k)
            if k in ('timing','continuity'):
                if not observed.get('playback') or {m['format'] for m in evidence.get(k,[]) if m['kind']=='video'}!={'wide','vertical'}:errors.append('Timing/continuity require observed video evidence in both formats: '+k)
            elif not observed.get('stills') and not observed.get('playback'):errors.append('Score requires observed media: '+k)
        complete=not errors and all(scores.get(k) is not None for k in DIMENSIONS)
        reports.append({'id':case['id'],'status':'invalid' if errors else 'complete' if complete else 'pending','errors':errors,'scores':scores})
    complete=[r for r in reports if r['status']=='complete']
    return {'version':'1.2.0','cases':reports,'complete':len(complete),'pending':sum(r['status']=='pending' for r in reports),'invalid':sum(r['status']=='invalid' for r in reports),'aggregate_scores':{k:sum(r['scores'][k] for r in complete)/len(complete) for k in DIMENSIONS} if len(complete)==len(reports) and complete else None,'note':'Reviewer judgments, not an automatic aesthetic grade. No aggregate until every case has valid complete reviews.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='command',required=True);a=s.add_parser('prepare');a.add_argument('destination',type=Path);a.add_argument('--render',action='store_true');a.add_argument('--seed',type=int,default=120);a.add_argument('--source-root',type=Path);b=s.add_parser('assess');b.add_argument('public',type=Path);v=p.parse_args()
    try:
        if v.command=='prepare':print(prepare(v.destination,v.render,v.seed,v.source_root))
        else:
            report=assess(v.public);print(json.dumps(report,indent=2));sys.exit(1 if report['invalid'] else 0)
    except (ValueError,OSError,KeyError,TypeError) as e:p.exit(1,str(e)+'\n')
