"""Planche d'images d'un film rendu, à regarder avant l'approbation.

Usage : python3 contact_sheet.py VIDEO [--out CHEMIN] [--cols N] [--rows N] [--width PX]

Par défaut, 12 images (4 colonnes, 3 rangées) de 480 px de large, prises au milieu de 12 tranches
égales du film, écrites à côté de la vidéo sous <film>-planche.png. Le ffmpeg local n'a pas le
filtre drawtext : la planche est sans légende, et les instants des images, dans l'ordre de lecture
(rangée par rangée, de gauche à droite), sont rendus dans la sortie JSON. Une planche existante
n'est pas écrasée. Créé le 25 novembre 2026 (ticket 60), depuis la planche faite à la main pour
le film 47.
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def duration(video):
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(video),
        ],
        timeout=30,
    )
    return float(out)


def sheet(video, out, cols, rows, width):
    """Écrit la planche et rend les instants des images ; lève ValueError en cas de refus."""
    if not video.is_file():
        raise ValueError(f"vidéo absente : {video}")
    if out.exists() or out.is_symlink():
        raise ValueError(f"planche existante, non écrasée : {out}")
    if min(cols, rows, width) < 1:
        raise ValueError("colonnes, rangées et largeur doivent être positives")
    total = duration(video)
    count = cols * rows
    times = [round(total * (i + 0.5) / count, 3) for i in range(count)]
    with tempfile.TemporaryDirectory(prefix=".planche-", dir=out.parent) as temp:
        for i, at in enumerate(times):
            subprocess.run(
                [
                    "ffmpeg",
                    "-v",
                    "error",
                    "-ss",
                    str(at),
                    "-i",
                    str(video),
                    "-frames:v",
                    "1",
                    "-vf",
                    f"scale={width}:-2",
                    str(Path(temp) / f"{i:03d}.png"),
                ],
                check=True,
                timeout=60,
            )
        built = Path(temp) / "planche.png"
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-i",
                str(Path(temp) / "%03d.png"),
                "-vf",
                f"tile={cols}x{rows}",
                "-frames:v",
                "1",
                str(built),
            ],
            check=True,
            timeout=60,
        )
        # Renommage dans le même dossier : la planche apparaît entière ou pas du tout.
        built.rename(out)
    return times


def main():
    parser = argparse.ArgumentParser(description="Planche d'images d'un film rendu.")
    parser.add_argument("video", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--cols", type=int, default=4)
    parser.add_argument("--rows", type=int, default=3)
    parser.add_argument("--width", type=int, default=480)
    args = parser.parse_args()
    video = args.video.resolve()
    out = (args.out or video.with_name(video.stem + "-planche.png")).resolve()
    try:
        times = sheet(video, out, args.cols, args.rows, args.width)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False))
        return 2
    print(
        json.dumps(
            {"status": "PASS", "sheet": str(out), "times_s": times}, ensure_ascii=False
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
