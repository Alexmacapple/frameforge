"""Tests du contrôle de la fiche de film (manifeste de provenance, FF-04)."""

import copy
import importlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
m = importlib.import_module("check_manifest")
MANIFEST = json.loads((D / "provenance-manifest.json").read_text())
TEXT_FILES = (
    "index.html",
    "captions.srt",
    "captions.vtt",
    "transcript.txt",
    "capture-events.json",
    "kokoro-input-pins.json",
    "provenance-manifest.json",
)


def statuses(results):
    return {r["check"]: r["status"] for r in results}


def failed(results):
    return sorted(r["check"] for r in results if r["status"] == "FAIL")


def mutated(change):
    data = copy.deepcopy(MANIFEST)
    change(data)
    return m.check_data(data, D)


class ManifestTests(unittest.TestCase):
    def test_nominal_manifest_has_no_failure(self):
        results = m.check_data(MANIFEST, D)
        self.assertEqual(failed(results), [])
        self.assertEqual(len(MANIFEST["scenes"]), 3)

    def test_open_checks_are_reported_unverified_not_passed(self):
        results = m.check_data(MANIFEST, D)
        open_checks = [r for r in results if r["check"] == "open_check"]
        self.assertEqual(len(open_checks), len(MANIFEST["film"]["open_checks"]))
        self.assertTrue(all(r["status"] == "UNVERIFIED" for r in open_checks))
        self.assertEqual(m.exit_code(results), 2)

    def test_unknown_field_rejected(self):
        self.assertIn(
            "schema", failed(mutated(lambda d: d["scenes"][0].update(mood="calme")))
        )

    def test_narration_text_must_match_transcript(self):
        def change(d):
            d["scenes"][0]["narration"]["text"] = "Un autre nom est saisi."

        self.assertIn("texts", failed(mutated(change)))

    def test_narration_start_must_match_composition(self):
        def change(d):
            d["scenes"][1]["narration"]["start_s"] = 5.0

        self.assertIn("composition", failed(mutated(change)))

    def test_caption_timing_must_match_subtitles(self):
        def change(d):
            d["scenes"][2]["caption"]["end_s"] = 13.0

        self.assertIn("captions", failed(mutated(change)))

    def test_result_shown_before_its_announcement_rejected(self):
        # Défaut de l'ancien film : confirmation à 8,43 s pour un sous-titre qui commence à 10 s.
        events = json.loads((D / "capture-events.json").read_text())
        for event in events["events"]:
            if event["name"] in ("send_clicked", "confirmation_visible"):
                event["script_s"] = 8.43
        self.assertIn("gestures", failed(m.check_data(MANIFEST, D, events=events)))

    def test_observed_result_must_match_expected(self):
        def change(d):
            d["scenes"][0]["result"]["expected"] = "Autre nom"

        self.assertIn("results", failed(mutated(change)))

    def test_unpinned_media_rejected(self):
        def change(d):
            d["scenes"][0]["narration"]["audio_ref"] = "voice1.m4a"

        self.assertIn("pinned_media", failed(mutated(change)))

    def test_unverified_scene_blocks_reviewed_film(self):
        def change(d):
            d["scenes"][1]["evidence_status"] = "unverified"

        self.assertIn("statuses", failed(mutated(change)))

    def test_approval_must_name_the_exact_film(self):
        def change(d):
            d["film"]["output_sha256"] = "0" * 64

        self.assertIn("approval", failed(mutated(change)))

    def test_overlapping_narrations_rejected(self):
        def change(d):
            d["scenes"][1]["narration"]["start_s"] = 4.0

        self.assertIn("timeline", failed(mutated(change)))

    def test_changed_source_rejected(self):
        def change(d):
            d["source"]["sha256"] = "0" * 64

        self.assertIn("source", failed(mutated(change)))

    def test_missing_local_media_is_unverified_not_passed(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "pilot"
            root.mkdir()
            (Path(t) / "form-pilot").mkdir()
            for name in TEXT_FILES:
                shutil.copyfile(D / name, root / name)
            shutil.copyfile(
                D.parent / "form-pilot/form.html", Path(t) / "form-pilot/form.html"
            )
            approval = Path(MANIFEST["film"]["approval"]["ref"]).name
            shutil.copyfile(D.parent / approval, Path(t) / approval)
            results = m.check_data(MANIFEST, root)
            self.assertEqual(failed(results), [])
            self.assertEqual(statuses(results)["measured_audio"], "UNVERIFIED")
            self.assertEqual(statuses(results)["output_film"], "UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
