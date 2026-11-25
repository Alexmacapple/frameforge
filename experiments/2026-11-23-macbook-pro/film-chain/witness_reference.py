"""Rend le brouillon témoin d'un film et écrit sa référence de sortie (output-reference.json).

Usage :
  python3 witness_reference.py DOSSIER_DU_FILM                 rend le témoin, puis écrit la référence
  python3 witness_reference.py DOSSIER_DU_FILM --from TEMOIN   écrit la référence d'un témoin déjà rendu

Le témoin est rendu par la commande même du garde (HyperFrames 0.8.33, sans réseau), sur une copie des
entrées que déclare render_guarded.py, sous media/<film>-draft.mp4 ; un témoin existant n'est pas
écrasé. La télémétrie de HyperFrames est coupée pour ce rendu. La référence est mesurée avec les
fonctions mêmes du garde : empreintes du flux vidéo, du son et des paquets, étiquettes du conteneur.

Refusé, sans rien écrire : une fiche qui porte déjà l'empreinte d'un film rendu (sa référence fige
ce film), un témoin dont la durée ou la cadence diffère de la fiche. La référence décrit le témoin,
elle ne l'approuve pas : le regarder avant de refiger. Créé le 25 novembre 2026 depuis le script écrit
à la main pour le film 47.
"""

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
film_guard = importlib.import_module("film_guard")
FPS = 30
# Même commande que le garde : HyperFrames 0.8.33, mêmes options, sans réseau sortant.
render_command = film_guard.wrapper.render_command
NO_TELEMETRY = {"HYPERFRAMES_NO_TELEMETRY": "1", "DO_NOT_TRACK": "1"}


def load_guard(film):
    spec = importlib.util.spec_from_file_location(
        f"render_guarded_{abs(hash(str(film)))}", film / "render_guarded.py"
    )
    if (
        spec is None
        or spec.loader is None
        or not (film / "render_guarded.py").is_file()
    ):
        raise ValueError("garde du film introuvable : render_guarded.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.GUARD


def render_witness(film):
    guard = load_guard(film)
    target = film / "media" / (guard.output.stem + "-draft.mp4")
    if target.exists() or target.is_symlink():
        raise ValueError(f"témoin existant, non écrasé : {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".temoin-", dir=target.parent) as temp:
        work = Path(temp) / "project"
        work.mkdir()
        for name in (*guard.config, *guard.media):
            if (film / name).is_file():
                # Une entrée peut être rangée dans un sous-dossier (insert dans compositions/).
                (work / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(film / name, work / name)
        rendered = Path(temp) / "rendered.mp4"
        subprocess.run(
            render_command(work, rendered),
            check=True,
            stdout=subprocess.DEVNULL,
            env=dict(os.environ, **NO_TELEMETRY),
            timeout=1800,
        )
        os.link(rendered, target)
    return target


def reference(film, draft):
    fiche = json.loads((film / "provenance-manifest.json").read_text())
    if fiche["film"].get("output_sha256"):
        raise ValueError(
            "fiche d'un film déjà rendu : sa référence fige ce film, rien n'est écrit"
        )
    duration = fiche["film"]["duration_s"]
    probe = json.loads(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "format=duration:format_tags:stream=avg_frame_rate",
                "-of",
                "json",
                str(draft),
            ]
        )
    )
    if abs(float(probe["format"]["duration"]) - duration) > 0.08:
        raise ValueError(
            f"témoin de {probe['format']['duration']} s, fiche de {duration} s"
        )
    num, den = map(int, probe["streams"][0]["avg_frame_rate"].split("/"))
    if den == 0 or abs(num / den - FPS) > 0.01:
        raise ValueError(
            f"témoin à {probe['streams'][0]['avg_frame_rate']} images par seconde"
        )
    pcm = subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(draft),
            "-map",
            "0:a:0",
            "-f",
            "s16le",
            "-ac",
            "2",
            "-ar",
            "48000",
            "-",
        ]
    )
    return {
        "expected_pcm_sha256": hashlib.sha256(pcm).hexdigest(),
        "expected_video_stream_sha256": film_guard.video_stream_hash(draft),
        "expected_duration_s": duration,
        "expected_fps": FPS,
        "expected_packets_sha256": film_guard.packets_hash(draft),
        "expected_format_tags": probe["format"].get("tags", {}),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Brouillon témoin et référence de sortie d'un film."
    )
    parser.add_argument("film", type=Path)
    parser.add_argument("--from", dest="draft", type=Path)
    args = parser.parse_args()
    film = args.film.resolve()
    try:
        fiche = json.loads((film / "provenance-manifest.json").read_text())
        # Refus vérifié avant tout rendu : un rendu d'une minute ne doit pas précéder un refus connu.
        if fiche["film"].get("output_sha256"):
            raise ValueError(
                "fiche d'un film déjà rendu : sa référence fige ce film, rien n'est écrit"
            )
        draft = args.draft.resolve() if args.draft else render_witness(film)
        ref = reference(film, draft)
    except (
        OSError,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        subprocess.SubprocessError,
    ) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False))
        return 2
    (film / "output-reference.json").write_text(json.dumps(ref, indent=2) + "\n")
    print(
        json.dumps(
            {
                "status": "PASS",
                "witness": str(draft),
                "reference": "output-reference.json",
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
