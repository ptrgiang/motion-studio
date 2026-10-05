import hashlib,importlib.util,json,os,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(os.environ.get('MOTION_SOURCE_ROOT',ROOT/'skills'))
def skill(name):
    return next(p.parent for p in SOURCE.glob('*/SKILL.md') if f'name: {name}\n' in p.read_text(encoding='utf-8'))
def load(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
R=load(skill('motion-design')/'scripts/recipes.py','test_recipes')
L=load(skill('motion-design')/'assets/motion_library.py','test_library')
B=load(skill('motion-review')/'scripts/benchmark.py','test_benchmark')
class RecipeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.root=Path(cls.tmp.name);cls.public=B.prepare(cls.root/'blind',source_root=SOURCE)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_every_recipe_seek_dimensions_and_variant(self):
        key=json.loads((self.root/'blind/private/answer-key.json').read_text())
        for cid,data in key.items():
            project=self.root/'blind/private'/cid;spec=json.loads((project/'spec.json').read_text());pipeline=R.load_pipeline(SOURCE)
            self.assertEqual(pipeline.validate(project),[])
            for fmt in spec['formats']:
                render=pipeline.module(project/'src/pillow_composition.py').render_frame
                expected=render(66,spec,fmt['id'],project);render(119,spec,fmt['id'],project);render(0,spec,fmt['id'],project)
                self.assertEqual(expected.tobytes(),render(66,spec,fmt['id'],project).tobytes());self.assertEqual(expected.size,(fmt['width'],fmt['height']))
                clean=L.render(90,spec,fmt['id'],data['recipe']);bad=L.render(90,spec,fmt['id'],data['recipe'],'flawed')
                # Delayed UI feedback has already recovered by frame90; inspect frame48.
                if data['recipe']=='ui-interaction':clean=L.render(48,spec,fmt['id'],data['recipe']);bad=L.render(48,spec,fmt['id'],data['recipe'],'flawed')
                self.assertNotEqual(clean.tobytes(),bad.tobytes())
            with self.assertRaises(ValueError):L.render(True,spec,'wide',data['recipe'])
    def test_ease_and_spring_endpoints(self):
        self.assertEqual(L.progress(-1,0,20),0);self.assertEqual(L.progress(50,0,20),1)
        self.assertEqual(L.ease(0),0);self.assertEqual(L.ease(1),1);self.assertEqual(L.spring(0),0);self.assertEqual(L.spring(1),1)
    def test_blind_manifest_pending(self):
        report=B.assess(self.public);self.assertEqual(report['pending'],12);self.assertEqual(report['invalid'],0);self.assertIsNone(report['aggregate_scores'])
        self.assertFalse((self.public/'answer-key.json').exists())
        manifest=(self.public/'manifest.json').read_text();self.assertNotIn('flawed',manifest);self.assertNotIn('intended_defect',manifest)
    def test_review_rejects_unobserved_and_fake_evidence(self):
        path=self.public/'case-01/review.json';original=path.read_text();review=json.loads(original);review['scores']['timing']=5;review['reviewer']='test'
        try:
            path.write_text(json.dumps(review));report=B.assess(self.public);self.assertEqual(report['invalid'],1);self.assertIsNone(report['aggregate_scores'])
            review['scores']['timing']=None;review['scores']['readability']=True;path.write_text(json.dumps(review));self.assertEqual(B.assess(self.public)['invalid'],1)
            review['scores']['readability']=4;review['observed']['stills']=True
            m=json.loads((self.public/'manifest.json').read_text())['cases'][0]['media'][0]
            review['observations']=[{'dimension':'readability','media':m['path'],'sha256':m['sha256'],'frame':m['frame'],'finding':'Readable at this frame.'}]
            path.write_text(json.dumps(review));self.assertEqual(B.assess(self.public)['invalid'],0)
            review['observations'][0]['frame']=119;path.write_text(json.dumps(review));self.assertEqual(B.assess(self.public)['invalid'],1)
            review['observations'][0]['frame']=m['frame'];review['observations'][0]['sha256']='stale';path.write_text(json.dumps(review));self.assertEqual(B.assess(self.public)['invalid'],1)
        finally:path.write_text(original)
    def test_media_tampering(self):
        path=self.public/'case-01/wide-000.png';old=path.read_bytes()
        try:path.write_bytes(b'changed');self.assertEqual(B.assess(self.public)['invalid'],1)
        finally:path.write_bytes(old)
    def test_existing_workspace_refused(self):
        with self.assertRaisesRegex(ValueError,'exists'):B.prepare(self.root/'blind',source_root=SOURCE)
if __name__=='__main__':unittest.main()
