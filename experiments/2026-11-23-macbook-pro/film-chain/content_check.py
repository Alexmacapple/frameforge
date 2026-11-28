"""Contrôle le contenu d'un brouillon témoin avant qu'il devienne la référence du film (ticket 78).

Usage :
  python3 content_check.py DOSSIER_DU_FILM TEMOIN

La référence d'un film neuf est mesurée sur son témoin, puis le garde exige que tout rendu la
reproduise : un témoin muet deviendrait la norme. Ce contrôle regarde le témoin, sans le modifier,
avec trois filtres de FFmpeg (blackdetect, freezedetect, silencedetect) et sa mesure de niveau.

Refusé :
- son_muet           le son de tout le film est sous -50 LUFS ;
- voix_absente:N     le créneau de la phrase N de la fiche est silencieux à 80 % ou plus ;
- image_noire:P      l'écran est noir pendant la moitié du film ou plus (P en pour cent) ;
- image_figee:P      une seule image tient 90 % du film ou plus ;
- son_illisible, temoin_illisible   FFmpeg ne lit pas le son, ou pas le fichier.

Les seuils viennent d'une mesure du 28 novembre 2026 sur six témoins approuvés : aucun noir, et un
film immobile 88 à 96 % du temps, en 9 à 31 plans fixes dont le plus long tient au plus 34 % de la
durée. Une capture d'écran bouge peu : seule une image unique sur presque tout le film est une panne.

Limites : ce contrôle voit un film vide ou amputé, pas un film faux. Une voix qui dit autre chose,
une image qui montre la mauvaise page ou un son trop fort passent. Un témoin accepté reste à
regarder et à écouter.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SILENT_LUFS = -50.0
SILENCE = "silencedetect=noise=-50dB:d=0.2"
PICTURE = "blackdetect=d=0.1:pix_th=0.10,freezedetect=n=-60dB:d=0.5"
ABSENT_VOICE, BLACK_FILM, STILL_FILM = 0.8, 0.5, 0.9


def ffmpeg(draft, *filters):
    return subprocess.run(
        [
            "ffmpeg",
            "-nostdin",
            "-hide_banner",
            "-i",
            str(draft),
            *filters,
            "-f",
            "null",
            "-",
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=600,
    )


def measure(draft):
    """Durée, noir, plus long plan fixe, niveau et silences du témoin ; ValueError s'il est illisible."""
    try:
        duration = float(
            subprocess.check_output(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "csv=p=0",
                    str(draft),
                ],
                stderr=subprocess.DEVNULL,
                timeout=60,
            )
        )
        picture = ffmpeg(draft, "-an", "-vf", PICTURE)
        if picture.returncode != 0 or duration <= 0:
            raise ValueError("temoin_illisible")
    except (subprocess.SubprocessError, ValueError) as exc:
        raise ValueError("temoin_illisible") from exc
    sound = ffmpeg(draft, "-vn", "-af", f"{SILENCE},loudnorm=print_format=json")
    try:
        text = sound.stderr
        lufs = float(
            json.loads(text[text.rindex("{") : text.rindex("}") + 1])["input_i"]
        )
    except (ValueError, KeyError) as exc:
        raise ValueError("son_illisible") from exc
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", text)]
    ends = [float(x) for x in re.findall(r"silence_end: (-?[\d.]+)", text)]
    # Un silence qui dure jusqu'à la fin du film n'a pas de fin annoncée.
    ends += [duration] * (len(starts) - len(ends))
    stills = [
        float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", picture.stderr)
    ]
    opened = len(re.findall(r"freeze_start: ", picture.stderr)) - len(stills)
    last_start = re.findall(r"freeze_start: ([\d.]+)", picture.stderr)
    if opened > 0 and last_start:
        stills.append(duration - float(last_start[-1]))
    return {
        "duration_s": duration,
        "black_s": sum(
            float(x) for x in re.findall(r"black_duration:([\d.]+)", picture.stderr)
        ),
        "longest_still_s": max(stills, default=0.0),
        "lufs": lufs,
        "silences": list(zip(starts, ends)),
    }


def failures(measured, narrations):
    """Motifs de refus, dans un ordre fixe ; liste vide si le témoin est accepté."""
    reasons = []
    if measured["lufs"] < SILENT_LUFS:
        reasons.append("son_muet")
    for rank, narration in enumerate(narrations, 1):
        start = narration["start_s"]
        end = start + narration["duration_s"]
        silent = sum(
            max(0.0, min(end, stop) - max(start, begin))
            for begin, stop in measured["silences"]
        )
        if end > start and silent / (end - start) >= ABSENT_VOICE:
            reasons.append(f"voix_absente:{rank}")
    duration = measured["duration_s"]
    if measured["black_s"] / duration >= BLACK_FILM:
        reasons.append(f"image_noire:{round(100 * measured['black_s'] / duration)}")
    if measured["longest_still_s"] / duration >= STILL_FILM:
        reasons.append(
            f"image_figee:{round(100 * measured['longest_still_s'] / duration)}"
        )
    return reasons


def run(film, draft):
    """Motifs de refus du témoin d'un film, lus contre les phrases de sa fiche."""
    fiche = json.loads((Path(film) / "provenance-manifest.json").read_text())
    narrations = [s["narration"] for s in fiche.get("scenes", []) if s.get("narration")]
    try:
        return failures(measure(draft), narrations)
    except ValueError as exc:
        return [str(exc)]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("film", type=Path)
    parser.add_argument("draft", type=Path)
    args = parser.parse_args()
    try:
        reasons = run(args.film.resolve(), args.draft.resolve())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status": "FAIL" if reasons else "PASS", "reasons": reasons}))
    return 1 if reasons else 0


if __name__ == "__main__":
    sys.exit(main())
