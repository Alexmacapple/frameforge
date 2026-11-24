"""Point d'entrée du garde : verdict, code de sortie et reçu de rendu, sans média ni rendu réel.

Né de la revue ShipGuard du 23 novembre 2026 : FilmGuard.main n'était exercé par aucun test, et
rien ne liait un film rendu aux entrées dont il sort. Le rendu lui-même est remplacé ici par une
fonction qui dépose un fichier ; ce qui est prouvé est ce que main fait autour.
"""

import contextlib
import importlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
film_guard = importlib.import_module("film_guard")
check = importlib.import_module("check_manifest")

REFERENCE = {key: 1 for key in film_guard.REFERENCE_KEYS}


class GuardCase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.pins = {"clip.wav": "a" * 64, "provenance-manifest.json": "b" * 64}
        (self.root / "pins.json").write_text(json.dumps(self.pins))
        (self.root / "reference.json").write_text(json.dumps(REFERENCE))
        self.guard = film_guard.FilmGuard(
            root=self.root,
            prefix="film",
            media=("clip.wav",),
            config=("index.html",),
            pins_ref="pins.json",
            reference_ref="reference.json",
            output="media/film.mp4",
            pins=("0" * 64,) * 3,
        )

    def run_main(self, render):
        out = io.StringIO()
        with (
            mock.patch.object(film_guard.wrapper, "run", side_effect=render),
            contextlib.redirect_stdout(out),
        ):
            code = self.guard.main(lambda *a: True, lambda *a: True)
        return code, json.loads(out.getvalue())

    def deposit(self, args, **kwargs):
        args.output.parent.mkdir(parents=True)
        args.output.write_bytes(b"film rendu")
        return {"status": "PASS", "output": str(args.output)}


class MainTests(GuardCase):
    def test_successful_render_reports_pass_and_writes_the_receipt(self):
        code, said = self.run_main(self.deposit)
        self.assertEqual((code, said["status"]), (0, "PASS"))
        receipt = json.loads(film_guard.receipt_path(self.guard.output).read_text())
        self.assertEqual(
            receipt,
            {
                "output_sha256": film_guard.sha(self.guard.output),
                "inputs_sha256": check.inputs_fingerprint(self.pins),
            },
        )

    def test_refused_render_reports_blocked_code_2_and_writes_no_receipt(self):
        refusals = (
            ValueError("film_asset_changed:clip.wav"),
            RuntimeError("render_processes_left: 4242"),
            KeyboardInterrupt("guarded render interrupted"),
            OSError("disque plein"),
            subprocess.TimeoutExpired(["ffmpeg"], 300),
            subprocess.CalledProcessError(1, ["ffmpeg"]),
        )
        for refusal in refusals:
            with self.subTest(refusal=type(refusal).__name__):
                code, said = self.run_main(mock.Mock(side_effect=refusal))
                self.assertEqual((code, said["status"]), (2, "BLOCKED_OR_INTERRUPTED"))
                self.assertFalse(self.guard.output.exists())
                self.assertFalse(film_guard.receipt_path(self.guard.output).exists())

    def test_unreadable_pins_file_is_a_refusal_not_a_traceback(self):
        (self.root / "pins.json").write_text("pas du json")
        code, said = self.run_main(self.deposit)
        self.assertEqual((code, said["status"]), (2, "BLOCKED_OR_INTERRUPTED"))
        self.assertFalse(self.guard.output.exists())


class UnreadableOutputTests(GuardCase):
    def probe(self, data):
        return mock.patch.object(
            film_guard.subprocess,
            "check_output",
            return_value=json.dumps(data).encode(),
        )

    def test_probe_without_the_expected_fields_is_a_named_refusal(self):
        shapes = (
            {},
            {"format": {}},
            {"format": {"duration": "1"}},
            {"format": {"duration": "1"}, "streams": [{}, {}]},
        )
        for shape in shapes:
            with (
                self.subTest(probe=shape),
                self.probe(shape),
                self.assertRaisesRegex(ValueError, "film_output_unreadable"),
            ):
                self.guard.validate_output(self.root / "film.mp4")


class ProbedShapeTests(GuardCase):
    """Chaque refus de forme, isolé : la sonde est fabriquée, un seul champ s'écarte du film attendu."""

    def setUp(self):
        super().setUp()
        (self.root / "reference.json").write_text(
            json.dumps({**REFERENCE, "expected_duration_s": 10, "expected_fps": 30})
        )

    def probe(self, **changes):
        video = {
            "codec_type": "video",
            "codec_name": "h264",
            "width": 1920,
            "height": 1080,
            "nb_frames": "300",
            "avg_frame_rate": "30/1",
            "sample_aspect_ratio": "1:1",
            "display_aspect_ratio": "16:9",
        }
        audio = {"codec_type": "audio", "codec_name": "aac", "duration": "10.0"}
        video.update(changes.get("video", {}))
        audio.update(changes.get("audio", {}))
        data = {
            "format": {"duration": changes.get("duration", "10.0")},
            "streams": [video, audio],
        }
        return mock.patch.object(
            film_guard.subprocess,
            "check_output",
            return_value=json.dumps(data).encode(),
        )

    def refused(self, reason, **changes):
        with (
            self.probe(**changes),
            self.assertRaisesRegex(ValueError, "film_" + reason + "$"),
        ):
            self.guard.validate_output(self.root / "film.mp4")

    def test_expected_shape_reaches_the_content_comparison(self):
        # Témoin : sans écart de forme, le refus vient de la comparaison des images, plus loin.
        with (
            self.probe(),
            mock.patch.object(film_guard, "video_stream_hash", return_value="autre"),
            self.assertRaisesRegex(ValueError, "film_output_video_changed$"),
        ):
            self.guard.validate_output(self.root / "film.mp4")

    def test_sound_shorter_than_the_film_is_refused(self):
        self.refused("output_audio_invalid", audio={"duration": "9.5"})

    def test_missing_frames_are_refused(self):
        self.refused("output_framerate_invalid", video={"nb_frames": "299"})

    def test_other_frame_rate_is_refused(self):
        self.refused(
            "output_framerate_invalid",
            video={"avg_frame_rate": "25/1", "nb_frames": "300"},
        )

    def test_other_duration_is_refused(self):
        self.refused("output_duration_invalid", duration="10.2")


if __name__ == "__main__":
    unittest.main()
