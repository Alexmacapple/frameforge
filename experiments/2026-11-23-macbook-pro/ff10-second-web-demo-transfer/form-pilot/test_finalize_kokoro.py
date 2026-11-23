import importlib.util
from pathlib import Path
import tempfile,unittest
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('finalize_kokoro',D/'finalize_kokoro.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class FinalTests(unittest.TestCase):
 def test_reject_unapproved_audio_before_render(self):
  with tempfile.TemporaryDirectory() as t:
   a=Path(t)/'audio.m4a';a.write_bytes(b'not approved')
   out=Path(t)/'out.mp4'
   with self.assertRaisesRegex(ValueError,'unapproved_kokoro_audio'):m.finalize(audio=a,output=out)
   self.assertFalse(out.exists())
 def test_reject_bad_video_stream_without_output(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t)/'out.mp4'
   def bad_render(path): path.write_bytes(b'fake')
   with self.assertRaises(Exception):m.finalize(output=out,render_fn=bad_render)
   self.assertFalse(out.exists())
 def test_exact_approved_result_with_existing_guarded_fixture(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t)/'out.mp4'
   def render(path):path.write_bytes((D/'media/form-guarded.mp4').read_bytes())
   result=m.finalize(output=out,render_fn=render)
   self.assertEqual(result['sha256'],m.APPROVED_SHA)
 def test_existing_output_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t)/'out.mp4';out.write_bytes(b'exists')
   with self.assertRaisesRegex(ValueError,'output_already_exists'):m.finalize(output=out)
if __name__=='__main__':unittest.main()
