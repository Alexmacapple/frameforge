"""Rend l'insert avec les options du garde, sur une copie isolée de ses entrées.

Usage : python3 render_insert.py NOM   écrit media/NOM.mp4, jamais par-dessus un fichier existant

Mêmes options que guarded_hyperframes_v2.py (HyperFrames 0.8.33, --workers=2, --no-best-effort),
télémétrie coupée. Affiche l'empreinte du fichier et celles du flux vidéo et des paquets, mesurées
par les fonctions du garde : deux rendus identiques ont les mêmes.
"""

import hashlib
import importlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "film-chain"))
film_guard = importlib.import_module("film_guard")
INPUTS = ("index.html", "hyperframes.json", "voice1.wav", "voice2.wav", "voice3.wav")
RENDER = ["npx", "--yes", "hyperframes@0.8.33", "render"]
NO_TELEMETRY = {"HYPERFRAMES_NO_TELEMETRY": "1", "DO_NOT_TRACK": "1"}


def main():
    if len(sys.argv) != 2 or not sys.argv[1].replace("-", "").isalnum():
        print(json.dumps({"status": "BLOCKED", "reason": "usage : NOM"}))
        return 2
    target = ROOT / "media" / f"{sys.argv[1]}.mp4"
    if target.exists():
        print(json.dumps({"status": "BLOCKED", "reason": f"{target.name} existe"}))
        return 2
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix=".rendu-", dir=ROOT / "media") as temp:
        work = Path(temp) / "project"
        work.mkdir()
        for name in INPUTS:
            shutil.copyfile(ROOT / name, work / name)
        rendered = Path(temp) / "rendered.mp4"
        subprocess.run(
            [
                *RENDER,
                str(work),
                "--output=" + str(rendered),
                "--workers=2",
                "--no-best-effort",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            env=dict(os.environ, **NO_TELEMETRY),
            timeout=1800,
        )
        os.link(rendered, target)
    print(
        json.dumps(
            {
                "status": "PASS",
                "output": str(target.relative_to(ROOT)),
                "seconds": round(time.monotonic() - started, 1),
                "file_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "video_stream_sha256": film_guard.video_stream_hash(target),
                "packets_sha256": film_guard.packets_hash(target),
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
