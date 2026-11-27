"""Contrôle de la composition avant le brouillon témoin (issue 70).

HyperFrames 0.8.33 sait vérifier une composition sans la rendre : erreurs de lint et d'exécution,
texte qui déborde, contraste des textes. Essais du 27 novembre 2026 sur le film 47, sur les deux
Mac : des sous-titres illisibles sont vus, mais la commande répond quand même « ok » et sort en
code 0 ; et une erreur de lint laisse les passes suivantes vides et vertes. Le verdict se lit donc
dans les compteurs du rapport, jamais dans « ok » ni dans le code de sortie.
"""

import importlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
composition = importlib.import_module("composition_check")
witness = importlib.import_module("witness_reference")
wrapper = composition.wrapper
FILM = CHAIN.parent / "ff47-film-fenetres-modales"
RENDER_INPUTS = (
    "index.html",
    "hyperframes.json",
    "package.json",
    "capture.mp4",
) + tuple(f"voice{n}.wav" for n in range(1, 8))
HAS_INPUTS = all((FILM / name).is_file() for name in RENDER_INPUTS)


def hyperframes_cached():
    """HyperFrames 0.8.33 est-il dans le cache npm ? Sans lui, rien ne tourne hors réseau."""
    npx = shutil.which("npx")
    if npx is None or shutil.which("sandbox-exec") is None:
        return False
    out = subprocess.run(
        [npx, "--offline", "hyperframes@0.8.33", "--version"],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return out.returncode == 0 and out.stdout.strip() == "0.8.33"


def report(**changes):
    """Rapport d'un film sain, tel que mesuré sur le film 47, puis modifié clé par clé."""
    base = {
        "ok": True,
        "lint": {
            "errorCount": 0,
            "warningCount": 1,
            "findings": [{"code": "timeline_track_too_dense", "severity": "warning"}],
        },
        "runtime": {"errorCount": 0, "findings": []},
        "layout": {"samples": [3, 9, 15, 21, 27, 33, 39, 45, 51], "totalIssueCount": 0},
        "contrast": {"enabled": True, "checked": 4, "passed": 4},
    }
    for path, value in changes.items():
        section, key = path.split("__")
        base[section][key] = value
    return base


class Verdict(unittest.TestCase):
    def test_film_sain_accepte_malgre_un_avertissement_de_lint(self):
        self.assertEqual(composition.failures(report()), [])

    def test_texte_illisible_refuse_meme_si_le_rapport_dit_ok(self):
        seen = composition.failures(report(contrast__passed=0))
        self.assertEqual(seen, ["contrast_failed:0/4"])

    def test_un_seul_texte_illisible_suffit(self):
        self.assertEqual(
            composition.failures(report(contrast__passed=3)), ["contrast_failed:3/4"]
        )

    def test_contraste_non_mesure_refuse(self):
        self.assertEqual(
            composition.failures(report(contrast__checked=0, contrast__passed=0)),
            ["contrast_not_measured"],
        )

    def test_contraste_desactive_refuse(self):
        self.assertEqual(
            composition.failures(report(contrast__enabled=False)),
            ["contrast_not_measured"],
        )

    def test_mise_en_page_non_mesuree_refusee(self):
        self.assertEqual(
            composition.failures(report(layout__samples=[])), ["layout_not_measured"]
        )

    def test_texte_qui_deborde_refuse(self):
        self.assertEqual(
            composition.failures(report(layout__totalIssueCount=2)),
            ["layout_overflow:2"],
        )

    def test_erreur_de_lint_refusee_avec_son_code(self):
        seen = composition.failures(
            report(
                lint__errorCount=1,
                lint__findings=[
                    {"code": "timeline_track_too_dense", "severity": "warning"},
                    {"code": "multiple_root_compositions", "severity": "error"},
                ],
            )
        )
        self.assertEqual(seen, ["lint_error:multiple_root_compositions"])

    def test_erreur_d_execution_refusee(self):
        self.assertEqual(
            composition.failures(report(runtime__errorCount=1)), ["runtime_errors:1"]
        )

    def test_plusieurs_motifs_sont_tous_rendus(self):
        seen = composition.failures(
            report(layout__samples=[], contrast__checked=0, contrast__passed=0)
        )
        self.assertEqual(seen, ["layout_not_measured", "contrast_not_measured"])

    def test_rapport_illisible_refuse(self):
        for broken in ({}, {"ok": True}, [], None, report(contrast__checked="4")):
            with self.subTest(broken=broken):
                self.assertEqual(composition.failures(broken), ["report_unreadable"])


class Command(unittest.TestCase):
    def test_meme_bac_a_sable_et_meme_version_que_le_rendu(self):
        render = wrapper.render_command(Path("/projet"), Path("/sortie.mp4"))
        cmd = composition.check_command(Path("/projet"))
        cut = render.index("render")
        self.assertEqual(cmd[:cut], render[:cut])
        self.assertEqual(cmd[cut:], ["check", "--json", "/projet"])

    def test_sans_bac_a_sable_le_controle_est_refuse(self):
        with (
            mock.patch.object(wrapper.shutil, "which", return_value=None),
            self.assertRaisesRegex(ValueError, "no_network_sandbox"),
        ):
            composition.check_command(Path("/projet"))

    def test_sortie_qui_n_est_pas_du_json_refusee(self):
        done = subprocess.CompletedProcess([], 0, stdout="pas du json", stderr="")
        with mock.patch.object(composition.subprocess, "run", return_value=done):
            self.assertEqual(composition.run(Path("/projet")), ["report_unreadable"])

    def test_le_code_de_sortie_ne_fait_pas_le_verdict(self):
        # Code 0 et « ok » avec des sous-titres illisibles : cas mesuré le 27 novembre 2026.
        bad = subprocess.CompletedProcess(
            [], 0, stdout=json.dumps(report(contrast__passed=0)), stderr=""
        )
        with mock.patch.object(composition.subprocess, "run", return_value=bad):
            self.assertEqual(composition.run(Path("/projet")), ["contrast_failed:0/4"])
        # Code 1 pour un film sain : c'est ce que donne --strict, que la chaîne n'utilise pas.
        good = subprocess.CompletedProcess(
            [], 1, stdout=json.dumps(report()), stderr=""
        )
        with mock.patch.object(composition.subprocess, "run", return_value=good):
            self.assertEqual(composition.run(Path("/projet")), [])


class Witness(unittest.TestCase):
    """Le témoin n'est pas rendu si la composition est refusée."""

    def film(self):
        root = Path(tempfile.mkdtemp(prefix="ff70-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        (root / "index.html").write_text("<html></html>")
        guard = SimpleNamespace(
            config=("index.html",), media=(), output=Path("media/essai.mp4")
        )
        return root, guard

    def test_composition_refusee_aucun_rendu_aucun_temoin(self):
        root, guard = self.film()
        with (
            mock.patch.object(witness, "load_guard", return_value=guard),
            mock.patch.object(
                witness.composition_check, "run", return_value=["contrast_failed:0/4"]
            ),
            mock.patch.object(witness.subprocess, "run") as render,
            self.assertRaisesRegex(ValueError, "contrast_failed:0/4"),
        ):
            witness.render_witness(root)
        render.assert_not_called()
        self.assertFalse((root / "media/essai-draft.mp4").exists())

    def test_composition_acceptee_le_temoin_est_rendu(self):
        root, guard = self.film()
        seen = []

        def fake_render(cmd, **_):
            Path(cmd[-3].removeprefix("--output=")).write_bytes(b"film")
            return subprocess.CompletedProcess(cmd, 0)

        def fake_check(work):
            seen.append(sorted(p.name for p in Path(work).iterdir()))
            return []

        with (
            mock.patch.object(witness, "load_guard", return_value=guard),
            mock.patch.object(witness.composition_check, "run", side_effect=fake_check),
            mock.patch.object(witness.subprocess, "run", side_effect=fake_render),
        ):
            target = witness.render_witness(root)
        # Le contrôle a porté sur la copie isolée : les seules entrées du garde.
        self.assertEqual(seen, [["index.html"]])
        self.assertEqual(target.read_bytes(), b"film")


@unittest.skipUnless(HAS_INPUTS, "entrées de rendu du film 47 absentes en local")
@unittest.skipUnless(hyperframes_cached(), "HyperFrames 0.8.33 absent du cache npm")
class RealComposition(unittest.TestCase):
    """Le vrai HyperFrames, sans réseau, sur des copies du film 47. Aucun rendu."""

    def copy(self):
        root = Path(tempfile.mkdtemp(prefix="ff70-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        work = root / "project"
        work.mkdir()
        for name in RENDER_INPUTS:
            shutil.copyfile(FILM / name, work / name)
        return work

    def test_film_47_accepte(self):
        self.assertEqual(composition.run(self.copy()), [])

    def test_sous_titres_illisibles_refuses(self):
        work = self.copy()
        html = (work / "index.html").read_text()
        self.assertIn("color:#fff;", html)
        (work / "index.html").write_text(html.replace("color:#fff;", "color:#333;"))
        self.assertEqual(composition.run(work), ["contrast_failed:0/4"])

    def test_seconde_composition_a_la_racine_refusee(self):
        # Avec baseline.html à côté d'index.html, HyperFrames ne mesure plus ni mise en page ni
        # contraste : le contrôle doit porter sur la copie isolée, pas sur le dossier du film.
        work = self.copy()
        shutil.copyfile(FILM / "baseline.html", work / "baseline.html")
        self.assertEqual(
            composition.run(work),
            [
                "lint_error:multiple_root_compositions",
                "layout_not_measured",
                "contrast_not_measured",
            ],
        )


if __name__ == "__main__":
    unittest.main()
