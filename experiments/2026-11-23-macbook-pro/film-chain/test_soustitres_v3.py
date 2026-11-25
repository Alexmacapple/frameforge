"""Sous-titres découpés (version 3 de la fiche) et planche d'images (ticket 60).

Le film des fenêtres modales sert de témoin : en version 2, ses sous-titres vont jusqu'à
136 caractères ; la même fiche passée en version 3 doit donner des sous-titres de deux lignes
au plus, sans changer un octet des films déjà rendus en version 1 ou 2.
"""

import importlib
import itertools
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
m = importlib.import_module("check_manifest")
b = importlib.import_module("build_from_fiche")
FILM = CHAIN.parent / "ff47-film-fenetres-modales"
FICHE = json.loads((FILM / "provenance-manifest.json").read_text())
GENERATED = {"index.html", "captions.srt", "captions.vtt", "transcript.txt"}
TEXT_CHECKS = ("schema", "texts", "captions", "composition", "timeline")


def v3_fiche():
    data = json.loads(json.dumps(FICHE))
    data["manifest_version"] = 3
    return data


def run(tool, *args):
    return subprocess.run(
        [sys.executable, "-B", str(CHAIN / tool), *map(str, args)],
        check=False,
        capture_output=True,
        text=True,
        timeout=300,
    )


class SplitRule(unittest.TestCase):
    def test_une_phrase_courte_reste_un_seul_sous_titre(self):
        self.assertEqual(b.split_caption("Le focus revient."), [["Le focus revient."]])

    def test_chaque_sous_titre_tient_en_deux_lignes(self):
        for scene in FICHE["scenes"]:
            text = scene["narration"]["text"]
            with self.subTest(scene=scene["scene_id"]):
                cues = b.split_caption(text)
                self.assertGreater(len(cues), 1)
                for lines in cues:
                    self.assertTrue(1 <= len(lines) <= b.CUE_LINES, lines)
                    self.assertTrue(all(len(x) <= b.LINE_CHARS for x in lines), lines)
                # Rien n'est perdu ni ajouté : les mots se suivent comme dans la phrase.
                self.assertEqual(" ".join(" ".join(c) for c in cues), text)

    def test_les_coupures_tombent_sur_la_ponctuation(self):
        # Les phrases du film 47 tiennent toutes en deux lignes : aucune coupure entre deux mots
        # d'une même proposition, aucun reste isolé en fin de phrase.
        for scene in FICHE["scenes"]:
            with self.subTest(scene=scene["scene_id"]):
                for lines in b.split_caption(scene["narration"]["text"]):
                    self.assertIn(lines[-1][-1], ".,;:!?", lines)

    def test_une_phrase_trop_longue_se_coupe_a_la_virgule(self):
        text = (
            "Le focus entre dans la fenêtre et se pose sur le premier bouton, "
            "puis il revient au bouton qui a ouvert la fenêtre."
        )
        cues = b.split_caption(text)
        self.assertEqual(
            [" ".join(c) for c in cues],
            [
                "Le focus entre dans la fenêtre et se pose sur le premier bouton,",
                "puis il revient au bouton qui a ouvert la fenêtre.",
            ],
        )

    def test_un_mot_plus_long_qu_une_ligne_reste_entier(self):
        word = "a" * (b.LINE_CHARS + 5)
        cues = b.split_caption(f"Le mot {word} reste.")
        # Couper le mot le rendrait illisible : il occupe sa propre ligne, entier.
        self.assertIn(word, [line for c in cues for line in c])
        self.assertEqual(" ".join(" ".join(c) for c in cues), f"Le mot {word} reste.")


class Timing(unittest.TestCase):
    def test_les_sous_titres_d_une_phrase_couvrent_sa_fenetre_sans_trou(self):
        for scene, cues in zip(FICHE["scenes"], b.caption_cues(v3_fiche())):
            window = scene["caption"]
            with self.subTest(scene=scene["scene_id"]):
                self.assertEqual(cues[0][0], window["start_s"])
                self.assertEqual(cues[-1][1], window["end_s"])
                for before, after in itertools.pairwise(cues):
                    self.assertEqual(before[1], after[0])
                    self.assertLess(before[0], before[1])

    def test_version_2_garde_un_sous_titre_par_phrase(self):
        cues = b.caption_cues(FICHE)
        self.assertEqual([len(c) for c in cues], [1] * len(FICHE["scenes"]))
        # Le témoin : en version 2, ces sous-titres dépassent deux lignes.
        longest = max(len(c[0][2][0]) for c in cues)
        self.assertGreater(longest, b.LINE_CHARS * b.CUE_LINES)


