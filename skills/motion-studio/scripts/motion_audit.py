#!/usr/bin/env python3
"""Measure motion in encoded film; static windows are review prompts, never a taste score."""
import argparse,json,subprocess,hashlib
from pathlib import Path
import numpy as np

def audit(movie,plan=None):
    movie=Path(movie);meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(movie)]));duration=float(meta['format']['duration'])
    data=subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-vf','fps=6,scale=160:90','-f','rawvideo','-pix_fmt','gray','-'])
    frames=np.frombuffer(data,dtype=np.uint8).reshape(-1,90,160).astype(np.int16);d=np.abs(np.diff(frames,axis=0));area=(d>8).mean(axis=(1,2));energy=d.mean(axis=(1,2))
    declared=(plan or {}).get('rests',[]);windows=[];start=None
    for i,v in enumerate(area):
        if v<.008 and start is None:start=i/6
        if (v>=.008 or i==len(area)-1) and start is not None:
            end=(i+1)/6
            if end-start>=.66:windows.append({'start_seconds':round(start,3),'end_seconds':round(end,3),'declared_rest':any(r['start_seconds']<=start+.17 and r['end_seconds']>=end-.17 for r in declared)})
            start=None
    cuts=set(round(c*6) for c in (plan or {}).get('cuts_seconds',[]));spikes=[{'seconds':round((i+1)/6,3),'mean_delta':round(float(v),2),'declared_cut':i+1 in cuts} for i,v in enumerate(energy) if v>max(20,float(np.median(energy))*5)]
    return {'movie_sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'duration_seconds':duration,'sample_fps':6,'static_windows':windows,'spikes':spikes,'changed_area':area.round(5).tolist(),'mean_delta':energy.round(3).tolist(),'status':'heuristic_review_required','limits':'Low-resolution luma differences miss subtle motion and mistake noise for action. Inspect actual film. Rest is a legitimate design choice.'}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('movie');p.add_argument('--plan');p.add_argument('--out',required=True);a=p.parse_args();result=audit(a.movie,json.loads(Path(a.plan).read_text()) if a.plan else None);Path(a.out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('static_windows','spikes','status')}))
