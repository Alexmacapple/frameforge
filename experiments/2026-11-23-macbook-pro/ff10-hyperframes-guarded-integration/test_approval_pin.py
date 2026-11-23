import tempfile
import unittest
from pathlib import Path
import hashlib

from guarded_hyperframes_v3 import check_approval
from guarded_hyperframes import preflight

HERE=Path(__file__).resolve().parent
L=HERE/"local"
EXPECTED="340fb7b0ffc17605d6f1bbcd9892928c24236b75e44c9a3821a79dac2c9abdb7"

class PinTests(unittest.TestCase):
    def test_baseline_pinned(self):
        self.assertTrue(check_approval(L/"baseline.html",EXPECTED))

    def test_authorized_change(self):
        self.assertTrue(preflight(L/"baseline.html",L/"index.html"))

    def test_adversarial_candidate_rejected(self):
        with self.assertRaisesRegex(ValueError,"protected_caption2_changed"):
            preflight(L/"baseline.html",L/"adversarial.html")

    def test_forged_reference_rejected_even_if_candidate_matches(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/"forged.html"
            p.write_bytes((L/"adversarial.html").read_bytes())
            self.assertTrue(preflight(p,p))
            with self.assertRaisesRegex(ValueError,"approved_reference_digest_mismatch"):
                check_approval(p,EXPECTED)

    def test_digest_argument_invalid(self):
        with self.assertRaisesRegex(ValueError,"invalid_approval_digest"):
            check_approval(L/"baseline.html","invalid")

if __name__=="__main__":
    unittest.main()
