"""Mesure si les tests voient la suppression d'un contrôle.

Né de la contre-revue du 23 novembre 2026 (issue 15, constat 7) : huit contrôles sur quatorze
pouvaient disparaître sans qu'aucun test ne rougisse.

Le script copie les dossiers utiles dans un dossier temporaire, y neutralise un contrôle à la fois,
lance toutes les suites de tests et note les mutants que personne n'a vus. Rien n'est modifié dans
le dépôt. Durée : quelques minutes.

  python3 mutation_check.py            tous les mutants ; code 1 s'il reste un survivant non justifié
  python3 mutation_check.py --list     liste les mutants sans rien lancer

Un mutant survivant est un contrôle que l'on peut retirer sans qu'un test échoue : soit il manque
un test, soit le contrôle est redondant. Les redondances assumées sont listées dans ACCEPTED, avec
leur raison.
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHAIN = Path(__file__).resolve().parent
EXPERIMENTS = CHAIN.parent
COPIED = (
    "film-chain",
    "ff10-hyperframes-guarded-integration",
    "ff04-room-booking-film",
    "ff10-second-web-demo-transfer",
    "ff10-web-workflow-entrypoint",
)
SUITES = (
    (
        "film-chain",
        (
            "test_film_guard",
            "test_repin",
            "test_fiche_checks",
            "test_habillage_v2",
            "test_guard_main",
            "test_interruption",
        ),
    ),
    (
        "ff10-second-web-demo-transfer/form-pilot-kokoro",
        (
            "test_manifest",
            "test_build_from_fiche",
            "test_kokoro_guard",
            "test_gesture_alignment",
        ),
    ),
    ("ff04-room-booking-film", ("test_room_booking",)),
)
# Mutants que l'on accepte de voir survivre, avec la raison. Vide tant que rien n'est justifié.
ACCEPTED = {}


def mutants():
    """Rend (identifiant, fichier, ancien texte, nouveau texte, rang de l'occurrence)."""
    out = []
    guard = (CHAIN / "film_guard.py").read_text()
    for rank, match in enumerate(
        re.finditer(r'raise self\.refuse\(\s*"([a-z_:]+)', guard)
    ):
        out.append(
            (
                f"garde:{match.group(1)}#{rank}",
                "film_guard.py",
                "raise self.refuse(",
                "self.refuse(",
                rank,
            )
        )
    check = (CHAIN / "check_manifest.py").read_text()
    for rank, _ in enumerate(re.finditer(r"problems\.append\(", check)):
        line = (
            check[
                : [m.start() for m in re.finditer(r"problems\.append\(", check)][rank]
            ].count("\n")
            + 1
        )
        out.append(
            (
                f"fiche:append#{rank}@L{line}",
                "check_manifest.py",
                "problems.append(",
                "(lambda *_: None)(",
                rank,
            )
        )
    header = "    def verdict(check, problems):\n"
    for name in re.findall(r'verdict(?:_or_unverified)?\(\s*"(\w+)"', check):
        patch = header + f'        if check == "{name}":\n            problems = []\n'
        out.append((f"fiche:contrôle {name}", "check_manifest.py", header, patch, 0))
    return out


def apply(path, old, new, rank):
    text = path.read_text()
    starts = [m.start() for m in re.finditer(re.escape(old), text)]
    if rank >= len(starts):
        raise ValueError(f"occurrence {rank} de {old!r} introuvable dans {path.name}")
    at = starts[rank]
    path.write_text(text[:at] + new + text[at + len(old) :])


def suites_pass(root):
    """Vrai si toutes les suites passent ; s'arrête à la première qui échoue."""
    for folder, modules in SUITES:
        present = [m for m in modules if (root / folder / f"{m}.py").is_file()]
        done = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", *present],
            cwd=root / folder,
            check=False,
            capture_output=True,
            text=True,
        )
        if done.returncode != 0:
            return False
    return True


def main():
    todo = mutants()
    if "--list" in sys.argv[1:]:
        print("\n".join(m[0] for m in todo))
        return 0
    with tempfile.TemporaryDirectory(prefix="frameforge-mutation-") as tmp:
        root = Path(tmp)
        for name in COPIED:
            shutil.copytree(
                EXPERIMENTS / name,
                root / name,
                ignore=shutil.ignore_patterns("__pycache__", ".ruff_cache", "*.webm"),
            )
        if not suites_pass(root):
            print(
                json.dumps(
                    {
                        "status": "BLOCKED",
                        "reason": "les tests échouent déjà sans mutation",
                    },
                    ensure_ascii=False,
                )
            )
            return 2
        survivors = []
        for ident, name, old, new, rank in todo:
            target = root / "film-chain" / name
            original = target.read_text()
            apply(target, old, new, rank)
            killed = not suites_pass(root)
            target.write_text(original)
            print(("tué       " if killed else "SURVIVANT ") + ident, flush=True)
            if not killed:
                survivors.append(ident)
    unjustified = [s for s in survivors if s not in ACCEPTED]
    print(
        json.dumps(
            {
                "mutants": len(todo),
                "survivants": survivors,
                "non_justifiés": unjustified,
                "status": "FAIL" if unjustified else "PASS",
            },
            ensure_ascii=False,
        )
    )
    return 1 if unjustified else 0


if __name__ == "__main__":
    sys.exit(main())
