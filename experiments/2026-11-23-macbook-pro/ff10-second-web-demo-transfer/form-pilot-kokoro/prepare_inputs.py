"""Reconstruit les médias locaux du pilote Kokoro depuis les sources figées de form-pilot.

Recette de la piste approuvée à l'écoute (voir KOKORO-NATIVE-PROTOCOL.md) :
phrases 1 et 2 accélérées par atempo, phrase 3 inchangée. Aucune synthèse n'est relancée.
"""

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT.parent / "form-pilot"
SOURCE_PINS = {
    "capture.mp4": "43c3350529a8cd9ecb74bbc39009fb49e60dd95289c87b388a9ce6f6b6a1e6c3",
    "media/kokoro-fast1.wav": "9cd8bc0f02321e9a7dde3a2ebaf9e997ac0d801ed1719d493b82033e37344819",
    "media/kokoro-fast2.wav": "c717e1fdc212083ec03d811a0c112e5fd89b5caefa37b6b29d177092a2703089",
    "media/kokoro-fast3.wav": "676c07c7ad87cc084f5db3f143bc32d0ebb9d4aeccaf66c69af8edced73cdca3",
}
# (fichier produit, source, facteur atempo ou None pour une copie exacte)
RECIPE = (
    ("capture.mp4", "capture.mp4", None),
    ("kokoro1.wav", "media/kokoro-fast1.wav", "1.06"),
    ("kokoro2.wav", "media/kokoro-fast2.wav", "1.08"),
    ("kokoro3.wav", "media/kokoro-fast3.wav", None),
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare(sources=SOURCES, target=ROOT):
    sources, target = Path(sources), Path(target)
    pins = json.loads((ROOT / "kokoro-input-pins.json").read_text())
    for src, expected in SOURCE_PINS.items():
        if not (sources / src).is_file() or sha(sources / src) != expected:
            raise ValueError("kokoro_source_changed:" + src)
    # Tout est construit et vérifié à l'écart ; rien n'est déposé si un seul fichier diverge.
    with tempfile.TemporaryDirectory(prefix=".prepare-", dir=target) as temp:
        work = Path(temp)
        for name, src, tempo in RECIPE:
            if tempo is None:
                shutil.copyfile(sources / src, work / name)
            else:
                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-v",
                        "error",
                        "-i",
                        str(sources / src),
                        "-af",
                        "atempo=" + tempo,
                        "-c:a",
                        "pcm_s16le",
                        "-bitexact",
                        str(work / name),
                    ],
                    check=True,
                )
            if sha(work / name) != pins[name]:
                raise ValueError("kokoro_derived_input_mismatch:" + name)
        for name, _, _ in RECIPE:
            os.replace(work / name, target / name)
    return {"status": "PASS", "prepared": [name for name, _, _ in RECIPE]}


if __name__ == "__main__":
    import sys

    try:
        print(json.dumps(prepare()))
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}))
        sys.exit(2)
