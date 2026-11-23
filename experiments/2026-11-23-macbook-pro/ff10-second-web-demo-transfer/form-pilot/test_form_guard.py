import importlib.util
from pathlib import Path
import subprocess,tempfile,unittest
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('form_guard',D/'render_guarded.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class GuardTests(unittest.TestCase):
 def test_baseline_accepted(self): self.assertTrue(g.preflight(D/'baseline.html',D/'index.html'))
 def test_bad_html_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'changed.html';p.write_text((D/'index.html').read_text().replace('Camille Martin','Autre nom'))
   with self.assertRaisesRegex(ValueError,'form_reference_or_candidate_changed'):
    g.preflight(D/'baseline.html',p)
 def test_bad_asset_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)
   for n in (*__import__('json').loads((D/'form-input-pins.json').read_text()),'form-output-reference.json','form-input-pins.json','baseline.html'):
    (root/n).write_bytes((D/n).read_bytes())
   (root/'captions.srt').write_bytes(b'altered')
   with self.assertRaisesRegex(ValueError,'form_asset_changed:captions.srt'):
    g.preflight(root/'baseline.html',root/'index.html')
 def test_short_silent_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'short.mp4'
   subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=s=64x64:r=10:d=0.5',
      '-c:v','libx264','-pix_fmt','yuv420p',str(p)],check=True)
   with self.assertRaisesRegex(ValueError,'form_output_duration_invalid'):
    g.validate_output(p)
 def test_draft_output_accepted(self): self.assertTrue(g.validate_output(D/'media/form-draft.mp4'))
if __name__=='__main__':unittest.main()
