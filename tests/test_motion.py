import copy,hashlib,importlib.util,json,os,shutil,sys,tempfile,unittest,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=Path(os.environ.get('MOTION_SKILL_DIR',ROOT/'skills/motion-studio'))
sys.path.insert(0,str(SKILL/'scripts'))
from studio import validate
from pipeline import demo,execute,module
from audio import mix
from export_claude import export,NAMES

def write(p,data):p.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
class StudioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.base=Path(cls.tmp.name)/'sample';demo(cls.base)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)/'film';shutil.copytree(self.base,self.root);self.spec=json.loads((self.root/'spec.json').read_text(encoding='utf-8'))
    def tearDown(self):self.temp.cleanup()
    def change(self,fn):fn(self.spec);write(self.root/'spec.json',self.spec);return validate(self.root)
    def test_valid_demo(self):self.assertEqual(validate(self.root),[])
    def test_bad_fps(self):self.assertTrue(self.change(lambda s:s.update(fps=True)))
    def test_boolean_version(self):self.assertTrue(self.change(lambda s:s.update(version=True)))
    def test_gap(self):self.assertTrue(self.change(lambda s:s['shots'][1].update(start=61)))
    def test_short_coverage(self):self.assertTrue(self.change(lambda s:s['shots'][-1].update(end=179)))
    def test_missing_layout(self):self.assertTrue(self.change(lambda s:s['shots'][0]['layouts'].pop('vertical')))
    def test_missing_asset(self):self.assertTrue(self.change(lambda s:s['shots'][0].update(asset_ids=['nonexistent'])))
    def test_unapproved_audio(self):
        a=json.loads((self.root/'assets.json').read_text());a['assets'][0]['approved']=False;write(self.root/'assets.json',a);self.assertTrue(validate(self.root))
    def test_escape_path(self):self.assertTrue(self.change(lambda s:s['audio_cues'][0].update(path='../outside.wav')))
    def test_two_cue_timelines(self):write(self.root/'audio-cues.json',[]);self.assertTrue(validate(self.root))
    def test_silent_with_cue(self):self.assertTrue(self.change(lambda s:s.update(audio_mode='silent')))
    def test_designed_without_cue(self):self.assertTrue(self.change(lambda s:s.update(audio_cues=[])))
    def test_duplicate_cue(self):self.assertTrue(self.change(lambda s:s['audio_cues'].append(copy.deepcopy(s['audio_cues'][0]))))
    def test_invalid_gain(self):self.assertTrue(self.change(lambda s:s['audio_cues'][0].update(gain_db='loud')))
    def test_unicode(self):self.assertEqual(self.change(lambda s:s['shots'][0].update(copy='Chuyển động rõ ràng')),[])
    def test_safe_empty(self):self.assertTrue(self.change(lambda s:s['formats'][0]['safe'].update(left=960)))
    def test_pixel_seek(self):
        render=module(self.root/'src/pillow_composition.py').render_frame
        for fmt in self.spec['formats']:
            expected=render(90,self.spec,fmt['id'],self.root);render(179,self.spec,fmt['id'],self.root);render(0,self.spec,fmt['id'],self.root)
            self.assertEqual(expected.tobytes(),render(90,self.spec,fmt['id'],self.root).tobytes());self.assertEqual(expected.size,(fmt['width'],fmt['height']))
        with self.assertRaises(ValueError):render(180,self.spec,'wide',self.root)
    def test_short_audio_source(self):
        self.spec['audio_cues'][0]['source_offset_seconds']=5;write(self.root/'spec.json',self.spec)
        with self.assertRaisesRegex(ValueError,'source shorter'):mix(self.root,self.root/'mix')
    def test_audio_alignment_and_duck(self):
        cue=self.spec['audio_cues'][0];cue.update(start_frame=30,duration_frames=90,visual_event_frame=30,fade_in_seconds=0,fade_out_seconds=0)
        voice=copy.deepcopy(cue);voice.update(id='voice',role='voice');self.spec['audio_cues'].append(voice);write(self.root/'spec.json',self.spec)
        path,report=mix(self.root,self.root/'mix');self.assertTrue(report['voice_ducking']);self.assertTrue(report['loudness_pass'])
        with wave.open(str(path.parent/'mix-raw.wav'),'rb') as wav:
            self.assertEqual(wav.getframerate(),48000);self.assertEqual(wav.getnchannels(),2)
            first=wav.readframes(47000);self.assertLessEqual(max(abs(int.from_bytes(first[i:i+3],'little',signed=True)) for i in range(0,len(first),3)),2)
            later=wav.readframes(9600);self.assertGreater(max(abs(int.from_bytes(later[i:i+3],'little',signed=True)) for i in range(0,len(later),3)),100)
    def test_odd_dimensions_rejected(self):
        self.spec['formats'][0]['width']=961;write(self.root/'spec.json',self.spec)
        with self.assertRaisesRegex(ValueError,'even'):execute(self.root,'pillow','bad-dim')

