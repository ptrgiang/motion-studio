#!/usr/bin/env python3
"""Make timestamped contact sheets from stills or selected video frames."""
import argparse, json, math, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

def main():
    p=argparse.ArgumentParser(description=__doc__)
    src=p.add_mutually_exclusive_group(required=True);src.add_argument('--video');src.add_argument('--stills',help='Directory of frame-000000.png style names')
    p.add_argument('--samples',required=True,help='JSON from studio.py samples')
    p.add_argument('--output',required=True);p.add_argument('--columns',type=int,default=4);p.add_argument('--thumb-width',type=int,default=360)
    a=p.parse_args();data=json.loads(Path(a.samples).read_text(encoding='utf-8'));frames=data['frames'];fps=data['fps']
    if not isinstance(fps,(int,float)) or fps<=0 or not frames or a.columns<=0 or a.thumb_width<=0 or any(not isinstance(f,int) or f<0 for f in frames):p.error('Invalid fps/frames/layout')
    if len(frames)>500:p.error('Select <=500 frames; split large reviews into sheets')
    with tempfile.TemporaryDirectory() as td:
        extracted={}
        if a.video:
            ordered=sorted(set(frames))
            # Decode once; select exact frame numbers and map output sequence to them.
            selection='+'.join('eq(n\\,%d)' % f for f in ordered)
            subprocess.run(['ffmpeg','-v','error','-i',a.video,'-vf','select='+selection,'-vsync','0','-frames:v',str(len(ordered)),'-start_number','0','-y',str(Path(td)/'selected-%06d.png')],check=True)
            extracted={f:Path(td)/f'selected-{i:06d}.png' for i,f in enumerate(ordered)}
        imgs=[]
        for f in frames:
            path=extracted[f] if a.video else Path(a.stills)/f'frame-{f:06d}.png'
            if not path.is_file():p.error(f'Missing frame {f}: {path}')
            with Image.open(path) as im: imgs.append((f,im.convert('RGB').copy()))
        ratio=max(im.height/im.width for _,im in imgs);w=a.thumb_width;h=math.ceil(w*ratio);gap=16;label=30;cols=min(a.columns,len(imgs));rows=math.ceil(len(imgs)/cols)
        sheet=Image.new('RGB',(cols*(w+gap)+gap,rows*(h+label+gap)+gap),'#e8e5df');d=ImageDraw.Draw(sheet)
        for i,(f,im) in enumerate(imgs):
            x=gap+(i%cols)*(w+gap);y=gap+(i//cols)*(h+label+gap)
            thumb=ImageOps.contain(im,(w,h));sheet.paste(thumb,(x+(w-thumb.width)//2,y+(h-thumb.height)//2))
            d.text((x,y+h+6),f'frame {f:06d} | {f/fps:.3f}s',fill='#171717')
        out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);sheet.save(out)
        print(f'{out.resolve()} ({len(imgs)} observed-frame slots)')
if __name__=='__main__':main()
