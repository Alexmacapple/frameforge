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


if __name__ == "__main__":
    unittest.main()
