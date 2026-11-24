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
import unicodedata
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


class SecondReviewGenerationTests(GenerationWriteTests):
    """Seconde revue de Codex (24 novembre 2026), constat 2 : fichiers encore écrasés."""

    def test_two_unicode_spellings_of_a_name_are_the_same_file(self):
        # « é » en un caractère dans la fiche, en deux dans le nom à générer : même fichier sur
        # un disque macOS.
        data = self.fiche()
        data["capture"]["events_ref"] = unicodedata.normalize("NFC", "relevé.txt")
        data["film"]["transcript_ref"] = unicodedata.normalize("NFD", "relevé.txt")
        with self.assertRaisesRegex(ValueError, "nom de fichier généré refusé"):
            b.render(data)

    def test_other_spelling_on_the_side_of_the_input_is_seen(self):
        data = self.fiche()
        data["source"]["ref"] = "./" + data["source"]["ref"]
        data["film"]["composition_ref"] = self.fiche()["source"]["ref"]
        with self.assertRaisesRegex(ValueError, "nom de fichier généré refusé"):
            b.render(data)

    def test_two_generated_files_differing_by_case_are_refused(self):
        data = self.fiche()
        data["film"]["transcript_ref"] = data["film"]["composition_ref"].capitalize()
        with self.assertRaisesRegex(ValueError, "nom de fichier généré refusé"):
            b.render(data)

    def kept(self, name, change, prepare=None):
        """La génération refuse d'écrire sur ce fichier, et il garde son contenu."""
        target = self.root / name
        target.write_text("à conserver")
        data = self.fiche()
        change(data)
        if prepare:
            prepare(data)
        code, said = self.generate(data)
        self.assertEqual(code, 2, said)
        self.assertIn("fichier du film à conserver", json.loads(said)["reason"])
        self.assertEqual(target.read_text(), "à conserver")

    def test_approval_document_is_not_overwritten(self):
        def change(d):
            d["film"]["approval"]["ref"] = "accord.txt"
            d["film"]["transcript_ref"] = "accord.txt"

        self.kept("accord.txt", change)

    def test_file_linked_to_the_approval_document_is_not_overwritten(self):
        # Lien physique : deux noms, un seul fichier.
        def link(data):
            transcript = self.root / data["film"]["transcript_ref"]
            transcript.unlink()
            os.link(self.root / data["film"]["approval"]["ref"], transcript)

        self.kept(self.fiche()["film"]["approval"]["ref"], lambda d: None, link)

    def test_fiche_given_under_another_name_is_not_overwritten(self):
        data = self.fiche()
        data["film"]["transcript_ref"] = "fiche.txt"
        (self.root / "fiche.txt").write_text(json.dumps(data))
        out = io.StringIO()
        argv = ["outil", str(self.root / "fiche.txt")]
        with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(out):
            code = b.main()
        self.assertEqual(code, 2, out.getvalue())
        self.assertEqual(json.loads((self.root / "fiche.txt").read_text()), data)


class SecondReviewCompositionTests(FilmCopy):
    """Constat 8 : une capture absente ou mal adressée passait le contrôle de composition."""

    def test_video_without_a_real_address_is_refused(self):
        page = self.root / "index.html"
        text = page.read_text()
        self.assertEqual(text.count(' src="capture.mp4"'), 1)
        page.write_text(text.replace(' src="capture.mp4"', ' data-src="capture.mp4"'))
        self.expect(
            "composition", "la composition ne montre pas la seule capture de la fiche"
        )

    def test_audio_without_a_real_address_is_refused(self):
        page = self.root / "index.html"
        text = page.read_text()
        self.assertEqual(text.count(' src="voice1.wav"'), 1)
        page.write_text(text.replace(' src="voice1.wav"', ' data-src="voice1.wav"'))
        self.expect("composition", "piste audio non reconnue dans la composition")

    def test_name_that_an_address_would_cut_is_refused_by_the_schema(self):
        # « capture#1.mp4 » écrit dans une page désigne le fichier « capture ».
        for name in ("capture#1.mp4", "capture?v=2.mp4"):
            with self.subTest(name=name):
                got = self.details(
                    lambda d, name=name: d["capture"].update(media_ref=name)
                )
                self.assertEqual(got["schema"][0], "FAIL", got["schema"])


class SecondReviewJournalTests(FilmCopy):
    """Constat 9 : un journal de capture absent ou vide court-circuitait le verdict."""

    def test_missing_or_broken_journal_is_a_failure_not_a_traceback(self):
        journal = self.root / "capture-events.json"
        for damage in (journal.unlink, lambda: journal.write_text("pas du json")):
            damage()
            got = self.details()
            with self.subTest(journal=journal.exists()):
                for check in ("gestures", "results", "statuses"):
                    self.assertEqual(got[check][0], "FAIL", got[check])
                self.assertIn(
                    "journal de capture absent ou illisible", got["results"][1]
                )

    def test_journal_without_observations_fails_the_statuses_of_a_reviewed_film(self):
        (self.root / "capture-events.json").write_text(
            json.dumps({"events": [], "observed": {}})
        )
        self.expect("statuses", "sans journal de capture lisible")


class SecondReviewMutantTests(unittest.TestCase):
    """Constat 11 : un mutant analysable mais non compilable, et un « raise (X) from exc »."""

    def mutate(self, source, old, new):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "outil.py"
            target.write_text(source)
            mutation_check.apply(target, old, new, 0)
            return target.read_text()

    def test_mutant_that_parses_but_does_not_compile_is_refused(self):
        with self.assertRaisesRegex(ValueError, "mutant illisible"):
            self.mutate("while True:\n    break\n", "while True", "if True")

    def test_parenthesised_raise_keeps_its_parentheses(self):
        source = "try:\n    pass\nexcept OSError as exc:\n    raise (ValueError(1)) from exc\n"
        self.assertEqual(
            self.mutate(source, "raise (ValueError(", "(ValueError("),
            "try:\n    pass\nexcept OSError as exc:\n    (ValueError(1))\n",
        )


if __name__ == "__main__":
    unittest.main()
