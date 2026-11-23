"""Offline FF-10 regression tests for the selected narrated web draft."""
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

D=Path(__file__).resolve().parent
L=D/'local'
spec=importlib.util.spec_from_file_location('ff10_web_render',L/'render_guarded.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class WebEntrypointTests(unittest.TestCase):
    def test_approved_fixture(self):
        self.assertTrue(mod.check(L/'baseline.html',L/'index.html'))
    def test_protected_caption_rejected(self):
        with self.assertRaisesRegex(ValueError,'protected_caption2_changed'):
            mod.check(L/'baseline.html',L/'adversarial.html')
    def test_forged_reference_rejected(self):
        with self.assertRaisesRegex(ValueError,'approved_fixture_digest_mismatch'):
            mod.check(L/'adversarial.html',L/'adversarial.html')
    def test_unauthorized_caption3_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'candidate.html'
            path.write_text((L/'index.html').read_text().replace('La deuxième reste à faire.','Tout est terminé.'))
            with self.assertRaises(ValueError):
                mod.check(L/'baseline.html',path)
    def test_unauthorized_media_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'candidate.html'
            path.write_text((L/'index.html').read_text().replace('src="capture.webm"','src="other.webm"'))
            with self.assertRaises(ValueError):
                mod.check(L/'baseline.html',path)
    def test_existing_output_not_overwritten(self):
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'existing.mp4'
            out.write_bytes(b'preserve-this-output')
            args=SimpleNamespace(project=L,baseline=L/'baseline.html',candidate=L/'index.html',output=out)
            with self.assertRaisesRegex(ValueError,'output_already_exists'):
                mod.v2.run(args,preflight_fn=mod.check,
                    media=('capture.webm','voice1.m4a','voice2.m4a','voice3.m4a'),
                    config=('index.html','hyperframes.json','package.json','captions.srt','captions.vtt','transcript.txt'))
            self.assertEqual(out.read_bytes(),b'preserve-this-output')
    def test_publish_script_refuses(self):
        p=subprocess.run(['npm','run','publish'],cwd=L,capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0)
    def test_render_script_invokes_guard(self):
        import json
        pkg=json.loads((L/'package.json').read_text())
        self.assertEqual(pkg['scripts']['render'],'python3 render_guarded.py')
    def test_rendered_mp4_integrity(self):
        path=L/'guarded-web-demo.mp4'
        self.assertTrue(path.exists())
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
          '9fbb7c316fb20ef94a0424f231881b5f0f24d86daf32418aadc1a92e94ae11ad')

if __name__=='__main__':unittest.main()
