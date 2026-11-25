"""Outils de fabrication d'un film neuf (ticket 56, manques 1, 2 et 4 relevés sur le film 47).

- place_cues.py : pose les repères de la fiche depuis les durées mesurées des clips.
- witness_reference.py : écrit la référence de sortie depuis le brouillon témoin.
- check_manifest.py : un fichier d'empreintes absent donne un FAIL, pas une trace.

Le film des fenêtres modales sert de témoin : ses repères et sa référence ont été posés à la main
le 25 novembre 2026 ; les outils doivent redonner exactement les mêmes valeurs.
"""

import importlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
check = importlib.import_module("check_manifest")
FILM = CHAIN.parent / "ff47-film-fenetres-modales"
FICHE = json.loads((FILM / "provenance-manifest.json").read_text())
CLIPS = [s["narration"]["audio_ref"] for s in FICHE["scenes"]]
DRAFT = FILM / "media/fenetres-modales-draft.mp4"
HAS_CLIPS = all((FILM / c).is_file() for c in CLIPS)


def run(tool, *args):
    return subprocess.run(
        [sys.executable, "-B", str(CHAIN / tool), *map(str, args)],
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )


def draft_copy(root, keep_timings=False):
    """Copie de la fiche du film 47 remise en brouillon, repères effacés, avec ses clips."""
    fiche = json.loads(json.dumps(FICHE))
    fiche["film"]["output_sha256"] = None
    fiche["film"]["inputs_sha256"] = None
    fiche["film"]["approval"] = {"status": "DRAFT", "ref": None}
    if not keep_timings:
        fiche["film"]["duration_s"] = 1
        for s in fiche["scenes"]:
            s["narration"]["start_s"] = s["narration"]["duration_s"] = 0
            s["caption"]["start_s"] = s["caption"]["end_s"] = 0
    (root / "provenance-manifest.json").write_text(
        json.dumps(fiche, indent=2, ensure_ascii=False) + "\n"
    )
    for clip in CLIPS:
        if (FILM / clip).is_file():
            shutil.copyfile(FILM / clip, root / clip)
    return root / "provenance-manifest.json"


@unittest.skipUnless(HAS_CLIPS, "clips de voix du film 47 absents en local")
class PlaceCuesTests(unittest.TestCase):
    def test_redonne_les_reperes_poses_a_la_main(self):
        with tempfile.TemporaryDirectory() as t:
            path = draft_copy(Path(t))
            out = run(
                "place_cues.py",
                path,
                "--gap",
                "1.2",
                "--first",
                "1.8",
                "--tail",
                "2.5",
                "--pad",
                "0.3",
            )
            self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
            got = json.loads(path.read_text())
            self.assertEqual(got["film"]["duration_s"], FICHE["film"]["duration_s"])
            for mine, ref in zip(got["scenes"], FICHE["scenes"]):
                self.assertEqual(mine["narration"], ref["narration"], ref["scene_id"])
                self.assertEqual(mine["caption"], ref["caption"], ref["scene_id"])

    def test_ne_touche_que_les_reperes(self):
        with tempfile.TemporaryDirectory() as t:
            path = draft_copy(Path(t))
            before = json.loads(path.read_text())
            self.assertEqual(run("place_cues.py", path).returncode, 0)
            after = json.loads(path.read_text())
            for s in before["scenes"] + after["scenes"]:
                del s["narration"], s["caption"]
            del before["film"]["duration_s"], after["film"]["duration_s"]
            self.assertEqual(before, after)

    def test_refuse_la_fiche_d_un_film_deja_rendu(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            path = draft_copy(root, keep_timings=True)
            fiche = json.loads(path.read_text())
            fiche["film"]["output_sha256"] = FICHE["film"]["output_sha256"]
            path.write_text(json.dumps(fiche))
            before = path.read_bytes()
            out = run("place_cues.py", path)
            self.assertNotEqual(out.returncode, 0)
            self.assertEqual(path.read_bytes(), before)

    def test_refuse_un_clip_absent_sans_rien_ecrire(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            path = draft_copy(root)
            (root / CLIPS[3]).unlink()
            before = path.read_bytes()
            out = run("place_cues.py", path)
            self.assertNotEqual(out.returncode, 0)
            self.assertIn(CLIPS[3], out.stdout + out.stderr)
            self.assertEqual(path.read_bytes(), before)

    def test_refuse_un_premier_repere_sur_le_titre(self):
        with tempfile.TemporaryDirectory() as t:
            path = draft_copy(Path(t))
            before = path.read_bytes()
            out = run("place_cues.py", path, "--first", "1.0")
            self.assertNotEqual(out.returncode, 0)
            self.assertEqual(path.read_bytes(), before)


@unittest.skipUnless(DRAFT.is_file(), "brouillon témoin du film 47 absent en local")
class WitnessReferenceTests(unittest.TestCase):
    def test_redonne_la_reference_ecrite_a_la_main(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            draft_copy(root, keep_timings=True)
            out = run("witness_reference.py", root, "--from", DRAFT)
            self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
            self.assertEqual(
                json.loads((root / "output-reference.json").read_text()),
                json.loads((FILM / "output-reference.json").read_text()),
            )

    def test_refuse_un_film_deja_rendu(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            shutil.copyfile(
                FILM / "provenance-manifest.json", root / "provenance-manifest.json"
            )
            out = run("witness_reference.py", root, "--from", DRAFT)
            self.assertNotEqual(out.returncode, 0)
            self.assertFalse((root / "output-reference.json").exists())

    def test_refuse_un_temoin_de_duree_differente(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            path = draft_copy(root, keep_timings=True)
            fiche = json.loads(path.read_text())
            fiche["film"]["duration_s"] = 60
            path.write_text(json.dumps(fiche))
            out = run("witness_reference.py", root, "--from", DRAFT)
            self.assertNotEqual(out.returncode, 0)
            self.assertFalse((root / "output-reference.json").exists())


class MissingPinsTests(unittest.TestCase):
    def test_fichier_d_empreintes_absent_donne_un_fail(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            for name in (
                "modales.html",
                "transcript.txt",
                "captions.srt",
                "captions.vtt",
                "index.html",
                "capture-events.json",
            ):
                shutil.copyfile(FILM / name, root / name)
            fiche = json.loads(json.dumps(FICHE))
            results = check.check_data(fiche, root)
            states = {r["check"]: r["status"] for r in results}
            self.assertEqual(states["pinned_media"], "FAIL")
            self.assertEqual(check.exit_code(results), 1)


if __name__ == "__main__":
    unittest.main()
