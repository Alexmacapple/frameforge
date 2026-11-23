"""Tests du second film produit depuis une fiche : garde, fiche, fichiers générés et gestes."""

import importlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
g = importlib.import_module("render_guarded")
FICHE = json.loads((D / "provenance-manifest.json").read_text())
EVENTS = json.loads((D / "capture-events.json").read_text())
PINS = json.loads((D / "input-pins.json").read_text())
DRAFT = D / "media/room-booking-draft.mp4"


def pointer_pixels(film, at):
    raw = subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-ss",
            f"{at:.3f}",
            "-i",
            str(film),
            "-frames:v",
            "1",
            "-vf",
            "scale=480:270:flags=area",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-",
        ]
    )
    return sum(
        1
        for i in range(0, len(raw), 3)
        if raw[i] > 200 and 60 < raw[i + 1] < 170 and raw[i + 2] < 90
    )


def confirmation_time(film):
    """Instant où la zone du message de confirmation, relevée à la capture, devient verte."""
    box = EVENTS["result_box"]
    crop = f"crop={int(box['width']) - 40}:{int(box['height']) - 20}:{int(box['x']) + 20}:{int(box['y']) + 10}"
    out = subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(film),
            "-vf",
            crop + ",signalstats,metadata=print:key=lavfi.signalstats.SATAVG:file=-",
            "-f",
            "null",
            "-",
        ],
        text=True,
    )
    time = None
    for line in out.splitlines():
        if "pts_time:" in line:
            time = float(line.split("pts_time:")[1].split()[0])
        elif "SATAVG=" in line and float(line.split("=")[1]) > 5:
            return time
    return None


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
            for name in (
                *PINS,
                "input-pins.json",
                "output-reference.json",
                "baseline.html",
            ):
                (root / name).write_bytes((D / name).read_bytes())
            (root / "voice2.wav").write_bytes(b"altered")
            with self.assertRaisesRegex(ValueError, "film_asset_changed:voice2.wav"):
                g.preflight(root / "baseline.html", root / "index.html")

    def test_witness_draft_accepted(self):
        self.assertTrue(g.validate_output(DRAFT))

    def test_film_of_the_other_pilot_rejected(self):
        other = (
            D.parent
            / "ff10-second-web-demo-transfer/form-pilot-kokoro/media/form-kokoro-pointeur.mp4"
        )
        with self.assertRaisesRegex(ValueError, "film_output_"):
            g.validate_output(other)


class GestureTests(unittest.TestCase):
    def test_pointer_visible_at_each_gesture(self):
        times = {e["name"]: e["script_s"] for e in EVENTS["events"]}
        for scene in FICHE["scenes"]:
            at = times[scene["result"]["event"]] + 0.15
            self.assertGreater(pointer_pixels(DRAFT, at), 8, scene["scene_id"])

    def test_confirmation_appears_inside_its_caption(self):
        shown = confirmation_time(DRAFT)
        assert shown is not None, "message de confirmation jamais affiché"
        caption = FICHE["scenes"][2]["caption"]
        self.assertTrue(caption["start_s"] <= shown <= caption["end_s"], shown)

    def test_no_confirmation_before_the_third_gesture(self):
        shown = confirmation_time(DRAFT)
        assert shown is not None
        self.assertGreater(shown, FICHE["scenes"][1]["caption"]["end_s"])


if __name__ == "__main__":
    unittest.main()
