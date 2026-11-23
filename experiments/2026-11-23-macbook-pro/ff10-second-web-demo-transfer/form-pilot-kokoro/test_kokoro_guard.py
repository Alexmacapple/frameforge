"""Tests du rendu gardé Kokoro. Les médias locaux doivent avoir été préparés par prepare_inputs.py."""

import importlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

D = Path(__file__).resolve().parent
THOMAS_PILOT = D.parent / "form-pilot"
sys.path.insert(0, str(D))
g = importlib.import_module("render_guarded")
p = importlib.import_module("prepare_inputs")
PINS = json.loads((D / "kokoro-input-pins.json").read_text())


def copy_project(root):
    for name in (
        *PINS,
        "kokoro-input-pins.json",
        "kokoro-output-reference.json",
        "baseline.html",
    ):
        (root / name).write_bytes((D / name).read_bytes())


class PreflightTests(unittest.TestCase):
    def test_authorized_inputs_accepted(self):
        self.assertTrue(g.preflight(D / "baseline.html", D / "index.html"))

    def test_changed_html_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            changed = Path(t) / "changed.html"
            changed.write_text(
                (D / "index.html").read_text().replace("Camille Martin", "Autre nom")
            )
            with self.assertRaisesRegex(
                ValueError, "kokoro_reference_or_candidate_changed"
            ):
                g.preflight(D / "baseline.html", changed)

    def test_altered_kokoro_clip_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            copy_project(root)
            (root / "kokoro2.wav").write_bytes(b"altered")
            with self.assertRaisesRegex(ValueError, "kokoro_asset_changed:kokoro2.wav"):
                g.preflight(root / "baseline.html", root / "index.html")

    def test_thomas_voice_is_not_a_declared_input(self):
        self.assertFalse(
            [name for name in (*PINS, *g.MEDIA) if name.startswith("voice")]
        )
        self.assertNotIn(
            "voice", (D / "index.html").read_text().replace('id="voice', "")
        )


class FicheTests(unittest.TestCase):
    """La fiche de film (provenance-manifest.json) conditionne le rendu."""

    def test_coherent_fiche_reports_no_failure(self):
        self.assertEqual(g.fiche_failures(), [])

    def test_incoherent_fiche_blocks_preflight(self):
        # Fiche et empreintes à jour, mais narration décalée par rapport à la composition.
        fiche = g.load_fiche()
        fiche["scenes"][2]["narration"]["start_s"] = 9.0
        with mock.patch.object(g, "load_fiche", return_value=fiche):
            with self.assertRaisesRegex(ValueError, "kokoro_fiche_incoherent:.*composition"):
                g.preflight(D / "baseline.html", D / "index.html")

    def test_fiche_and_capture_events_are_pinned_inputs(self):
        for name in ("provenance-manifest.json", "capture-events.json"):
            self.assertIn(name, PINS)
            self.assertIn(name, g.CONFIG)


class OutputTests(unittest.TestCase):
    def test_thomas_voiced_film_rejected(self):
        # Images du brouillon témoin copiées sans réencodage, narration Thomas à la place de Kokoro.
        with tempfile.TemporaryDirectory() as t:
            thomas = Path(t) / "thomas.mp4"
            subprocess.run(
                [
                    "ffmpeg",
                    "-v",
                    "error",
                    "-i",
                    str(D / "media/form-kokoro-pointeur-draft.mp4"),
                    "-i",
                    str(THOMAS_PILOT / "media/form-guarded.mp4"),
                    "-map",
                    "0:v:0",
                    "-map",
                    "1:a:0",
                    "-c",
                    "copy",
                    str(thomas),
                ],
                check=True,
            )
            with self.assertRaisesRegex(ValueError, "kokoro_output_audio_changed"):
                g.validate_output(thomas)

    def test_reencoded_video_with_kokoro_audio_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            altered = Path(t) / "altered.mp4"
            subprocess.run(
                [
                    "ffmpeg",
                    "-v",
                    "error",
                    "-i",
                    str(D / "media/form-kokoro-pointeur-draft.mp4"),
                    "-vf",
                    "hue=s=0",
                    "-c:v",
                    "libx264",
                    "-preset",
                    "ultrafast",
                    "-pix_fmt",
                    "yuv420p",
                    "-c:a",
                    "copy",
                    str(altered),
                ],
                check=True,
            )
            with self.assertRaisesRegex(ValueError, "kokoro_output_video_changed"):
                g.validate_output(altered)

    def test_short_silent_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            short = Path(t) / "short.mp4"
            subprocess.run(
                [
                    "ffmpeg",
                    "-v",
                    "error",
                    "-f",
                    "lavfi",
                    "-i",
                    "color=s=64x64:r=10:d=0.5",
                    "-c:v",
                    "libx264",
                    "-pix_fmt",
                    "yuv420p",
                    str(short),
                ],
                check=True,
            )
            with self.assertRaisesRegex(ValueError, "kokoro_output_duration_invalid"):
                g.validate_output(short)

    def test_witness_draft_accepted(self):
        self.assertTrue(g.validate_output(D / "media/form-kokoro-pointeur-draft.mp4"))


class PrepareTests(unittest.TestCase):
    def test_nominal_preparation_reproduces_pinned_inputs(self):
        with tempfile.TemporaryDirectory() as t:
            target = Path(t)
            p.prepare(target=target)
            for name, _, _ in p.RECIPE:
                self.assertEqual(g.sha(target / name), PINS[name], name)

    def test_altered_source_rejected_without_deposit(self):
        with tempfile.TemporaryDirectory() as t:
            sources = Path(t) / "sources"
            target = Path(t) / "target"
            (sources / "media").mkdir(parents=True)
            target.mkdir()
            for src in p.SOURCE_PINS:
                (sources / src).write_bytes((THOMAS_PILOT / src).read_bytes())
            (sources / "media/kokoro-fast1.wav").write_bytes(b"altered")
            with self.assertRaisesRegex(
                ValueError, "kokoro_source_changed:media/kokoro-fast1.wav"
            ):
                p.prepare(sources=sources, target=target)
            self.assertEqual(list(target.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
