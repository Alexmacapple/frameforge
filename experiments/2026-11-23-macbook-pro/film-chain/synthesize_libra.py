"""Synthèse Libra-TTS des phrases de la fiche d'un film neuf (seconde voix, à côté de Kokoro).

Usage, avec le Python de `.venv-libra` (voir le README) :
  .venv-libra/bin/python synthesize_libra.py DOSSIER_DU_FILM [--voice nina] [--model DOSSIER]

Chaque clip est écrit sous le nom que la fiche lui donne, puis `narration-synthesis.json` relève
le moteur, la voix et l'empreinte de chaque clip. Aucun post-traitement.

Trois règles, contrôlées avant de charger le modèle :
- le modèle doit porter les empreintes de la révision figée ci-dessous ;
- aucun clip ni rapport existant n'est écrasé : un média figé n'existe qu'en un exemplaire local,
  et un film approuvé ne se resynthétise pas ;
- un clip s'écrit dans le dossier du film, sous un nom simple.

La synthèse se fait sans réseau. Sur le Mac Studio, le 28 novembre 2026, deux passages ont donné
les mêmes clips à l'octet près ; ce n'est pas vérifié d'une machine à l'autre.
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

ENGINE = "libra-tts"
CODE_COMMIT = "2642632179db91866041ba1a90d0988705217a09"
MODEL_REPO = "Ekam/Libra-TTS"
MODEL_REVISION = "a29b9e64155bffd08966f180502ca412cb358c92"
MODEL_SHA256 = {
    "model.safetensors": "f57fbe7cf62a429e470a7b90b4ad5ca4405ae909d17db6f641c5b9cec1ed9ec2",
    "codec.safetensors": "6e943a7e31d72f3d51e012562756af941a7a01b60eb42c9a32f4fc166d62c00c",
    "config.json": "d303cca62a64645eab90a33701efeb4a8651bcc1f0cb8a9f1938a8d072a27bab",
    "tokenizer.json": "21cbba93fc2b3723c68db44ba5a8ff1a22a3f7bed34a5adbd5a165e17fff551c",
    "frontend/en_acronyms.txt": "b822dfe17a9d52285954a2962a6405805ba8aa24719931e75466c1d5a49bfda5",
    "frontend/en_lexicon.tsv": "38bef48d028c75d0a2ac140d5411d90ce4efc58ac9f79a9ccb0506e060f749f3",
    "frontend/zh_rare_tokens.json": "87edf2f08cdb9db1b3632b5004fcb7dd449d364b7c9766967f790985a9cf2cd3",
}
DEFAULT_MODEL = Path.home() / ".cache" / "frameforge" / "libra-tts" / MODEL_REVISION
VOICES = ("nina", "sofia", "aliya", "omar", "jon", "bob", "maya", "sam")
LANG, SEED, REPORT = "fr", 0, "narration-synthesis.json"


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def check_model(model, expected):
    for name, digest in sorted(expected.items()):
        if not (model / name).is_file():
            raise ValueError(f"modele_absent:{name}")
        if sha(model / name) != digest:
            raise ValueError(f"modele_different:{name}")


def clips(film):
    """Rend (texte, cible) pour chaque phrase ; refuse tout ce qui écraserait ou sortirait du film."""
    fiche = film / "provenance-manifest.json"
    if not fiche.is_file():
        raise ValueError("fiche_absente")
    if (film / REPORT).exists() or (film / REPORT).is_symlink():
        raise ValueError("rapport_deja_present")
    out, seen = [], set()
    for scene in json.loads(fiche.read_text())["scenes"]:
        text, ref = scene["narration"]["text"], scene["narration"]["audio_ref"]
        if not ref or Path(ref).name != ref or ref in (".", ".."):
            raise ValueError(f"nom_de_clip_refuse:{ref}")
        if ref in seen:
            raise ValueError(f"clip_cite_deux_fois:{ref}")
        seen.add(ref)
        target = film / ref
        if target.exists() or target.is_symlink():
            raise ValueError(f"clip_deja_present:{ref}")
        out.append((text, ref, target))
    return out


class LibraEngine:
    """Le vrai moteur, chargé seulement une fois tous les contrôles passés."""

    def __init__(self, model):
        os.environ["HF_HUB_OFFLINE"] = "1"
        from libra_tts import LibraTTS

        self.tts = LibraTTS(str(model), backend="mlx")

    def write(self, target, text, voice):
        audio = self.tts.synthesize(text, voice=voice, lang=LANG, seed=SEED)
        if len(audio):
            self.tts.save(str(target), audio)
        return len(audio) / self.tts.sample_rate


def synthesize(film, model, voice, load=LibraEngine, expected=None):
    if voice not in VOICES:
        raise ValueError(f"voix_inconnue:{voice}")
    todo = clips(film)
    check_model(model, MODEL_SHA256 if expected is None else expected)
    engine = load(model)
    report = {
        "engine": ENGINE,
        "code_commit": CODE_COMMIT,
        "model": MODEL_REPO,
        "model_revision": MODEL_REVISION,
        "voice": voice,
        "lang": LANG,
        "seed": SEED,
        "clips": [],
    }
    for text, ref, target in todo:
        duration = engine.write(target, text, voice)
        if not duration or not target.is_file():
            raise ValueError(f"aucun_son:{ref}")
        report["clips"].append(
            {
                "audio_ref": ref,
                "text": text,
                "duration_s": round(duration, 3),
                "sha256": sha(target),
            }
        )
    (film / REPORT).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("film", type=Path)
    parser.add_argument("--voice", default="nina")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    args = parser.parse_args()
    try:
        report = synthesize(args.film.resolve(), args.model, args.voice)
    except ValueError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, ensure_ascii=False))
        return 1
    print(
        json.dumps(
            {
                "status": "PASS",
                "voice": report["voice"],
                "clips": [(c["audio_ref"], c["duration_s"]) for c in report["clips"]],
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
