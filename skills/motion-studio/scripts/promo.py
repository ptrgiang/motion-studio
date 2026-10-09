#!/usr/bin/env python3
"""Create a 15-second DOM promo of an original functional local app (not a client product)."""
import argparse,json,shutil
from pathlib import Path
from studio import init,save
from pack_font import pack
from sfx import create
HERE=Path(__file__).resolve().parent;ASSETS=HERE.parent/'assets'
def demo(project,font,license):
    root=Path(project).resolve();init(root)
    spec=json.loads((root/'spec.json').read_text());spec.update(duration_frames=450,events={'intro':0,'showProduct':90,'saveNote':150,'darkView':240,'localNote':300,'endCard':360},rhythm={'bpm':100,'offset_frame':0})
    spec['formats']=[{'id':'wide','width':960,'height':540,'safe':{'top':36,'right':48,'bottom':44,'left':48}},{'id':'vertical','width':540,'height':960,'safe':{'top':64,'right':40,'bottom':72,'left':40}}]
    beats=[('hook',0,90,'Small ideas. Worth keeping.','Establish a place for small useful thoughts'),('write',90,210,'Write. Save. Keep.','Demonstrate the actual save interaction'),('theme',210,300,'A calmer view.','Show the working light/dark toggle'),('local',300,360,'Keep it local.','Explain browser-local persistence truthfully'),('end',360,450,'Motion Notes','Resolve into a three-second end card')]
    spec['shots']=[{'id':id,'start':a,'end':b,'copy':copy,'purpose':purpose,'entry_state':'previous beat rests','exit_state':'stable hold','asset_ids':[],'layouts':{'wide':'copy left, captured UI right','vertical':'copy above, captured UI below'},'transitions':[{'start':a,'end':a+24}]} for id,a,b,copy,purpose in beats]
    for shot in spec['shots']:
        if shot['id'] in ('write','theme','local'):shot['asset_ids']=['capture-ui-metadata','capture-ui-draft','capture-ui-saved','capture-ui-dark']
    spec['readability']={'phone_width':360,'min_text_px':12,'min_ui_control_px':18,'words_per_second':3}
    for shot in spec['shots']:
        if shot['id'] in ('write','theme'):
            region=[50,170,760,430] if shot['id']=='write' else [500,0,500,430]
            shot['camera']=[[shot['start'],[0,0,1000,700]],[shot['start']+35,region],[shot['end']-1,region]]
    save(root/'spec.json',spec)
    for file in ('promo-product.html','promo.html','promo-scene.mjs','motion-dom.mjs','browser-runtime.mjs','render-dom.mjs','camera-ui.mjs','readability.mjs'):shutil.copy2(ASSETS/file,root/'src'/file)
    # Product markup expects .ttf; reject rather than silently packaging another extension.
    if Path(font).suffix.lower()!='.ttf':raise ValueError('Promo fixture requires a TTF font')
    pack(root,font,license,'MotionFont',''.join(s['copy'] for s in spec['shots'])+'Motion Notes Write Save Keep Dark view Light view Saved A thought to keep Ý tưởng nhỏ',True)
    save(root/'package.json',{'private':True,'dependencies':{'playwright':'1.62.1'}})
    common={'save':'#save','theme':'#theme','note':'#note'};fill={'type':'fill','selector':'#note','value':'A simple idea: make room for one useful thought.'};click={'type':'click','selector':'#save'}
    save(root/'capture-plan.json',{'source':'src/promo-product.html','viewport':{'width':1000,'height':700},'dpr':2,'ready':'#app','fonts':['400 32px MotionFont'],'states':[{'id':'draft','actions':[fill],'targets':common},{'id':'saved','actions':[fill,click],'ready':'#notes li','targets':common},{'id':'dark','actions':[fill,click,{'type':'click','selector':'#theme'}],'ready':'body.dark','targets':common}]})
    for event,kind,cid,frames,offset,gain in [('intro','pad','bed',450,0,-8),('showProduct','whoosh','product-sweep',18,-12,-8),('saveNote','click','save-click',6,0,-4),('darkView','blip','theme-blip',12,0,-6),('localNote','tick','local-tick',6,0,-10),('endCard','impact','end-impact',24,0,-12)]:create(root,event,kind,cid,frames,offset,gain)
    (root/'brief.md').write_text('# Motion Notes promo\n\n15-second original local demo app. The film demonstrates writing/saving notes, light/dark view and browser-local persistence. These functions exist in src/promo-product.html. No testimonials, performance metrics, external brand claims or fabricated client UI. Both aspect ratios use captured interface states.\n',encoding='utf-8')
    (root/'style-guide.md').write_text('# Direction\n\nQuiet editorial product study: pale sage, deep green, packaged MotionFont, asymmetric wide composition and stacked vertical layout. One focal action per beat. Three-second end hold. Use the packaged captures and coordinate metadata. SFX emphasize only meaningful changes.\n',encoding='utf-8')
    (root/'audio-plan.md').write_text('# Audio\n\nOriginal 48kHz event-seeded pad, whoosh, click, blip, tick and impact. One canonical spec; pre-lap is deliberate on product reveal. Target -16 LUFS/-1dBTP. Playback, listening and final aesthetic approval remain pending.\n',encoding='utf-8')
    print('Install project Playwright, run capture.py with original rights approval, then pipeline.py --engine dom.');return root
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('project');p.add_argument('--font',required=True);p.add_argument('--license-file',required=True);a=p.parse_args()
    try:demo(a.project,a.font,a.license_file)
    except (ValueError,OSError) as e:p.exit(1,str(e)+'\n')
