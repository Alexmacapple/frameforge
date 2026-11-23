"""Adversarial trust-boundary tests; no media render or file mutation outside temp."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from guarded_hyperframes import preflight
from guarded_hyperframes_v3 import check_approval

HERE=Path(__file__).resolve().parent
BASE=(HERE/'local/baseline.html').read_bytes()
CANDIDATE=(HERE/'local/index.html').read_bytes()
FORGED=CANDIDATE.replace(b'Les deux t\xc3\xa2ches sont visibles.',b'Les deux t\xc3\xa2ches ont disparu.')
PIN=hashlib.sha256(BASE).hexdigest()

class Boundary(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.d=Path(self.t.name)
        self.base=self.d/'baseline.html'
        self.candidate=self.d/'candidate.html'
        self.base.write_bytes(BASE)
        self.candidate.write_bytes(CANDIDATE)

    def test_fixed_external_pin_rejects_forged_baseline(self):
        self.base.write_bytes(FORGED)
        self.candidate.write_bytes(FORGED)
        with self.assertRaisesRegex(ValueError,'approved_reference_digest_mismatch'):
            check_approval(self.base,PIN)

    def test_attacker_controls_baseline_and_pin_bypass(self):
        self.base.write_bytes(FORGED)
        self.candidate.write_bytes(FORGED)
        attacker_pin=hashlib.sha256(FORGED).hexdigest()
        self.assertTrue(check_approval(self.base,attacker_pin))
        self.assertTrue(preflight(self.base,self.candidate))

    def test_fixed_pin_accepts_original_reference(self):
        self.assertTrue(check_approval(self.base,PIN))
        self.assertTrue(preflight(self.base,self.candidate))

if __name__=='__main__':
    unittest.main()
