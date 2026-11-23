"""Tests du générateur : la fiche de film est la seule source des fichiers texte du film."""

import copy
import hashlib
import importlib
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
sys.path.insert(0, str(D.parents[1] / "film-chain"))
b = importlib.import_module("build_from_fiche")
g = importlib.import_module("render_guarded")
FICHE = json.loads((D / "provenance-manifest.json").read_text())
# Empreintes des fichiers du film approuvé ab040730…7125, relevées avant l'écriture du générateur.
APPROVED = {
    "index.html": "4fd5bd62879513b88e538808f2b382fd99fe876f0351b698bd686c5ff84ee1ee",
    "captions.srt": "9124ff26239f36fe33b62f8686563516117cefcd4d5cef6cccf34ae95d0f4b6e",
    "captions.vtt": "8e78df3d0ea45d638f39dfad8c5b0e4bc9a705391c5484d57a31a5bedb6d7f98",
    "transcript.txt": "9d60690ff86471271494377da346c190025242652446a4fcffa14ff41f96da9a",
}


class BuildTests(unittest.TestCase):
    def test_generated_files_are_byte_identical_to_approved_ones(self):
        files = b.render(FICHE)
        self.assertEqual(sorted(files), sorted(APPROVED))
        for name, expected in APPROVED.items():
            self.assertEqual(
                hashlib.sha256(files[name].encode()).hexdigest(), expected, name
            )

    def test_files_on_disk_are_the_generated_ones(self):
        self.assertEqual(b.stale_files(FICHE, D), [])

    def test_changed_sentence_reaches_every_file(self):
        fiche = copy.deepcopy(FICHE)
        old = fiche["scenes"][0]["narration"]["text"]
        fiche["scenes"][0]["narration"]["text"] = "Le nom Dominique Petit est saisi."
        for name, text in b.render(fiche).items():
            self.assertIn("Le nom Dominique Petit est saisi.", text, name)
            self.assertNotIn(old, text, name)

    def test_changed_cue_reaches_subtitles_and_composition(self):
        fiche = copy.deepcopy(FICHE)
        fiche["scenes"][1]["narration"]["start_s"] = 5.5
        fiche["scenes"][1]["caption"] = {"start_s": 5.5, "end_s": 8.5}
        files = b.render(fiche)
        self.assertIn("00:00:05,500 --> 00:00:08,500", files["captions.srt"])
        self.assertIn("00:00:05.500 --> 00:00:08.500", files["captions.vtt"])
        self.assertIn('src="kokoro2.wav" data-start="5.5"', files["index.html"])
        self.assertIn(
            'id="caption2" class="clip" data-start="5.5" data-duration="3"',
            files["index.html"],
        )

    def test_markup_in_a_sentence_is_escaped(self):
        fiche = copy.deepcopy(FICHE)
        fiche["scenes"][0]["narration"]["text"] = "Saisir <b>A & B</b>."
        self.assertIn(
            "Saisir &lt;b&gt;A &amp; B&lt;/b&gt;.", b.render(fiche)["index.html"]
        )

    def test_render_refuses_files_not_generated_from_the_fiche(self):
        # Fiche jugée cohérente par ailleurs, mais fichiers présents différents de ce qu'elle génère.
        fiche = copy.deepcopy(FICHE)
        fiche["scenes"][0]["narration"]["text"] = "Le nom Dominique Petit est saisi."
        with (
            mock.patch.object(g, "load_fiche", return_value=fiche),
            mock.patch.object(g, "fiche_failures", return_value=[]),
        ):
            with self.assertRaisesRegex(
                ValueError, "kokoro_files_not_generated_from_fiche:.*index.html"
            ):
                g.preflight(D / "baseline.html", D / "index.html")


if __name__ == "__main__":
    unittest.main()
