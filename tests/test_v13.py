import hashlib,importlib.util,json,os,shutil,subprocess,sys,tempfile,unittest,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SKILL=Path(os.environ.get('MOTION_SKILL_DIR',ROOT/'skills/motion-studio'));sys.path.insert(0,str(SKILL/'scripts'))
from studio import validate
from pipeline import demo
from sfx import waveform,create,RATE,KINDS
from pack_font import pack
from capture import capture
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

def write(path,data):path.write_text(json.dumps(data),encoding='utf-8')
def original_font(path):
    names=['.notdef','space','A','B'];builder=FontBuilder(1000,isTTF=True);builder.setupGlyphOrder(names);builder.setupCharacterMap({32:'space',65:'A',66:'B'});glyphs={}
    for name in names:
        pen=TTGlyphPen(None)
        if name!='space':pen.moveTo((50,0));pen.lineTo((450,0));pen.lineTo((250,700));pen.closePath()
        glyphs[name]=pen.glyph()
    builder.setupGlyf(glyphs);builder.setupHorizontalMetrics({n:(500,0) for n in names});builder.setupHorizontalHeader(ascent=800,descent=-200);builder.setupNameTable({'familyName':'Original Test','styleName':'Regular','uniqueFontIdentifier':'motion-original-test','fullName':'Original Test Regular','psName':'OriginalTest-Regular'});builder.setupOS2(sTypoAscender=800,sTypoDescender=-200,usWinAscent=800,usWinDescent=200);builder.setupPost();builder.setupMaxp();builder.save(path)

class V13Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.tmp=tempfile.TemporaryDirectory();cls.base=Path(cls.tmp.name)/'base';demo(cls.base)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'project';shutil.copytree(self.base,self.root);self.spec=json.loads((self.root/'spec.json').read_text());self.spec['events']={'click':30};write(self.root/'spec.json',self.spec)
    def tearDown(self):self.tmp.cleanup()
    def test_every_sfx_repeatable_and_finite(self):
        for kind in KINDS:
            samples=waveform(kind,4800,42);self.assertEqual(len(samples),9600);self.assertEqual(samples,waveform(kind,4800,42));self.assertNotEqual(samples,bytes(9600))
        self.assertNotEqual(waveform('whoosh',4800,42),waveform('whoosh',4800,43))
    def test_sfx_alignment_and_seed_independence(self):
        path=create(self.root,'click','click','click-one',6);data=path.read_bytes();create(self.root,'click','whoosh','other',12)
        self.assertEqual(data,path.read_bytes());self.assertEqual(validate(self.root),[])
        with wave.open(str(path)) as w:self.assertEqual(w.getframerate(),RATE);self.assertEqual(w.getnframes(),9600)
        spec=json.loads((self.root/'spec.json').read_text());spec['events']['click']=31;write(self.root/'spec.json',spec);self.assertTrue(any('stale' in e for e in validate(self.root)))
    def test_sfx_bad_ranges_and_ids(self):
        for event,frames,offset in [('missing',6,0),('click',6,-31),('click',1000,0)]:
            with self.assertRaises(ValueError):create(self.root,event,'click','bad',frames,offset)
        create(self.root,'click','click','unique',6)
        with self.assertRaises(ValueError):create(self.root,'click','click','unique',6)
    def test_event_schema(self):
        for value in ({'click':True},{'click':180},[],{'click':-1}):
            spec=dict(self.spec,events=value);write(self.root/'spec.json',spec);self.assertTrue(validate(self.root))
    def test_font_coverage_hash_and_approval(self):
        font=Path(self.tmp.name)/'original.ttf';original_font(font);license=Path(self.tmp.name)/'license.txt';license.write_text('Original test font; authored for this repository. MIT.')
        with self.assertRaisesRegex(ValueError,'approved'):pack(self.root,font,license,'TestFont','AB',False)
        with self.assertRaisesRegex(ValueError,'glyph'):pack(self.root,font,license,'TestFont','ABC',True)
        self.spec['shots']=[dict(s,copy='AB') for s in self.spec['shots']];write(self.root/'spec.json',self.spec);record=pack(self.root,font,license,'TestFont','AB',True);self.assertEqual(validate(self.root),[])
        target=self.root/record['path'];target.write_bytes(target.read_bytes()+b'extra');self.assertTrue(any('hash stale' in e for e in validate(self.root)))
    def test_capture_requires_scope_and_fresh_destination(self):
        write(self.root/'capture-plan.json',{'source':'src/product.html'})
        with self.assertRaisesRegex(ValueError,'approved'):capture(self.root)
        with self.assertRaisesRegex(ValueError,'capture id'):capture(self.root,run_id='../escape',rights='original',provenance='fixture',approved=True)
        (self.root/'assets/ui').mkdir()
        with self.assertRaisesRegex(ValueError,'exists'):capture(self.root,rights='original',provenance='fixture',approved=True)
    def test_capture_metadata_tampering(self):
        source=self.root/'src/product.html';source.write_text('<p>Actual source</p>');dest=self.root/'assets/ui';dest.mkdir();image=dest/'saved.png';image.write_bytes(b'synthetic test evidence')
        meta={'source':'src/product.html','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'captures':[{'file':'saved.png','sha256':hashlib.sha256(image.read_bytes()).hexdigest()}]};write(dest/'capture.json',meta)
        inventory=json.loads((self.root/'assets.json').read_text());inventory['assets'].append({'id':'capture','path':'assets/ui/capture.json','role':'capture-metadata','provenance':'Synthetic validation fixture','rights':'original','approved':True,'required':True});write(self.root/'assets.json',inventory);self.assertEqual(validate(self.root),[])
        image.write_bytes(b'changed');self.assertTrue(any('screenshot' in e for e in validate(self.root)))
        write(dest/'capture.json',meta);source.write_text('<p>Edited source</p>');self.assertTrue(any('source changed' in e for e in validate(self.root)))
    @unittest.skipUnless(shutil.which('node'),'Node not available')
    def test_javascript_timing_primitives(self):
        result=subprocess.run(['node',str(ROOT/'tests/timing-v13.mjs'),str(SKILL/'assets/motion-dom.mjs')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)

if __name__=='__main__':unittest.main()
