"""Tests du film des fenêtres modales (ticket 47) : fiche, fichiers générés, garde et journal."""

import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
g = importlib.import_module("render_guarded")
check = importlib.import_module("check_manifest")
FICHE = json.loads((D / "provenance-manifest.json").read_text())
EVENTS = json.loads((D / "capture-events.json").read_text())
PINS = json.loads((D / "input-pins.json").read_text())
DRAFT = D / "media/fenetres-modales-draft.mp4"


def copy_inputs(root):
    for name in (*PINS, "input-pins.json", "output-reference.json", "baseline.html"):
        (root / name).write_bytes((D / name).read_bytes())


class FicheAndGuardTests(unittest.TestCase):
    def test_fiche_has_no_failure(self):
        self.assertEqual(g.fiche_failures(), [])

    def test_text_files_are_generated_from_the_fiche(self):
        self.assertEqual(g.fiche_build.stale_files(FICHE, D), [])

    def test_authorized_inputs_accepted(self):
        self.assertTrue(g.preflight(D / "baseline.html", D / "index.html"))

    def test_altered_voice_clip_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            copy_inputs(root)
            (root / "voice5.wav").write_bytes(b"altered")
            with self.assertRaisesRegex(ValueError, "film_asset_changed:voice5.wav"):
                g.preflight(root / "baseline.html", root / "index.html")

    def test_witness_draft_accepted(self):
        self.assertTrue(g.validate_output(DRAFT))

    def test_film_of_another_pilot_rejected(self):
        other = D.parent / "ff04-room-booking-film/media/room-booking.mp4"
        with self.assertRaisesRegex(ValueError, "film_output_"):
            g.validate_output(other)


class JournalTests(unittest.TestCase):
    """Le journal prouve chaque garantie, et un résultat contraire serait refusé par la fiche."""

    def test_each_guarantee_observed(self):
        seen = EVENTS["observed"]
        self.assertEqual(seen["bad_focus_after_open"], "open-bad")
        self.assertEqual(seen["bad_focus_after_tab"], "help-link")
        self.assertIs(seen["bad_open_after_escape"], True)
        self.assertEqual(seen["good_focus_after_open"], "good-cancel")
        self.assertEqual(seen["good_focus_after_one_tab"], "good-delete")
        self.assertEqual(seen["good_focus_after_two_tabs"], "good-cancel")
        self.assertIs(seen["good_open_after_escape"], False)
        self.assertEqual(seen["good_focus_after_escape"], "open-good")
        self.assertEqual(seen["focus_after_resume"], "next-step")
        self.assertIs(seen["good_dialog_named"], True)

    def test_focus_escaping_the_corrected_dialog_fails_the_fiche(self):
        # Témoin négatif : si le focus était sorti de la fenêtre corrigée, la fiche échouerait.
        events = json.loads(json.dumps(EVENTS))
        events["observed"]["good_focus_after_two_tabs"] = "help-link"
        results = {r["check"]: r["status"] for r in check.check_data(FICHE, D, events)}
        self.assertEqual(results["results"], "FAIL")

    def test_result_dated_outside_its_caption_fails_the_fiche(self):
        events = json.loads(json.dumps(EVENTS))
        for e in events["events"]:
            if e["name"] == "good_focus_restored":
                e["script_s"] = FICHE["film"]["duration_s"] - 1
        results = {r["check"]: r["status"] for r in check.check_data(FICHE, D, events)}
        self.assertEqual(results["gestures"], "FAIL")


if __name__ == "__main__":
    unittest.main()
