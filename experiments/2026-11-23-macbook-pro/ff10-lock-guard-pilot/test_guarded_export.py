import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("guarded_export", HERE / "guarded_export.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

REFERENCE = """1
00:00:00,350 --> 00:00:05,425
La Lune passe devant le Soleil.
Le satellite SDO observe cette occultation.

2
00:00:08,450 --> 00:00:12,600
Depuis l'espace, DSCOVR montre
son ombre sur la Terre.
"""


class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.ref = self.root / "reference.srt"
        self.ref.write_text(REFERENCE)

    def candidate(self, text):
        p = self.root / "candidate.srt"
        p.write_text(text)
        return p

    def test_allowed_reflow(self):
        p = self.candidate(REFERENCE.replace(
            "La Lune passe devant le Soleil.\nLe satellite",
            "La Lune passe devant le Soleil. Le\nsatellite"))
        self.assertTrue(mod.check(self.ref, p))

    def test_protected_change_rejected(self):
        p = self.candidate(REFERENCE.replace("sur la Terre.", "sur la planète."))
        with self.assertRaisesRegex(ValueError, "protected_cue_2_changed"):
            mod.check(self.ref, p)

    def test_time_change_rejected(self):
        p = self.candidate(REFERENCE.replace("00:00:00,350", "00:00:00,351"))
        with self.assertRaisesRegex(ValueError, "cue_1_words_or_times_changed"):
            mod.check(self.ref, p)

    def test_extra_cue_rejected(self):
        p = self.candidate(REFERENCE + "\n3\n00:00:12,700 --> 00:00:13,000\nExtra\n")
        with self.assertRaisesRegex(ValueError, "expected exactly two"):
            mod.check(self.ref, p)

    def test_no_output_for_bad_change(self):
        p = self.candidate(REFERENCE.replace("sur la Terre.", "sur la planète."))
        output = self.root / "forbidden.mp4"
        with self.assertRaisesRegex(ValueError, "protected_cue_2_changed"):
            mod.export(self.root / "missing.mp4", self.ref, p, output)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
