"""Rendu gardé du film de réservation de salle, second film produit depuis une fiche.

Copie adaptée du garde de form-pilot-kokoro : seuls changent les noms de fichiers, les empreintes
et les seuils de durée, désormais lus dans la référence de sortie.

Les empreintes figent une fixture technique : elles ne valent ni approbation éditoriale
ni autorisation de diffusion. Modifier le code et les références ensemble n'est pas une
approbation indépendante.
"""

import hashlib
import importlib
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent
# Le wrapper V2 est réutilisé tel quel ; il importe lui-même son voisin guarded_hyperframes.
sys.path.insert(0, str(ROOT.parent / "ff10-hyperframes-guarded-integration"))
wrapper = importlib.import_module("guarded_hyperframes_v2")
sys.path.insert(0, str(ROOT.parent / "ff10-second-web-demo-transfer/form-pilot-kokoro"))
fiche_check = importlib.import_module("check_manifest")
fiche_build = importlib.import_module("build_from_fiche")

MEDIA = ("capture.mp4", "voice1.wav", "voice2.wav", "voice3.wav")
CONFIG = (
    "index.html",
    "hyperframes.json",
    "package.json",
    "captions.srt",
    "captions.vtt",
    "transcript.txt",
    "input-pins.json",
    "output-reference.json",
    "provenance-manifest.json",
    "capture-events.json",
)
PIN_MANIFEST_SHA256 = "32b548ff6d03c4cae9481463f1c9801e379803ab0bd47167f9c7613f714eaa84"
PIN_HTML_SHA256 = "39a4a620ecdd6f3aaf9fc3ad9bddf8273ed4edcfd09e6aba7e9d19844e2cec81"
PIN_OUTPUT_REFERENCE_SHA256 = (
    "54292d32bc601f80150a421f4528b117e0fb3e21ac1344f546c9c1898aa52067"
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def preflight(reference, candidate):
    if sha(reference) != PIN_HTML_SHA256 or sha(candidate) != PIN_HTML_SHA256:
        raise ValueError("film_reference_or_candidate_changed")
    root = Path(candidate).parent
    manifest = root / "input-pins.json"
    if sha(manifest) != PIN_MANIFEST_SHA256:
        raise ValueError("film_manifest_changed")
    for name, expected in json.loads(manifest.read_text()).items():
        asset = root / name
        if not asset.is_file() or sha(asset) != expected:
            raise ValueError("film_asset_changed:" + name)
    if sha(root / "output-reference.json") != PIN_OUTPUT_REFERENCE_SHA256:
        raise ValueError("film_output_reference_changed")
    # La fiche du projet doit être cohérente avec les fichiers qu'elle cite. Elle est lue dans le
    # projet d'origine, y compris quand ce précontrôle est rejoué sur la copie isolée : la fiche
    # renvoie à des documents voisins que la copie n'embarque pas, et les empreintes ci-dessus
    # garantissent déjà que la copie porte la même fiche.
    failures = fiche_failures()
    if failures:
        raise ValueError("film_fiche_incoherent:" + ",".join(failures))
    # La fiche est la seule source des fichiers texte : ceux du projet doivent être ceux qu'elle génère.
    stale = fiche_build.stale_files(load_fiche(), ROOT)
    if stale:
        raise ValueError("film_files_not_generated_from_fiche:" + ",".join(stale))
    return True


def load_fiche():
    return json.loads((ROOT / "provenance-manifest.json").read_text())


def fiche_failures():
    """Noms des contrôles en échec ; les UNVERIFIED déclarés ne bloquent pas le rendu."""
    results = fiche_check.check_data(load_fiche(), ROOT)
    return sorted({r["check"] for r in results if r["status"] == "FAIL"})


def video_stream_hash(path):
    out = subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(path),
            "-map",
            "0:v:0",
            "-c",
            "copy",
            "-f",
            "streamhash",
            "-hash",
            "sha256",
            "-",
        ]
    )
    return out.decode().strip().split("=")[-1]


def validate_output(path):
    reference = json.loads((ROOT / "output-reference.json").read_text())
    data = json.loads(
        subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration:stream=codec_type,codec_name,width,height,nb_frames,avg_frame_rate,duration",
                "-of",
                "json",
                str(path),
            ]
        )
    )
    if abs(float(data["format"]["duration"]) - reference["expected_duration_s"]) > 0.08:
        raise ValueError("film_output_duration_invalid")
    video = [s for s in data["streams"] if s["codec_type"] == "video"]
    audio = [s for s in data["streams"] if s["codec_type"] == "audio"]
    if (
        len(video) != 1
        or video[0].get("codec_name") != "h264"
        or (video[0].get("width"), video[0].get("height")) != (1920, 1080)
    ):
        raise ValueError("film_output_video_invalid")
    num, den = map(int, video[0].get("avg_frame_rate", "0/0").split("/"))
    if (
        den == 0
        or abs(num / den - reference["expected_fps"]) > 0.01
        or int(video[0].get("nb_frames") or 0) < reference["expected_duration_s"] * reference["expected_fps"]
    ):
        raise ValueError("film_output_framerate_invalid")
    if (
        len(audio) != 1
        or audio[0].get("codec_name") != "aac"
        or float(audio[0].get("duration") or 0) < reference["expected_duration_s"] - 0.1
    ):
        raise ValueError("film_output_audio_invalid")
    # Les images doivent être exactement celles du brouillon témoin de référence.
    if video_stream_hash(path) != reference["expected_video_stream_sha256"]:
        raise ValueError("film_output_video_changed")
    pcm = subprocess.check_output(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(path),
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
    if hashlib.sha256(pcm).hexdigest() != reference["expected_pcm_sha256"]:
        raise ValueError("film_output_audio_changed")
    return True


def main():
    args = SimpleNamespace(
        project=ROOT,
        baseline=ROOT / "baseline.html",
        candidate=ROOT / "index.html",
        output=ROOT / "media/room-booking.mp4",
    )
    try:
        print(
            json.dumps(
                wrapper.run(
                    args,
                    preflight_fn=preflight,
                    media=MEDIA,
                    config=CONFIG,
                    output_validator=validate_output,
                )
            )
        )
    except (
        ValueError,
        OSError,
        RuntimeError,
        subprocess.CalledProcessError,
        KeyboardInterrupt,
    ) as exc:
        print(json.dumps({"status": "BLOCKED_OR_INTERRUPTED", "reason": str(exc)}))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
