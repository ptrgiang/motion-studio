"""Version-binding fixtures test integrity, not a claim that fake media passed decode."""
import copy,json,os,shutil,subprocess,sys,tempfile,threading,unittest,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SKILL=Path(os.environ.get('MOTION_SKILL_DIR',ROOT/'skills/motion-studio'));sys.path.insert(0,str(SKILL/'scripts'))
from review import snapshot,write,digest,init,identity,assess,import_notes,compare
from preview import make_server
from pipeline import demo
from studio import validate

class V14Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'project';self.root.mkdir();(self.root/'src').mkdir();(self.root/'assets').mkdir()
        write(self.root/'spec.json',{'fps':30,'duration_frames':60,'audio_mode':'designed','formats':[{'id':'vertical','width':540,'height':960,'safe':dict(top=20,left=20,right=20,bottom=20)},{'id':'wide','width':960,'height':540,'safe':dict(top=20,left=20,right=20,bottom=20)}]})
        write(self.root/'assets.json',{'assets':[{'id':'a','path':'assets/a.txt'}]});(self.root/'assets/a.txt').write_text('original');(self.root/'src/a.mjs').write_text('export const x=1;')
        self.fixture_run('first')
    def tearDown(self):self.tmp.cleanup()
    def fixture_run(self,name):
        out=self.root/'out'/name;out.mkdir(parents=True);exports=[]
        for fmt in ('wide','vertical'):
            d=out/fmt;d.mkdir();film=d/'film.mp4';film.write_bytes(b'Explicit unit fixture, not encoded media')
            write(d/'qc.json',{'technical_pass':True,'full_decode_pass':True,'film_sha256':digest(film)})
            exports.append({'format':fmt,'film':fmt+'/film.mp4','sha256':digest(film),'technical_pass':True})
        write(out/'manifest.json',{'version':'1.4.0','engine':'pillow','input_snapshot':snapshot(self.root),'exports':exports});return out
    @unittest.skipUnless(shutil.which('node'),'Node not installed')
    def test_camera_helpers(self):
        subprocess.run(['node',str(ROOT/'tests/camera-v14.mjs'),str(SKILL/'assets/camera-ui.mjs')],check=True,capture_output=True)
    def test_snapshot_tracks_source_asset_inventory_and_lock(self):
        original=snapshot(self.root);(self.root/'src/a.mjs').write_text('export const x=2;');self.assertNotEqual(original,snapshot(self.root))
        with self.assertRaisesRegex(ValueError,'Stale'):identity(self.root,'first')
        self.fixture_run('new');write(self.root/'package-lock.json',{'version':1})
        with self.assertRaises(ValueError):identity(self.root,'new')
    def test_pending_and_explicit_observations_per_format(self):
        doc=init(self.root,'first');self.assertEqual(assess(self.root,'first')['status'],'review_pending')
        for o in doc['observations'].values():o.update(visual=True,temporal=True,audio=True,note='Explicit fixture observation assertion')
        doc['defects']=[dict(id='d1',format='wide',frame=20,status='open',note='Fixture defect')];p=self.root/'notes.json';write(p,doc)
        self.assertEqual(import_notes(self.root,'first',p)['open_defects'],['d1']);doc['defects'][0].update(status='resolved')
        write(p,doc)
        with self.assertRaisesRegex(ValueError,'resolution'):import_notes(self.root,'first',p)
        doc['defects'][0]['resolution']='Fixture resolution assertion';write(p,doc);self.assertEqual(import_notes(self.root,'first',p)['status'],'review_complete')
        self.assertTrue((self.root/'out/first/review-backup-1.json').exists())
    def test_notes_wrong_binding_flags_frame_and_formats_rejected(self):
        base=init(self.root,'first');p=self.root/'notes.json'
        for modify in (lambda d:d['binding'].update(input_fingerprint='wrong'),lambda d:d['observations']['wide'].update(visual='yes'),lambda d:d['observations'].pop('vertical'),lambda d:d['defects'].append(dict(id='x',format='wide',frame=True,status='open',note='x'))):
            doc=copy.deepcopy(base);modify(doc);write(p,doc)
            with self.assertRaises(ValueError):import_notes(self.root,'first',p)
        self.assertEqual(json.loads((self.root/'out/first/review-v1.4.json').read_text()),base)
    def test_export_tamper_and_stale_observations(self):
        init(self.root,'first');film=self.root/'out/first/wide/film.mp4';film.write_bytes(b'edited')
        with self.assertRaisesRegex(ValueError,'bytes'):assess(self.root,'first')
    def test_compare_keeps_old_snapshot_and_does_not_inherit_review(self):
        init(self.root,'first');(self.root/'src/a.mjs').write_text('revised');self.fixture_run('second');init(self.root,'second')
        report=compare(self.root,'first','second');self.assertEqual(report['changed_inputs'],['src/a.mjs']);self.assertEqual(assess(self.root,'second')['status'],'review_pending')
        (self.root/'assets/a.txt').write_text('changed')
        with self.assertRaises(ValueError):compare(self.root,'first','second')
    def test_silent_review_starts_pending_without_listening_claim(self):
        spec=json.loads((self.root/'spec.json').read_text());spec['audio_mode']='silent';write(self.root/'spec.json',spec);self.fixture_run('silent');init(self.root,'silent');report=assess(self.root,'silent');self.assertNotIn('wide:audio',report['pending'])
    def test_readonly_server_range_confinement_and_stale_config(self):
        server=make_server(self.root,'first');thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start();url=f'http://127.0.0.1:{server.server_port}'
        try:
            with urllib.request.urlopen(url+'/__motion/config') as r:self.assertEqual(json.load(r)['version'],'1.4.0')
            req=urllib.request.Request(url+'/out/first/wide/film.mp4',headers={'Range':'bytes=2-5'})
            with urllib.request.urlopen(req) as r:self.assertEqual(r.status,206);self.assertEqual(len(r.read()),4)
            for path in ('/assets.json','/.env','/src/../../etc/passwd'):
                with self.assertRaises(urllib.error.HTTPError):urllib.request.urlopen(url+path)
            secret=Path(self.tmp.name)/'secret.mjs';secret.write_text('secret');
            try:(self.root/'src/escape.mjs').symlink_to(secret)
            except OSError:pass
            else:
                with self.assertRaises(urllib.error.HTTPError):urllib.request.urlopen(url+'/src/escape.mjs')
            (self.root/'src/a.mjs').write_text('changed')
            with self.assertRaises(urllib.error.HTTPError):urllib.request.urlopen(url+'/__motion/config')
        finally:server.shutdown();server.server_close();thread.join()
    def test_policy_and_camera_validation(self):
        project=Path(self.tmp.name)/'full';demo(project);s=json.loads((project/'spec.json').read_text());s['readability']={'min_text_px':False};write(project/'spec.json',s);self.assertTrue(any('readability' in e for e in validate(project)))
        s.pop('readability');s['shots'][0]['camera']=[[0,[0,0,100,100]],[0,[0,0,100,100]]];write(project/'spec.json',s);self.assertTrue(any('camera' in e for e in validate(project)))
