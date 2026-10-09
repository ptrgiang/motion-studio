#!/usr/bin/env python3
"""Mix canonical frame-based cues, duck music, normalize and measure actual output."""
import wave
import argparse,json,math,subprocess
from pathlib import Path
from studio import validate

def run(cmd):
    result=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if result.returncode:raise ValueError(f'{cmd[0]} failed ({result.returncode}): {result.stderr[-2500:]}')
    return result
def measurement(path,integrated=-16,peak=-1):
    r=run(['ffmpeg','-hide_banner','-i',str(path),'-af',f'loudnorm=I={integrated}:TP={peak}:LRA=11:print_format=json','-f','null','-'])
    start=r.stderr.rfind('{');end=r.stderr.find('}',start)
    if start<0 or end<0:raise ValueError('FFmpeg did not return loudness measurements')
    return json.loads(r.stderr[start:end+1])

def mix(project,output):
    root=Path(project).resolve();out=Path(output).resolve()
    errors=validate(root)
    if errors:raise ValueError('; '.join(errors))
    spec=json.loads((root/'spec.json').read_text(encoding='utf-8'))
    if spec['audio_mode']=='silent':raise ValueError('Film is intentionally silent; no audio mix requested')
    if out.exists() and any(out.iterdir()):raise ValueError('Use an empty audio output directory')
    out.mkdir(parents=True,exist_ok=True)
    cues=spec['audio_cues'];fps=spec['fps'];duration=spec['duration_frames']/fps
    command=['ffmpeg','-hide_banner','-v','error'];graph=[];groups={'music':[],'voice':[],'sfx':[]}
    for i,c in enumerate(cues):
        command+=['-i',str(root/c['path'])]
        length=c['duration_frames']/fps;offset=c['source_offset_seconds'];delay=round(c['start_frame']/fps*48000)
        fi=c.get('fade_in_seconds',0);fo=c.get('fade_out_seconds',0)
        if fi+fo>length:raise ValueError(f'{c["id"]}: fades exceed cue duration')
        source=json.loads(run(['ffprobe','-v','error','-show_format','-of','json',str(root/c['path'])]).stdout)
        if float(source['format']['duration'])+.001<offset+length:raise ValueError(f'{c["id"]}: source shorter than trim range')
        chain=f'[{i}:a]atrim=start={offset}:duration={length},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={c["gain_db"]}dB'
        if fi:chain+=f',afade=t=in:st=0:d={fi}'
        if fo:chain+=f',afade=t=out:st={length-fo}:d={fo}'
        graph.append(chain+f',adelay={delay}S:all=1[cue{i}]');groups[c.get('role','sfx')].append(f'[cue{i}]')
    buses=[]
    for role,labels in groups.items():
        if labels:
            graph.append(''.join(labels)+f'amix=inputs={len(labels)}:normalize=0:duration=longest[{role}]');buses.append(role)
    ducked='music' in buses and 'voice' in buses
    if ducked:
        graph+=['[voice]asplit=2[voice_mix][voice_sc]','[music][voice_sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=250[music_duck]']
        buses=[{'music':'music_duck','voice':'voice_mix'}.get(b,b) for b in buses]
    samples=round(duration*48000)
    graph.append(''.join(f'[{b}]' for b in buses)+f'amix=inputs={len(buses)}:normalize=0:duration=longest,apad=whole_len={samples},atrim=end_sample={samples},asetpts=N/SR/TB[mix]')
    raw=out/'mix-raw.wav';final=out/'mix.wav';partial=out/'mix-normalized.partial.wav'
    run(command+['-filter_complex',';'.join(graph),'-map','[mix]','-t',str(duration),'-ar','48000','-ac','2','-c:a','pcm_s24le',str(raw)])
    target=spec.get('audio_target',{});integrated=target.get('integrated_lufs',-16);peak=target.get('true_peak_db',-1)
    before=measurement(raw,integrated,peak)
    if any(not math.isfinite(float(before[k])) for k in ('input_i','input_tp','input_lra','input_thresh','target_offset')):
        raise ValueError('Audio is silent/unmeasurable; cannot claim loudness normalization')
    filt=(f'loudnorm=I={integrated}:TP={peak}:LRA=11:measured_I={before["input_i"]}:measured_TP={before["input_tp"]}:'
          f'measured_LRA={before["input_lra"]}:measured_thresh={before["input_thresh"]}:offset={before["target_offset"]}:linear=true')
    run(['ffmpeg','-v','error','-i',str(raw),'-af',filt,'-ar','48000','-ac','2','-c:a','pcm_s24le',str(partial)])
    with wave.open(str(partial),'rb') as wav:
        expected=samples*wav.getnchannels()*wav.getsampwidth()
        if wav.getnframes()!=samples or len(wav.readframes(samples))!=expected:raise ValueError('Normalized audio is incomplete')
    partial.replace(final)
    after=measurement(final,integrated,peak);lufs=float(after['input_i']);tp=float(after['input_tp'])
    passed=math.isfinite(lufs) and math.isfinite(tp) and abs(lufs-integrated)<=1 and tp<=peak+.2
    report={'targets':{'integrated_lufs':integrated,'true_peak_db':peak},'measured_output':{'integrated_lufs':lufs,'true_peak_db':tp},'loudness_pass':passed,'voice_ducking':ducked,'sample_rate':48000,'channels':2,'source_measurement':before,'output_measurement':after,'listening':'pending'}
    (out/'audio-qc.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if not passed:raise ValueError('Measured output missed audio targets; inspect audio-qc.json')
    return final,report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('project');p.add_argument('--output',required=True);a=p.parse_args()
    try:
        final,report=mix(a.project,a.output);print(json.dumps({'mix':str(final),**report},indent=2))
    except (ValueError,OSError,subprocess.CalledProcessError) as e:p.exit(1,f'Audio failed: {e}\n')
if __name__=='__main__':main()
