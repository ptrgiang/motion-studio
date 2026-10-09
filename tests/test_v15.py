import unittest,tempfile,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/motion-studio/scripts'))
from pipeline import demo
from studio import validate
class ExposureContract(unittest.TestCase):
 def test_rejects_bad_exposure_before_render(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td)/'p';demo(root);p=root/'spec.json';s=json.loads(p.read_text())
   for settings in [{'adapter':'unknown'},{'adapter':'craft','samples':0},{'adapter':'craft','shutter':2},{'adapter':'craft','cuts':[60,30]},{'adapter':'craft','cuts':[180]}]:
    s['render']=settings;p.write_text(json.dumps(s));self.assertTrue(validate(root),settings)
   s['render']={'adapter':'craft','samples':3,'shutter':.5,'cuts':[60,120]};p.write_text(json.dumps(s));self.assertEqual(validate(root),[])
