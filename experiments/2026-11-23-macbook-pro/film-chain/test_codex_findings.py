"""Constats de la revue indépendante de Codex du 24 novembre 2026 (issue 15), un test par constat.

Les constats 2 (capture hors du film) et 4 (paramètres d'un autre appel que GUARD) sont testés avec
leurs outils, dans test_capture_lib.py et test_repin.py.
"""

import ast
import contextlib
import importlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
b = importlib.import_module("build_from_fiche")
mutation_check = importlib.import_module("mutation_check")
FilmCopy = importlib.import_module("test_review_findings").FilmCopy


class GenerationWriteTests(FilmCopy):
    """Constat 1 : le générateur écrasait une entrée ou écrivait hors du film."""

    def generate(self, data):
        (self.root / "provenance-manifest.json").write_text(json.dumps(data))
        out = io.StringIO()
        argv = ["outil", str(self.root / "provenance-manifest.json")]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(out):
            return b.main(), out.getvalue()

    def test_other_spelling_of_an_input_name_is_refused(self):
        source = self.fiche()["source"]["ref"]
        for name in (
            "./" + source,
            source.capitalize(),
            "sous//" + source,
            source + "/",
        ):
            data = self.fiche()
            data["film"]["composition_ref"] = name
            with (
                self.subTest(name=name),
                self.assertRaisesRegex(ValueError, "nom de fichier généré refusé"),
            ):
                b.render(data)

    def test_two_generated_files_cannot_share_a_name(self):
        data = self.fiche()
        data["film"]["transcript_ref"] = "./" + data["film"]["composition_ref"]
        with self.assertRaisesRegex(ValueError, "nom de fichier généré refusé"):
            b.render(data)

    def test_generation_writes_nothing_through_a_link(self):
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        kept = Path(outside.name) / "note.txt"
        kept.write_text("à conserver")
        transcript = self.root / self.fiche()["film"]["transcript_ref"]
        transcript.unlink()
        transcript.symlink_to(kept)
        code, said = self.generate(self.fiche())
        self.assertEqual(code, 2, said)
        self.assertIn("lien", json.loads(said)["reason"])
        self.assertEqual(kept.read_text(), "à conserver")

    def test_generation_writes_nothing_through_a_linked_folder(self):
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        (self.root / "sorties").symlink_to(outside.name, target_is_directory=True)
        data = self.fiche()
        data["film"]["transcript_ref"] = "sorties/transcript.txt"
        code, said = self.generate(data)
        self.assertEqual(code, 2, said)
        self.assertIn("lien", json.loads(said)["reason"])
        self.assertEqual(os.listdir(outside.name), [])

    def test_stale_generated_file_is_still_rewritten(self):
        # Cas ordinaire : un fichier généré périmé, sans lien, est remis à jour.
        transcript = self.root / self.fiche()["film"]["transcript_ref"]
        wanted = transcript.read_bytes()
        transcript.write_text("périmé")
        code, said = self.generate(self.fiche())
        self.assertEqual(code, 0, said)
        self.assertEqual(transcript.read_bytes(), wanted)


class EscapedReferenceTests(FilmCopy):
    """Constat 6 : un nom de fichier contenant « & » était refusé à tort."""

    def test_composition_written_by_the_generator_is_accepted(self):
        def change(d):
            d["capture"]["media_ref"] = "capture&demo.mp4"
            d["scenes"][0]["narration"]["audio_ref"] = "voice&1.wav"

        data = self.fiche()
        change(data)
        for name, text in b.render(data).items():
            (self.root / name).write_text(text)
        got = self.details(change)["composition"]
        self.assertEqual(got[0], "PASS", got)

    def test_another_capture_name_is_still_refused(self):
        self.expect(
            "composition",
            "la composition ne montre pas la seule capture de la fiche",
            lambda d: d["capture"].update(media_ref="capture&demo.mp4"),
        )


class MutantTests(unittest.TestCase):
    """Constat 5 : un mutant qui ne se compile pas ne prouve aucune couverture."""

    def test_every_mutant_is_valid_python(self):
        with tempfile.TemporaryDirectory() as tmp:
            for ident, name, old, new, rank in mutation_check.mutants():
                target = Path(tmp) / name
                target.write_bytes((CHAIN / name).read_bytes())
                mutation_check.apply(target, old, new, rank)
                with self.subTest(mutant=ident):
                    ast.parse(target.read_text())
                    self.assertNotEqual(
                        target.read_text(),
                        (CHAIN / name).read_text(),
                        "rien n'a changé",
                    )

    def test_a_mutant_that_does_not_compile_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "outil.py"
            target.write_text("def f():\n    return (1)\n")
            with self.assertRaisesRegex(ValueError, "mutant illisible"):
                mutation_check.apply(target, "return (1)", "return (1", 0)


if __name__ == "__main__":
    unittest.main()
