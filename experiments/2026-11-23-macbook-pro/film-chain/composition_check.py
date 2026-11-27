"""Contrôle la composition d'un film avant de rendre son brouillon témoin (issue 70).

Usage :
  python3 composition_check.py DOSSIER_DU_FILM

HyperFrames 0.8.33 (« check ») ouvre la composition sans la rendre et mesure : erreurs de lint et
d'exécution, texte qui déborde de son cadre, contraste des textes. Le contrôle porte sur une copie
des seules entrées que déclare render_guarded.py, dans le bac à sable sans réseau du garde.

Le verdict vient des compteurs du rapport, jamais de son « ok » ni du code de sortie. Mesures du
27 novembre 2026 sur le film 47, sur les deux Mac : des sous-titres illisibles donnent « ok » et un
code 0 ; une erreur de lint laisse la mise en page et le contraste non mesurés, et verts.

Limites : seul le texte de la composition est mesuré (titre, sous-titres), pas l'interface filmée ;
le seuil de contraste est celui de HyperFrames (3 pour 1) ; les textes sont relevés à quelques
instants du film, pas à chaque sous-titre. Un film accepté ici reste à regarder.
"""

import argparse
import importlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
wrapper = importlib.import_module("film_guard").wrapper
NO_TELEMETRY = {"HYPERFRAMES_NO_TELEMETRY": "1", "DO_NOT_TRACK": "1"}
TIMEOUT_S = 300


def check_command(work):
    """Commande de contrôle : même bac à sable et même HyperFrames que le rendu du garde."""
    render = wrapper.render_command(work, Path("unused.mp4"))
    return [*render[: render.index("render")], "check", "--json", str(work)]


def failures(report):
    """Motifs de refus lus dans le rapport de « hyperframes check » ; liste vide si rien à dire."""
    try:
        lint, runtime = report["lint"], report["runtime"]
        layout, contrast = report["layout"], report["contrast"]
        lint_errors = [f["code"] for f in lint["findings"] if f["severity"] == "error"]
        counts = (
            lint["errorCount"],
            runtime["errorCount"],
            len(layout["samples"]),
            layout["totalIssueCount"],
            contrast["checked"],
            contrast["passed"],
        )
        measured = contrast["enabled"] is True
    except (KeyError, TypeError):
        return ["report_unreadable"]
    if not all(type(n) is int and n >= 0 for n in counts):
        return ["report_unreadable"]
    lint_count, runtime_count, samples, overflow, checked, passed = counts
    out = [f"lint_error:{code}" for code in lint_errors]
    if lint_count and not lint_errors:
        out.append(f"lint_errors:{lint_count}")
    if runtime_count:
        out.append(f"runtime_errors:{runtime_count}")
    if samples == 0:
        out.append("layout_not_measured")
    elif overflow:
        out.append(f"layout_overflow:{overflow}")
    if not measured or checked == 0:
        out.append("contrast_not_measured")
    elif passed != checked:
        out.append(f"contrast_failed:{passed}/{checked}")
    return out


def run(work):
    """Contrôle la composition du dossier `work` ; rend les motifs de refus."""

    done = subprocess.run(
        check_command(work),
        check=False,
        capture_output=True,
        text=True,
        env=dict(os.environ, **NO_TELEMETRY),
        timeout=TIMEOUT_S,
    )
    try:
        report = json.loads(done.stdout)
    except ValueError:
        return ["report_unreadable"]
    return failures(report)


def main():
    parser = argparse.ArgumentParser(
        description="Contrôle de la composition d'un film, sans rendu."
    )
    parser.add_argument("film", type=Path)
    film = parser.parse_args().film.resolve()
    witness = importlib.import_module("witness_reference")
    try:
        guard = witness.load_guard(film)
        with tempfile.TemporaryDirectory(prefix="composition-") as temp:
            work = Path(temp) / "project"
            witness.snapshot(film, guard, work)
            reasons = run(work)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False))
        return 2
    status = "FAIL" if reasons else "PASS"
    print(json.dumps({"status": status, "reasons": reasons}, ensure_ascii=False))
    return 1 if reasons else 0


if __name__ == "__main__":
    sys.exit(main())