class RenderedFilmsUnchanged(unittest.TestCase):
    def test_film_47_reste_identique(self):
        out = run("build_from_fiche.py", "--check", FILM / "provenance-manifest.json")
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)


class V3Film(unittest.TestCase):
    """Fichiers générés depuis la fiche du film 47 passée en version 3."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for path in FILM.iterdir():
            if path.is_file() and path.name not in GENERATED | {
                "provenance-manifest.json"
            }:
                (self.root / path.name).symlink_to(path)
        self.fiche = v3_fiche()
        for name, text in b.render(self.fiche).items():
            (self.root / name).write_text(text)

    def details(self):
        return {
            r["check"]: (r["status"], r["detail"])
            for r in m.check_data(self.fiche, self.root)
        }

    def test_film_v3_passe_les_controles_de_texte(self):
        got = self.details()
        for check in TEXT_CHECKS:
            self.assertEqual(got[check][0], "PASS", got[check][1])

    def test_srt_ecrit_les_deux_lignes(self):
        srt = (self.root / "captions.srt").read_text()
        cues = m.cues(srt)
        self.assertGreater(len(cues), len(self.fiche["scenes"]))
        for *_, said in cues:
            lines = said.split("\n")
            self.assertLessEqual(len(lines), b.CUE_LINES)
            self.assertTrue(all(len(x) <= b.LINE_CHARS for x in lines), said)

    def test_un_sous_titre_par_phrase_est_refuse_en_version_3(self):
        (self.root / "captions.srt").write_text(b.subtitles(FICHE, ",", numbered=True))
        self.assertEqual(self.details()["captions"][0], "FAIL")

    def test_incrustation_d_une_phrase_entiere_est_refusee(self):
        # La composition de la version 2 : même habillage, une phrase entière par sous-titre.
        (self.root / "index.html").write_text(b.composition(FICHE))
        self.assertEqual(self.details()["composition"][0], "FAIL")

    def test_texte_change_dans_un_morceau_est_refuse(self):
        vtt = self.root / "captions.vtt"
        vtt.write_text(vtt.read_text().replace("Tab", "Tabulation", 1))
        self.assertEqual(self.details()["texts"][0], "FAIL")


class ContactSheet(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.video = self.root / "essai.mp4"
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-f",
                "lavfi",
                "-i",
                "testsrc=size=640x360:rate=30:duration=6",
                "-pix_fmt",
                "yuv420p",
                str(self.video),
            ],
            check=True,
            timeout=60,
        )

    def size(self, path):
        out = subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "stream=width,height",
                "-of",
                "csv=p=0",
                str(path),
            ],
            text=True,
        )
        return tuple(map(int, out.strip().split(",")))

    def test_planche_de_douze_images_et_leurs_instants(self):
        out = run("contact_sheet.py", self.video)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        report = json.loads(out.stdout)
        sheet = Path(report["sheet"])
        self.assertEqual(sheet, (self.root / "essai-planche.png").resolve())
        # 4 colonnes de 480 px ; images en 16:9, donc 270 px de haut, 3 rangées.
        self.assertEqual(self.size(sheet), (4 * 480, 3 * 270))
        times = report["times_s"]
        self.assertEqual(len(times), 12)
        self.assertEqual(times, sorted(times))
        self.assertTrue(0 < times[0] and times[-1] < 6)

    def test_une_planche_existante_n_est_pas_ecrasee(self):
        sheet = self.root / "essai-planche.png"
        sheet.write_bytes(b"deja la")
        out = run("contact_sheet.py", self.video)
        self.assertEqual(out.returncode, 2)
        self.assertEqual(sheet.read_bytes(), b"deja la")

    def test_video_absente_refusee(self):
        out = run("contact_sheet.py", self.root / "absente.mp4")
        self.assertEqual(out.returncode, 2)
        self.assertEqual(json.loads(out.stdout)["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
