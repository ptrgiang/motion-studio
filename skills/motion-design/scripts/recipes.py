#!/usr/bin/env python3
"""Materialize an editable, standalone Pillow study in the canonical studio pipeline."""
import argparse,importlib.util,json,sys,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
RECIPES=('kinetic-typography','mask-reveal','match-cut','camera-move','ui-interaction','state-transition')
def find_skill(name,root=None):
    root=Path(root) if root else HERE.parent.parent
    for path in root.glob('*/SKILL.md'):
        if f'name: {name}\n' in path.read_text(encoding='utf-8'):return path.parent
    raise ValueError(f'Missing sibling {name}; install the complete pack or pass --source-root')
def load_pipeline(root=None):
    path=find_skill('motion-studio',root)/'scripts';sys.path.insert(0,str(path))
    s=importlib.util.spec_from_file_location('motion_recipe_pipeline',path/'pipeline.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
INTENTS={
'kinetic-typography':'Stage three words in reading order, then hold the complete statement.',
'mask-reveal':'Use one moving edge to reveal the entire headline, then hold.',
'match-cut':'Carry the same circle across a cut into a card without moving its screen position.',
'camera-move':'Reframe the rightmost node as the focal point, then settle.',
'ui-interaction':'Show immediate press feedback followed by a saved state in fictional schematic UI.',
'state-transition':'Keep object identity while moving and resizing into a new resting state.'}
def create(recipe,project,variant='intentional',source_root=None):
    if recipe not in RECIPES or variant not in ('intentional','flawed'):raise ValueError('Invalid recipe or variant')
    root=Path(project).resolve();p=load_pipeline(source_root);p.demo(root)
    spec=json.loads((root/'spec.json').read_text());spec.update(duration_frames=120,audio_mode='silent',audio_cues=[])
    spec['shots']=[{'id':'study','start':0,'end':120,'purpose':INTENTS[recipe],'entry_state':'establish primary object','exit_state':'stable reading hold','copy':recipe,'asset_ids':[],'layouts':{'wide':'centered stage inside safe bounds','vertical':'stacked stage inside safe bounds'},'transitions':[{'start':0,'end':66}]}]
    p.write(root/'spec.json',spec);p.write(root/'assets.json',{'assets':[]});(root/'assets/original-tone.wav').unlink()
    shutil.copy2(HERE.parent/'assets/motion_library.py',root/'src/motion_library.py')
    wrapper="import importlib.util\nfrom pathlib import Path\np=Path(__file__).with_name('motion_library.py')\ns=importlib.util.spec_from_file_location('project_motion_library',p)\nm=importlib.util.module_from_spec(s);s.loader.exec_module(m)\ndef render_frame(frame,spec,format_id,project):\n    return m.render(frame,spec,format_id,"+repr(recipe)+","+repr(variant)+")\n"
    (root/'src/pillow_composition.py').write_text(wrapper,encoding='utf-8')
    (root/'brief.md').write_text('# Motion study\n\n'+INTENTS[recipe]+'\n\nOriginal procedural shapes and type; UI is fictional. Silent by design. Inspect both aspect ratios and playback before approval.\n',encoding='utf-8')
    (root/'audio-plan.md').write_text('Silent visual calibration study. No audio review or audio score applies.\n')
    p.write(root/'recipe.json',{'recipe':recipe,'variant':variant,'version':'1.2.0','engine':'pillow'})
    return root
if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('recipe',choices=RECIPES);a.add_argument('project',type=Path);a.add_argument('--variant',choices=['intentional','flawed'],default='intentional');a.add_argument('--source-root',type=Path);v=a.parse_args()
    try:create(v.recipe,v.project,v.variant,v.source_root)
    except (ValueError,OSError) as e:a.exit(1,str(e)+'\n')
