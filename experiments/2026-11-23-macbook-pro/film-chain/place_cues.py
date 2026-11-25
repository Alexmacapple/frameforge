"""Pose les repères de la fiche d'un film depuis les durées mesurées de ses clips de voix.

Usage : python3 place_cues.py CHEMIN_DE_LA_FICHE [--first S] [--gap S] [--pad S] [--tail S]

Chaque phrase commence --gap secondes après la fin de la précédente, la première à --first ; son
sous-titre l'encadre et reste --pad secondes après elle ; le film dure jusqu'à --tail secondes après
la dernière phrase, arrondi à la seconde. Seuls narration.start_s, narration.duration_s,
caption.start_s, caption.end_s et film.duration_s sont écrits ; tout le reste de la fiche est gardé.

Refusé, sans rien écrire : une fiche qui porte déjà l'empreinte d'un film rendu (ses repères
décrivent ce film), un clip absent ou illisible, un premier repère qui tombe sur le titre d'ouverture
d'une fiche en version 2. Créé le 25 novembre 2026 depuis le script écrit à la main pour le film 47.
"""

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_from_fiche import TITLE_END
from check_manifest import is_ref

DEFAULTS = {"first": 1.8, "gap": 1.2, "pad": 0.3, "tail": 2.5}


def measured(clip):
    """Durée du clip au millième, lue par ffprobe comme le fait le contrôle de la fiche."""
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(clip),
        ],
        timeout=30,
    )
    return round(float(out), 3)


def place(fiche, root, first, gap, pad, tail):
    """Rend la fiche avec ses repères posés ; lève ValueError sans rien modifier en cas de refus."""
    film = fiche["film"]
    if film.get("output_sha256"):
        raise ValueError(
            "fiche d'un film déjà rendu : ses repères décrivent ce film, rien n'est écrit"
        )
    if fiche.get("manifest_version") == 2 and first < TITLE_END:
        raise ValueError(
            f"premier repère à {first} s, avant la fin du titre d'ouverture ({TITLE_END} s)"
        )
    if min(first, gap, pad, tail) < 0:
        raise ValueError("durée négative refusée")
    durations = []
    for scene in fiche["scenes"]:
        ref = scene["narration"]["audio_ref"]
        if not is_ref(ref) or not (root / ref).is_file():
            raise ValueError(f"clip absent ou hors du dossier du film : {ref}")
        try:
            durations.append(measured(root / ref))
        except (subprocess.SubprocessError, ValueError) as exc:
            raise ValueError(f"clip illisible par ffprobe : {ref}") from exc
    out = json.loads(json.dumps(fiche))
    t, last_end = first, 0.0
    for scene, d in zip(out["scenes"], durations):
        start = round(t, 3)
        scene["narration"]["start_s"], scene["narration"]["duration_s"] = start, d
        last_end = round(t + d + pad, 3)
        scene["caption"]["start_s"], scene["caption"]["end_s"] = start, last_end
        t += d + gap
    # Le film ne s'arrête jamais avant la fin du dernier sous-titre, même si l'arrondi le voudrait.
    out["film"]["duration_s"] = max(round(t - gap + tail), math.ceil(last_end))
    return out


def main():
    parser = argparse.ArgumentParser(
        description="Pose les repères de la fiche depuis les durées des clips."
    )
    parser.add_argument("fiche", type=Path)
    for name, value in DEFAULTS.items():
        parser.add_argument("--" + name, type=float, default=value)
    args = parser.parse_args()
    path = args.fiche.resolve()
    try:
        fiche = json.loads(path.read_text())
        placed = place(fiche, path.parent, args.first, args.gap, args.pad, args.tail)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False))
        return 2
    path.write_text(json.dumps(placed, indent=2, ensure_ascii=False) + "\n")
    scenes = [
        (s["scene_id"], s["narration"]["start_s"], s["narration"]["duration_s"])
        for s in placed["scenes"]
    ]
    print(
        json.dumps(
            {
                "status": "PASS",
                "duration_s": placed["film"]["duration_s"],
                "scenes": scenes,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
