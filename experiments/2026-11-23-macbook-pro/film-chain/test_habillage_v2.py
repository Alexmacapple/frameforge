"""Habillage de la version 2 de la fiche : titre d'ouverture, cartouche, capture agrandie.

Né de la critique d'habillage du 23 novembre 2026. Deux garanties : une fiche en version 1 génère
exactement les mêmes fichiers qu'avant, et ce que la version 2 ajoute est contrôlé motif par motif.
Le film d'essai est fabriqué en mémoire à partir de la fiche du film de réservation.
"""

import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
m = importlib.import_module("check_manifest")
b = importlib.import_module("build_from_fiche")
SOURCE = CHAIN.parent / "ff04-room-booking-film"
V1_FILMS = (SOURCE, CHAIN.parent / "ff10-second-web-demo-transfer/form-pilot-kokoro")
TITLE = "Réserver une salle avec vidéoprojecteur"


def v2_fiche():
    data = json.loads((SOURCE / "provenance-manifest.json").read_text())
    data["manifest_version"] = 2
    data["film"].update(title=TITLE, capture_zoom=1.2)
    return data


class V2Film(unittest.TestCase):
    """Dossier temporaire : fichiers générés depuis une fiche v2, médias du film de réservation."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for path in SOURCE.iterdir():
            if path.is_file() and path.name != "provenance-manifest.json":
                (self.root / path.name).symlink_to(path)

    def details(self, change=None, files_change=None):
        data = v2_fiche()
        files = b.render(data)
        if files_change:
            files_change(files)
        for name, text in files.items():
            (self.root / name).unlink(missing_ok=True)
            (self.root / name).write_text(text)
        if change:
            change(data)
        return {
            r["check"]: (r["status"], r["detail"])
            for r in m.check_data(data, self.root)
            if r["check"] != "open_check"
        }

    def expect(self, check, text, change=None, files_change=None):
        status, detail = self.details(change, files_change)[check]
        self.assertEqual(status, "FAIL", detail)
        self.assertIn(text, detail)


class Version1Unchanged(unittest.TestCase):
    def test_v1_fiches_generate_the_committed_files(self):
        for root in V1_FILMS:
            with self.subTest(film=root.name):
                fiche = json.loads((root / "provenance-manifest.json").read_text())
                self.assertEqual(fiche["manifest_version"], 1)
                self.assertEqual(b.stale_files(fiche, root), [])


class Version2Render(unittest.TestCase):
    def setUp(self):
        self.v1 = b.render(
            json.loads((SOURCE / "provenance-manifest.json").read_text())
        )
        self.v2 = b.render(v2_fiche())

    def test_title_is_shown_before_the_first_caption(self):
        html = self.v2["index.html"]
        self.assertIn(
            '<div id="title" class="clip" data-start="0.2" data-duration="1.2"', html
        )
        self.assertIn(f">{TITLE}</div>", html)
        self.assertLess(html.index('id="title"'), html.index('id="caption1"'))

    def test_captions_are_a_cartouche_not_a_full_width_band(self):
        html = self.v2["index.html"]
        self.assertIn("border-radius:14px", html)
        self.assertNotIn("bottom:0;width:100%", html)

    def test_capture_is_enlarged_from_the_top_centre(self):
        self.assertIn("left:-10%;top:0;width:120%;height:120%", self.v2["index.html"])

    def test_zoom_of_one_leaves_the_capture_full_frame(self):
        data = v2_fiche()
        data["film"]["capture_zoom"] = 1
        self.assertIn(
            "left:0%;top:0;width:100%;height:100%", b.render(data)["index.html"]
        )

    def test_transcript_starts_with_the_title(self):
        self.assertEqual(
            self.v2["transcript.txt"], TITLE + "\n" + self.v1["transcript.txt"]
        )

    def test_subtitle_files_do_not_carry_the_title(self):
        for name in ("captions.srt", "captions.vtt"):
            self.assertEqual(self.v2[name], self.v1[name])


class Version2Checks(V2Film):
    def test_generated_v2_film_has_no_failure_on_text_checks(self):
        got = self.details()
        for check in ("schema", "texts", "captions", "composition", "timeline"):
            self.assertEqual(got[check][0], "PASS", got[check][1])

    def test_unknown_version(self):
        self.expect(
            "schema",
            "version de fiche inconnue",
            lambda d: d.update(manifest_version=5),
        )

    def test_v2_without_title(self):
        self.expect(
            "schema",
            "film : champs inattendus ou manquants ['title']",
            lambda d: d["film"].pop("title"),
        )

    def test_v1_with_title(self):
        self.expect(
            "schema",
            "film : champs inattendus ou manquants ['capture_zoom', 'title']",
            lambda d: d.update(manifest_version=1),
        )

    def test_empty_title(self):
        self.expect("schema", "titre vide", lambda d: d["film"].update(title="  "))

    def test_zoom_out_of_range(self):
        for value in (0.9, 1.6, "1.2", True):
            with self.subTest(zoom=value):
                self.expect(
                    "schema",
                    "agrandissement de la capture hors de 1 à 1,5",
                    lambda d, value=value: d["film"].update(capture_zoom=value),
                )

    def test_transcript_without_the_title(self):
        def change(files):
            files["transcript.txt"] = files["transcript.txt"].split("\n", 1)[1]

        self.expect("texts", "la transcription diffère", files_change=change)

    def test_embedded_title_differs_from_fiche(self):
        def change(files):
            files["index.html"] = files["index.html"].replace(
                f">{TITLE}<", ">Autre titre<"
            )

        self.expect(
            "composition", "titre incrusté différent de la fiche", files_change=change
        )

    def test_embedded_title_timing_differs_from_fiche(self):
        def change(files):
            files["index.html"] = files["index.html"].replace(
                'id="title" class="clip" data-start="0.2" data-duration="1.2"',
                'id="title" class="clip" data-start="0.2" data-duration="9"',
            )

        self.expect(
            "composition", "titre incrusté différent de la fiche", files_change=change
        )

    def test_title_with_markup_characters_is_accepted(self):
        def change(d):
            d["film"]["title"] = "Salle & option <vidéo>"

        data = v2_fiche()
        change(data)
        files = b.render(data)
        got = self.details(change, lambda f: f.update(files))
        self.assertEqual(
            (got["composition"][0], got["texts"][0]), ("PASS", "PASS"), got
        )

    def test_no_room_for_the_title(self):
        def change(d):
            d["scenes"][0]["narration"]["start_s"] = 0.5
            d["scenes"][0]["caption"]["start_s"] = 0.5

        self.expect(
            "timeline", "pas de place pour le titre avant le premier sous-titre", change
        )


if __name__ == "__main__":
    unittest.main()