class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.source=Path(self.temp.name)/'source';self.dest=Path(self.temp.name)/'target'
        # Small parser fixtures, never installed or presented as production skills.
        for name in NAMES:
            p=self.source/name;p.mkdir(parents=True);(p/'SKILL.md').write_text(f'---\nname: {name}\ndescription: Test fixture\n---\n\nFixture\n',encoding='utf-8')
    def tearDown(self):self.temp.cleanup()
    def test_install_refusal_update_backup(self):
        export(self.source,self.dest)
        with self.assertRaises(ValueError):export(self.source,self.dest)
        p=self.source/NAMES[0]/'SKILL.md';p.write_text(p.read_text()+'Updated\n')
        plan=export(self.source,self.dest,True,True);self.assertEqual(len(plan['diff']['changed']),1)
        report=export(self.source,self.dest,True);self.assertTrue(Path(report['backup']).is_dir());self.assertEqual((self.dest/NAMES[0]/'SKILL.md').read_text(),p.read_text())
    def test_local_edit_protected(self):
        export(self.source,self.dest);(self.dest/NAMES[0]/'custom.txt').write_text('Keep my work')
        with self.assertRaisesRegex(ValueError,'baseline'):export(self.source,self.dest,True)
    def test_legacy_protected(self):
        (self.dest/NAMES[0]).mkdir(parents=True)
        with self.assertRaisesRegex(ValueError,'baseline'):export(self.source,self.dest,True)
    def test_missing_source(self):
        shutil.rmtree(self.source/NAMES[-1])
        with self.assertRaisesRegex(ValueError,'Missing'):export(self.source,self.dest)

@unittest.skipUnless(os.environ.get('MOTION_INTEGRATION')=='1','Set MOTION_INTEGRATION=1 for full FFmpeg pipeline')
class IntegrationTests(unittest.TestCase):
    def test_full_pipeline_both_formats(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'film';demo(root);out=execute(root,'pillow','run1')
            report=json.loads((out/'manifest.json').read_text());self.assertFalse(report['final']);self.assertEqual(len(report['exports']),2)
            self.assertEqual(json.loads((out/'pipeline-state.json').read_text())['status'],'technical_pass_review_pending')
            for fmt in ['wide','vertical']:
                qc=json.loads((out/fmt/'qc.json').read_text());self.assertTrue(qc['technical_pass']);self.assertEqual(qc['temporal_review'],'pending');self.assertTrue((out/fmt/'contact-sheet.png').is_file());self.assertTrue((out/fmt/'poster.png').is_file())
            with self.assertRaises(ValueError):execute(root,'pillow','run1')
    def test_silent_pipeline(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'film';demo(root);spec=json.loads((root/'spec.json').read_text());spec.update(audio_mode='silent',audio_cues=[]);spec['formats']=spec['formats'][:1];write(root/'spec.json',spec)
            out=execute(root,'pillow','silent');qc=json.loads((out/'wide/qc.json').read_text());self.assertEqual(qc['audio_listening'],'not_applicable_intentional_silence')
if __name__=='__main__':unittest.main()
