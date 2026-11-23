"""FF-10 — rendu gardé du formulaire, voix Kokoro lue directement par la composition.

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
sys.path.insert(0, str(ROOT.parents[1] / "ff10-hyperframes-guarded-integration"))
wrapper = importlib.import_module("guarded_hyperframes_v2")
sys.path.insert(0, str(ROOT))
fiche_check = importlib.import_module("check_manifest")
fiche_build = importlib.import_module("build_from_fiche")

MEDIA = ("capture.mp4", "kokoro1.wav", "kokoro2.wav", "kokoro3.wav")
CONFIG = (
    "index.html",
    "hyperframes.json",
    "package.json",
    "captions.srt",
    "captions.vtt",
    "transcript.txt",
    "kokoro-input-pins.json",
    "kokoro-output-reference.json",
    "provenance-manifest.json",
    "capture-events.json",
)
PIN_MANIFEST_SHA256 = "9513a93b40f00873a5da1de79207c079a2820aa1bd567c582d59354d6f59da36"
PIN_HTML_SHA256 = "4fd5bd62879513b88e538808f2b382fd99fe876f0351b698bd686c5ff84ee1ee"
PIN_OUTPUT_REFERENCE_SHA256 = (
    "5ed3fd42e6f0b4c2737fceea52d3fd5af1a9c3dbd39d136e9ce6661146e36563"
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def preflight(reference, candidate):
    if sha(reference) != PIN_HTML_SHA256 or sha(candidate) != PIN_HTML_SHA256:
        raise ValueError("kokoro_reference_or_candidate_changed")
    root = Path(candidate).parent
    manifest = root / "kokoro-input-pins.json"
    if sha(manifest) != PIN_MANIFEST_SHA256:
        raise ValueError("kokoro_manifest_changed")
    for name, expected in json.loads(manifest.read_text()).items():
        asset = root / name
        if not asset.is_file() or sha(asset) != expected:
            raise ValueError("kokoro_asset_changed:" + name)
    if sha(root / "kokoro-output-reference.json") != PIN_OUTPUT_REFERENCE_SHA256:
        raise ValueError("kokoro_output_reference_changed")
    # La fiche du projet doit être cohérente avec les fichiers qu'elle cite. Elle est lue dans le
    # projet d'origine, y compris quand ce précontrôle est rejoué sur la copie isolée : la fiche
    # renvoie à des documents voisins que la copie n'embarque pas, et les empreintes ci-dessus
    # garantissent déjà que la copie porte la même fiche.
    failures = fiche_failures()
    if failures:
        raise ValueError("kokoro_fiche_incoherent:" + ",".join(failures))
    # La fiche est la seule source des fichiers texte : ceux du projet doivent être ceux qu'elle génère.
    stale = fiche_build.stale_files(load_fiche(), ROOT)
    if stale:
        raise ValueError("kokoro_files_not_generated_from_fiche:" + ",".join(stale))
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
    reference = json.loads((ROOT / "kokoro-output-reference.json").read_text())
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
        raise ValueError("kokoro_output_duration_invalid")
    video = [s for s in data["streams"] if s["codec_type"] == "video"]
    audio = [s for s in data["streams"] if s["codec_type"] == "audio"]
    if (
        len(video) != 1
        or video[0].get("codec_name") != "h264"
        or (video[0].get("width"), video[0].get("height")) != (1920, 1080)
    ):
        raise ValueError("kokoro_output_video_invalid")
    num, den = map(int, video[0].get("avg_frame_rate", "0/0").split("/"))
    if (
        den == 0
        or abs(num / den - reference["expected_fps"]) > 0.01
        or int(video[0].get("nb_frames") or 0) < 480
    ):
        raise ValueError("kokoro_output_framerate_invalid")
    if (
        len(audio) != 1
        or audio[0].get("codec_name") != "aac"
        or float(audio[0].get("duration") or 0) < 15.9
    ):
        raise ValueError("kokoro_output_audio_invalid")
    # Les images doivent être exactement celles du brouillon témoin de référence.
    if video_stream_hash(path) != reference["expected_video_stream_sha256"]:
        raise ValueError("kokoro_output_video_changed")
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
        raise ValueError("kokoro_output_audio_changed")
    return True


def main():
    args = SimpleNamespace(
        project=ROOT,
        baseline=ROOT / "baseline.html",
        candidate=ROOT / "index.html",
        output=ROOT / "media/form-kokoro-pointeur.mp4",
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
