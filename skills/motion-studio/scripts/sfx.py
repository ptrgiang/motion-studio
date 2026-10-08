#!/usr/bin/env python3
"""Generate original event-seeded SFX and register frame-aligned canonical cues."""
import argparse,hashlib,json,math,random,re,struct,wave
from pathlib import Path
from studio import save,integer
KINDS=('click','tick','blip','whoosh','riser','impact','pad');RATE=48000

def waveform(kind,samples,seed):
    if kind not in KINDS or type(samples) is not int or not 0<samples<=RATE*60:raise ValueError('Invalid sound kind or length (max 60s)')
    rng=random.Random(seed);duration=samples/RATE;result=bytearray();phase=0.;filtered=0.
    for i in range(samples):
        t=i/RATE;p=i/samples;noise=rng.uniform(-1,1);filtered=.88*filtered+.12*noise;fade=min(1,t/.008,(duration-t)/.015)
        if kind in ('click','tick'):value=(.65*noise+.35*math.sin(2*math.pi*2400*t))*math.exp(-t*90)
        elif kind=='blip':value=math.sin(2*math.pi*880*t)*math.exp(-t*8)
        elif kind=='impact':
            phase+=2*math.pi*(45+100*math.exp(-t*18))/RATE;value=(.75*math.sin(phase)+.25*noise*math.exp(-t*22))*math.exp(-t*5)
        elif kind in ('whoosh','riser'):
            phase+=2*math.pi*(300+2500*p*p)/RATE;value=(.7*filtered+.3*math.sin(phase))*((math.sin(math.pi*p)**1.5) if kind=='whoosh' else p*p)
        else:value=sum(math.sin(2*math.pi*f*t) for f in (220,277.18,329.63))/3*min(1,t/.3)*min(1,(duration-t)/.4)
        result+=struct.pack('<h',round(max(-1,min(1,value*fade*.45))*32767))
    return bytes(result)

def create(project,event,kind,cue_id,frames,offset=0,gain_db=0):
    root=Path(project).resolve();spec=json.loads((root/'spec.json').read_text(encoding='utf-8'));inventory=json.loads((root/'assets.json').read_text(encoding='utf-8'));at=spec.get('events',{}).get(event)
    if not integer(at) or not integer(frames) or frames<=0 or not integer(offset) or at+offset<0 or at+offset+frames>spec['duration_frames']:raise ValueError('SFX event/range invalid')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}',cue_id) or any(c['id']==cue_id for c in spec['audio_cues']) or any(a['id']=='sfx-'+cue_id for a in inventory['assets']):raise ValueError('Invalid or duplicate cue id')
    if not isinstance(gain_db,(int,float)) or isinstance(gain_db,bool) or not math.isfinite(gain_db):raise ValueError('Finite gain required')
    path=root/'assets/sfx'/f'{cue_id}.wav';path.parent.mkdir(exist_ok=True)
    if path.exists():raise ValueError('SFX file exists')
    seed=int.from_bytes(hashlib.sha256(f'{spec["seed"]}:{cue_id}:{event}:{kind}'.encode()).digest()[:8],'big');data=waveform(kind,round(frames/spec['fps']*RATE),seed)
    with wave.open(str(path),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(RATE);w.writeframes(data)
    relative=path.relative_to(root).as_posix();inventory['assets'].append({'id':'sfx-'+cue_id,'path':relative,'role':'audio','provenance':f'Original procedural {kind}; stable seed from project/cue/event identity','rights':'original','approved':True,'required':True})
    spec['audio_mode']='designed';spec['audio_cues'].append({'id':cue_id,'path':relative,'role':'music' if kind=='pad' else 'sfx','event_id':event,'start_frame':at+offset,'duration_frames':frames,'visual_event_frame':at,'intentional_offset_frames':offset,'source_offset_seconds':0,'gain_db':gain_db})
    save(root/'spec.json',spec);save(root/'assets.json',inventory);return path
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('project');p.add_argument('--event',required=True);p.add_argument('--kind',choices=KINDS,required=True);p.add_argument('--id',required=True);p.add_argument('--frames',type=int,required=True);p.add_argument('--offset',type=int,default=0);p.add_argument('--gain-db',type=float,default=0);a=p.parse_args()
    try:print(create(a.project,a.event,a.kind,a.id,a.frames,a.offset,a.gain_db))
    except (ValueError,OSError) as e:p.exit(1,str(e)+'\n')
