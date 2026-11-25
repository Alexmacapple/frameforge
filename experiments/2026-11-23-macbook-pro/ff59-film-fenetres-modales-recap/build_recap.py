"""Voix et sous-composition du récapitulatif animé, en fin du film des fenêtres modales.

  python3 build_recap.py voice    écrit voice8.wav : les trois clips de l'essai (ff59-insert-anime),
                                  séparés par GAP secondes de silence ; jamais par-dessus un fichier
  python3 build_recap.py insert   écrit compositions/recapitulatif.html depuis la fiche placée

L'animation part du début de la phrase de l'insert (son instant zéro) et dure jusqu'à la fin du
film ; chaque étape démarre avec sa phrase dans voice8.wav.
"""

import importlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ESSAI = ROOT.parent / "ff59-insert-anime"
sys.path.insert(0, str(ESSAI))
sys.path.insert(0, str(ROOT.parent / "film-chain"))
build_insert = importlib.import_module("build_insert")
b = importlib.import_module("build_from_fiche")
GAP, RATE = 0.4, 24000
CLIPS = json.loads((ESSAI / "narration-synthesis.json").read_text())["clips"]
TEXT = " ".join(c["text"] for c in CLIPS)


def voice():
    target = ROOT / "voice8.wav"
    if target.exists():
        raise ValueError(f"{target.name} existe, non écrasé")
    inputs, labels = [], []
    for i, clip in enumerate(CLIPS):
        inputs += ["-i", str(ESSAI / clip["audio_ref"])]
        labels.append(f"[{i}:a]")
    silence = f"anullsrc=r={RATE}:cl=mono,atrim=duration={GAP}"
    parts = []
    for i, label in enumerate(labels):
        parts.append(label)
        if i < len(labels) - 1:
            parts.append(f"[s{i}]")
    graph = (
        ";".join(f"{silence}[s{i}]" for i in range(len(labels) - 1))
        + ";"
        + "".join(parts)
        + f"concat=n={len(parts)}:v=0:a=1[out]"
    )
    subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            *inputs,
            "-filter_complex",
            graph,
            "-map",
            "[out]",
            "-ar",
            str(RATE),
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            "-bitexact",
            "-map_metadata",
            "-1",
            str(target),
        ],
        check=True,
        timeout=60,
    )
    return target


def insert():
    fiche = json.loads((ROOT / "provenance-manifest.json").read_text())
    [(ref, _start, length)] = b.insert_windows(fiche)
    times, t = [], 0.0
    for clip in CLIPS:
        times.append(round(t, 3))
        t += clip["duration_s"] + GAP
    target = ROOT / ref
    target.write_text(build_insert.embedded(times, length))
    return target, times, length


def main():
    try:
        if sys.argv[1:] == ["voice"]:
            print(
                json.dumps(
                    {"status": "PASS", "voice": str(voice().name), "text": TEXT},
                    ensure_ascii=False,
                )
            )
        elif sys.argv[1:] == ["insert"]:
            target, times, length = insert()
            print(
                json.dumps(
                    {
                        "status": "PASS",
                        "insert": str(target.relative_to(ROOT)),
                        "times_s": times,
                        "duration_s": length,
                    }
                )
            )
        else:
            raise ValueError("usage : voice | insert")
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
