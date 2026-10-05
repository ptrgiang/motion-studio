"""Seekable motion studies: all state derives from integer frame, no mutable history."""
import math, os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
RECIPES=('kinetic-typography','mask-reveal','match-cut','camera-move','ui-interaction','state-transition')
BG='#101a27'; FG='#f1eee6'; ACCENT='#b9ef72'; MUTED='#8996a8'
def progress(frame,start,end):
    return max(0.,min(1.,(frame-start)/max(1,end-start)))
def ease(t):return 1-(1-t)**3
def spring(t):
    """Analytical damped response, snapped to rest at phase end."""
    if t<=0:return 0.
    if t>=1:return 1.
    return 1-math.exp(-8*t)*math.cos(10*t)
def font(size):
    for p in (os.environ.get('MOTION_FONT_PATH',''),'/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','C:/Windows/Fonts/arial.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
        if p and Path(p).is_file():return ImageFont.truetype(p,max(8,round(size)))
    return ImageFont.load_default(size=max(8,round(size)))
def render(frame,spec,format_id,recipe,variant='intentional'):
    if recipe not in RECIPES:raise ValueError('Unknown recipe')
    if variant not in ('intentional','flawed'):raise ValueError('Unknown variant')
    if isinstance(frame,bool) or not isinstance(frame,int) or not 0<=frame<spec['duration_frames']:raise ValueError('Frame outside timeline')
    fmt=next(f for f in spec['formats'] if f['id']==format_id)
    w,h=fmt['width'],fmt['height']; safe=fmt['safe']; l,r,t,b=safe['left'],w-safe['right'],safe['top'],h-safe['bottom']
    cw,ch=r-l,b-t; cx,cy=(l+r)/2,t+ch*.53; unit=min(cw,ch); vertical=h>w
    im=Image.new('RGB',(w,h),BG);d=ImageDraw.Draw(im);bad=variant=='flawed'; n=spec['duration_frames']; f=frame*120/n
    def text(x,y,copy,size,color=FG,anchor='mm'):
        d.text((round(x),round(y)),copy,font=font(size),fill=color,anchor=anchor)
    def disc(x,y,radius,color=ACCENT):d.ellipse((round(x-radius),round(y-radius),round(x+radius),round(y+radius)),fill=color)
    def box(bounds,fill,outline=None):d.rounded_rectangle(tuple(round(v) for v in bounds),radius=round(unit*.035),fill=fill,outline=outline,width=2)
    text(l,t+unit*.035,'MOTION / STUDY',unit*.026,MUTED,'lm')
    text(l,b-unit*.025,recipe.upper().replace('-',' '),unit*.023,MUTED,'lm')
    if recipe=='kinetic-typography':
        words=['MAKE','SPACE','MATTER']; size=unit*.125
        for i,word in enumerate(words):
            p=ease(progress(f,i*9,24+i*9)); y=cy+(i-1)*unit*.16+(1-p)*unit*.12
            x=cx+(unit*.95 if bad and i==1 else 0)
            text(x,y,word,size,ACCENT if i==1 else FG)
    elif recipe=='mask-reveal':
        layer=im.copy();ld=ImageDraw.Draw(layer)
        ld.text((cx,cy),'REVEAL',font=font(unit*.13),fill=FG,anchor='mm')
        p=ease(progress(f,8,48)); bounds=ld.textbbox((cx,cy),'REVEAL',font=font(unit*.13),anchor='mm')
        x=bounds[0]+(bounds[2]-bounds[0])*p
        if bad:x=bounds[0]+(bounds[2]-bounds[0])*.38*p
        mask=Image.new('L',(w,h));md=ImageDraw.Draw(mask);md.rectangle((l,t,x,b),fill=255)
        im.paste(layer,(0,0),mask);d=ImageDraw.Draw(im)
        d.line((x,cy-unit*.12,x,cy+unit*.12),fill=ACCENT,width=max(2,round(unit*.006)))
    elif recipe=='match-cut':
        x=cx+((-unit*.3 if f<60 else unit*.3) if bad else 0); radius=unit*.105
        if f<60:
            disc(x,cy,radius);text(cx,cy+unit*.23,'One shape.',unit*.055)
        else:
            box((cx-unit*.3,cy-unit*.24,cx+unit*.3,cy+unit*.28),'#263849')
            disc(x,cy,radius);text(cx,cy+unit*.39,'A new context.',unit*.055)
    elif recipe=='camera-move':
        p=ease(progress(f,12,66)) if not bad else spring(progress(f,12,30))*1.5
        zoom=1+.6*p; ox=-unit*.22*p
        for i in range(3):
            x=cx+((i-1)*unit*.24+ox)*zoom
            disc(x,cy,unit*.052*zoom,ACCENT if i==2 else '#4b6077')
        text(cx,cy+unit*.29,'Find the focus.',unit*.055)
    elif recipe=='ui-interaction':
        # Fictional controls, never evidence of a real product.
        text(cx,cy-unit*.33,'SCHEMATIC UI',unit*.035,MUTED)
        press=progress(f,28,34);response=ease(progress(f,65 if bad else 34,91 if bad else 52))
        bw=unit*.44; bh=unit*.16;scale=1-.05*math.sin(math.pi*press)
        box((cx-bw*scale/2,cy-bh*scale/2,cx+bw*scale/2,cy+bh*scale/2),ACCENT)
        text(cx,cy,'SAVE' if response<.95 else 'SAVED',unit*.06,BG)
        if response>0:
            d.line((cx-unit*.06,cy+unit*.2,cx-unit*.015,cy+unit*.245,cx+unit*.09*response,cy+unit*.14),fill=ACCENT,width=max(2,round(unit*.012)))
        px=cx+unit*.36*(1-ease(progress(f,8,28)))
        d.polygon([(px,cy),(px+unit*.03,cy+unit*.08),(px+unit*.06,cy+unit*.045)],fill=FG)
    else:
        p=ease(progress(f,18,66)); x=cx+(-unit*.25+unit*.5*p); y=cy
        if bad and f>=60:x=cx-unit*.25
        radius=unit*(.07+.04*p);disc(x,y,radius)
        d.line((l+cw*.2,cy+unit*.23,r-cw*.2,cy+unit*.23),fill='#394b60',width=2)
        text(cx,cy+unit*.36,'Same object. New state.',unit*.043)
    return im
