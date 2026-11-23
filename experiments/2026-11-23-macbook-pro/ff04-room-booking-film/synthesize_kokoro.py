"""Synthèse Kokoro reproductible des phrases de la fiche de film.

À lancer avec un Python qui dispose de kokoro, soundfile et torch (hors dépôt, voir le compte rendu).
La graine est remise avant chaque phrase. Elle ne suffit pas à tout rendre reproductible : sur ce
film, deux clips sur trois ressortent identiques à l'octet, le premier varie d'un passage à l'autre
(graine avant chargement, échauffement et fil unique essayés sans effet). Les clips utilisés par le
film sont donc figés par empreinte ; une nouvelle synthèse demande une nouvelle écoute.
Chaque clip est écrit sous le nom que la fiche lui donne ; aucun post-traitement, aucune accélération.
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


def main():
    fiche = json.loads((ROOT / "provenance-manifest.json").read_text())
    pipeline = KPipeline(lang_code=LANG)
    report = {"voice": VOICE, "lang": LANG, "speed": SPEED, "seed": SEED, "clips": []}
    for scene in fiche["scenes"]:
        narration = scene["narration"]
        torch.manual_seed(SEED)
        parts = [
            np.asarray(audio, dtype=np.float32)
            for _, _, audio in pipeline(
                narration["text"], voice=VOICE, speed=SPEED, split_pattern=r"\n+"
            )
        ]
        if not parts:
            print(
                json.dumps(
                    {
                        "status": "FAIL",
                        "reason": "aucun son produit",
                        "text": narration["text"],
                    }
                )
            )
            return 1
        samples = np.concatenate(parts)
        target = ROOT / narration["audio_ref"]
        sf.write(str(target), samples, RATE, subtype="PCM_16")
        report["clips"].append(
            {
                "audio_ref": narration["audio_ref"],
                "text": narration["text"],
                "duration_s": round(len(samples) / RATE, 3),
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            }
        )
    (ROOT / "narration-synthesis.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "status": "PASS",
                "clips": [(c["audio_ref"], c["duration_s"]) for c in report["clips"]],
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
