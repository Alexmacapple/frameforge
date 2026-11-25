"""Synthèse Kokoro des trois phrases de l'insert animé (ticket 59).

Mêmes réglages que le film 47 (voix, vitesse, graine). Une phrase par clip : la durée de chaque
clip cale une étape de l'animation. Les clips ne sont pas versionnés ; leurs empreintes et durées
sont écrites dans narration-synthesis.json.

À lancer depuis la racine du dépôt :
  HF_HUB_OFFLINE=1 .venv-voice/bin/python experiments/2026-11-23-macbook-pro/ff59-insert-anime/synthesize_kokoro.py
"""

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from kokoro import KPipeline

ROOT = Path(__file__).resolve().parent
VOICE, LANG, SPEED, SEED, RATE = "ff_siwis", "f", 1.2, 20261123, 24000
PHRASES = json.loads((ROOT / "phrases.json").read_text())


def main():
    pipeline = KPipeline(lang_code=LANG)
    report = {"voice": VOICE, "lang": LANG, "speed": SPEED, "seed": SEED, "clips": []}
    for i, text in enumerate(PHRASES, 1):
        torch.manual_seed(SEED)
        parts = [
            np.asarray(audio, dtype=np.float32)
            for _, _, audio in pipeline(
                text, voice=VOICE, speed=SPEED, split_pattern=r"\n+"
            )
        ]
        if not parts:
            print(json.dumps({"status": "FAIL", "reason": "aucun son", "text": text}))
            return 1
        samples = np.concatenate(parts)
        target = ROOT / f"voice{i}.wav"
        if target.exists():
            print(json.dumps({"status": "BLOCKED", "reason": f"{target.name} existe"}))
            return 2
        sf.write(str(target), samples, RATE, subtype="PCM_16")
        report["clips"].append(
            {
                "audio_ref": target.name,
                "text": text,
                "duration_s": round(len(samples) / RATE, 3),
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            }
        )
    (ROOT / "narration-synthesis.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps({"status": "PASS", "clips": report["clips"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
