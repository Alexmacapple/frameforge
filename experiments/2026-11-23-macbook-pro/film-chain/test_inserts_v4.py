"""Insert animé en fin de film (version 4 de la fiche, suite du ticket 59).

Une scène « insert » a sa voix et ses sous-titres, mais aucun geste filmé : elle montre une
sous-composition HyperFrames figée par empreinte. Au plus une par film, après toutes les scènes
filmées ; la capture s'arrête quand elle commence. Le film des fenêtres modales sert de base.
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
film_guard = importlib.import_module("film_guard")
FILM = CHAIN.parent / "ff47-film-fenetres-modales"
FICHE = json.loads((FILM / "provenance-manifest.json").read_text())
GENERATED = {"index.html", "captions.srt", "captions.vtt", "transcript.txt"}
INSERT_REF = "compositions/recapitulatif.html"
INSERT_HTML = (
    '<!doctype html><html lang="fr"><body><div id="insert-root" '
    'data-composition-id="insert" data-start="0" data-duration="13"></div></body></html>\n'
)
START, END_FILM = 53.175, 67


def recap_scene(**change):
    scene = {
        "scene_id": "recapitulatif",
        "shot_type": "insert",
        "insert_ref": INSERT_REF,
        "gesture_events": [],
        "result": {"event": None, "observed_key": None, "expected": None},
        "narration": {
            "text": "À l'ouverture, le focus entre dans la fenêtre. Échap le rend.",
            "audio_ref": "voice1.wav",
            "start_s": START,
            "duration_s": 10.8,
        },
        "caption": {"start_s": START, "end_s": 64.275},
        "evidence_status": "reasoned",
    }
    scene.update(change)
    return scene


def v4_fiche():
    data = json.loads(json.dumps(FICHE))
    data["manifest_version"] = 4
    data["film"]["duration_s"] = END_FILM
    data["scenes"].append(recap_scene())
    return data


class V4Film(unittest.TestCase):
    """Fichiers générés depuis la fiche du film 47 passée en version 4, avec un insert final."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for path in FILM.iterdir():
            if path.is_file() and path.name not in GENERATED | {
                "provenance-manifest.json"
            }:
                (self.root / path.name).symlink_to(path)
        (self.root / "compositions").mkdir()
        (self.root / INSERT_REF).write_text(INSERT_HTML)
        self.fiche = v4_fiche()
        self.write()

    def write(self):
        for name, text in b.render(self.fiche).items():
            (self.root / name).write_text(text)

    def details(self, fiche=None):
        return {
            r["check"]: (r["status"], r["detail"])
            for r in m.check_data(fiche or self.fiche, self.root)
        }

    def expect(self, check, needle, change):
        fiche = v4_fiche()
        change(fiche)
        got = self.details(fiche)
        self.assertEqual(got[check][0], "FAIL", got[check])
        self.assertIn(needle, got[check][1])

    def test_film_v4_passe_ses_controles(self):
        got = self.details()
        for check in (
            "schema",
            "texts",
            "captions",
            "composition",
            "timeline",
            "inserts",
            "gestures",
            "statuses",
        ):
            self.assertEqual(got[check][0], "PASS", (check, got[check][1]))

    def test_la_capture_s_arrete_quand_l_insert_commence(self):
        page = (self.root / "index.html").read_text()
        self.assertIn(f'data-duration="{b.number(START)}" data-track-index="0"', page)
        self.assertIn(
            f'data-composition-id="insert" data-composition-src="{INSERT_REF}" '
            f'data-start="{b.number(START)}" data-duration="{b.number(END_FILM - START)}"',
            page,
        )

    def test_insert_refuse_avant_la_version_4(self):
        fiche = v4_fiche()
        fiche["manifest_version"] = 3
        got = self.details(fiche)
        self.assertEqual(got["schema"][0], "FAIL")
        self.assertIn("insert", got["schema"][1])

    def test_insert_avant_une_scene_filmee(self):
        def move(d):
            d["scenes"].insert(0, d["scenes"].pop())

        self.expect("inserts", "après toutes les scènes filmées", move)

    def test_insert_avec_un_geste(self):
        self.expect(
            "inserts",
            "ni geste ni résultat",
            lambda d: d["scenes"][-1].update(gesture_events=["open_good"]),
        )

    def test_insert_dit_observe(self):
        self.expect(
            "inserts",
            "reasoned",
            lambda d: d["scenes"][-1].update(evidence_status="observed"),
        )

    def test_deux_inserts(self):
        self.expect(
            "inserts",
            "un seul insert",
            lambda d: d["scenes"].append(recap_scene(scene_id="encore")),
        )

    def test_fichier_d_insert_absent(self):
        (self.root / INSERT_REF).unlink()
        got = self.details()
        self.assertEqual(got["inserts"][0], "FAIL")
        self.assertIn(INSERT_REF, got["inserts"][1])

    def test_fichier_d_insert_sans_l_identifiant_attendu(self):
        (self.root / INSERT_REF).write_text(INSERT_HTML.replace('"insert"', '"autre"'))
        got = self.details()
        self.assertEqual(got["inserts"][0], "FAIL")
        self.assertIn('data-composition-id="insert"', got["inserts"][1])

    def test_composition_sans_l_insert_est_refusee(self):
        fiche = v4_fiche()
        fiche["scenes"].pop()
        fiche["manifest_version"] = 3
        (self.root / "index.html").write_text(b.composition(fiche))
        self.assertEqual(self.details()["composition"][0], "FAIL")

    def test_capture_qui_deborde_sur_l_insert_est_refusee(self):
        page = self.root / "index.html"
        page.write_text(
            page.read_text().replace(
                f'data-duration="{b.number(START)}" data-track-index="0"',
                f'data-duration="{END_FILM}" data-track-index="0"',
            )
        )
        got = self.details()
        self.assertEqual(got["composition"][0], "FAIL")

    def test_insert_decale_dans_la_composition_est_refuse(self):
        # Seul l'insert change : la capture garde sa durée, l'écart ne vient que de lui.
        page = self.root / "index.html"
        page.write_text(
            page.read_text().replace(
                f'data-composition-src="{INSERT_REF}" data-start="{b.number(START)}"',
                f'data-composition-src="{INSERT_REF}" data-start="{b.number(START + 1)}"',
            )
        )
        got = self.details()
        self.assertEqual(got["composition"][0], "FAIL")
        self.assertIn("insert de la composition", got["composition"][1])

    def test_fichier_d_insert_hors_du_dossier(self):
        self.expect(
            "schema",
            "hors du dossier du film",
            lambda d: d["scenes"][-1].update(insert_ref="../ailleurs/recap.html"),
        )

    def test_l_insert_doit_etre_fige(self):
        got = self.details()
        self.assertIn(INSERT_REF, got["pinned_media"][1])

    def test_scene_filmee_non_observee_toujours_refusee(self):
        self.expect(
            "statuses",
            "non observée",
            lambda d: d["scenes"][0].update(evidence_status="reasoned"),
        )


class GuardMedia(unittest.TestCase):
    def guard(self, media):
        return film_guard.FilmGuard(
            root=FILM,
            prefix="film",
            media=media,
            config=(),
            pins_ref=FICHE["pins_ref"],
            reference_ref="output-reference.json",
            output=FICHE["film"]["output_ref"],
            pins=("0" * 64,) * 3,
        )

    def test_le_garde_compte_l_insert_parmi_les_medias(self):
        cited = ["capture.mp4", *[f"voice{i}.wav" for i in range(1, 8)]]
        fiche = v4_fiche()
        self.assertEqual(self.guard(cited).differs_from_fiche(fiche), ["media"])
        self.assertEqual(self.guard([*cited, INSERT_REF]).differs_from_fiche(fiche), [])


if __name__ == "__main__":
    unittest.main()
