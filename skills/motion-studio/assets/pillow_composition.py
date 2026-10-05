"""Original procedural graphic demo; replace its composition for a client film."""
import math,os
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

def font(size):
    choices=[os.environ.get('MOTION_FONT_PATH',''),'/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','C:/Windows/Fonts/arial.ttf','/System/Library/Fonts/Supplemental/Arial.ttf']
    for p in choices:
        if p and Path(p).is_file():return ImageFont.truetype(p,size=size)
    return ImageFont.load_default(size=size)
def progress(frame,start,length):return max(0,min(1,(frame-start)/max(1,length)))
def ease(u):return 1-(1-u)**3

def render_frame(frame,spec,format_id,project):
    if not isinstance(frame,int) or not 0<=frame<spec['duration_frames']:raise ValueError('Frame outside timeline')
    fmt=next(f for f in spec['formats'] if f['id']==format_id);w,h=fmt['width'],fmt['height'];vertical=h>w
    im=Image.new('RGB',(w,h),'#ebe7df');d=ImageDraw.Draw(im)
    shot=next(s for s in spec['shots'] if s['start']<=frame<s['end']);i=spec['shots'].index(shot)
    local=frame-shot['start'];enter=ease(progress(local,0,round(spec['fps']*.35)))
    size=min(w,h);margin=max(fmt['safe']['left'],fmt['safe']['right']);ink='#242722';orange='#d65a36'
    # Constant identity: three nodes become a connected path, then a stable mark.
    center=(w*.5,h*.32) if vertical else (w*.28,h*.5);radius=size*.085
    xs=[center[0]+(j-1)*radius*2.7 for j in range(3)]
    shape_enter=enter if i==0 else 1
    y=center[1]+(1-shape_enter)*size*.12
    if i>=1:
        for j in range(2):
            end=xs[j]+(xs[j+1]-xs[j])*enter if i==1 else xs[j+1]
            d.line((xs[j],y,end,y),fill=ink,width=max(2,round(size*.008)))
    for j,x in enumerate(xs):
        r=radius*(.6+.4*shape_enter);d.ellipse((x-r,y-r,x+r,y+r),fill=orange if (j==i%3) else ink)
    textx=w*.5 if vertical else w*.56;texty=h*.60 if vertical else h*.40
    f=font(round(size*.07));words=shot['copy'].split();lines=[];line='';maxwidth=w-margin*2 if vertical else w*.38
    for word in words:
        candidate=(line+' '+word).strip()
        if line and d.textlength(candidate,font=f)>maxwidth:lines.append(line);line=word
        else:line=candidate
    if line:lines.append(line)
    for j,line in enumerate(lines):
        d.text((textx,texty+j*size*.09+(1-enter)*size*.04),line,font=f,fill=ink,anchor='mt' if vertical else 'lt')
    small=font(max(12,round(size*.024)));d.text((fmt['safe']['left'],fmt['safe']['top']),'MOTION STUDY / ORIGINAL GRAPHICS',font=small,fill=ink)
    # Progress is a subtle reading aid; no invented product metrics.
    fraction=(frame+1)/spec['duration_frames'];baseline=h-fmt['safe']['bottom']
    d.line((margin,baseline,w-margin,baseline),fill='#b7b4ab',width=2)
    d.line((margin,baseline,margin+(w-2*margin)*fraction,baseline),fill=orange,width=3)
    return im
