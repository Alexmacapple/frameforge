"""Rendu gardé de la copie de travail (expérience de révision et reprise) : paramètres du film, logique dans film-chain."""

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "film-chain"))
film_guard = importlib.import_module("film_guard")

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
PIN_MANIFEST_SHA256 = "ff60da8fa50adf9b6b3916ecc59f060cc1cc5bee6d4873ba09bf4f2f25d703b0"
PIN_HTML_SHA256 = "d5a145c9244192ac1652c8907950c05ad4f5171afde4209e1f61b0e4393dc2a2"
PIN_OUTPUT_REFERENCE_SHA256 = (
    "262c9fb12261123c7f650b59ae836f2286a9c59417ff72ae3326bae13b094e13"
)

GUARD = film_guard.FilmGuard(
    root=ROOT,
    prefix="film",
    media=MEDIA,
    config=CONFIG,
    pins_ref="input-pins.json",
    reference_ref="output-reference.json",
    output="media/revised.mp4",
    pins=(PIN_MANIFEST_SHA256, PIN_HTML_SHA256, PIN_OUTPUT_REFERENCE_SHA256),
)
sha = film_guard.sha
fiche_build = film_guard.fiche_build


def load_fiche():
    return GUARD.load_fiche()


def fiche_failures():
    return GUARD.fiche_failures(load_fiche())


def preflight(reference, candidate):
    return GUARD.preflight(
        reference, candidate, load_fiche=load_fiche, fiche_failures=fiche_failures
    )


def validate_output(path):
    return GUARD.validate_output(path, load_fiche=load_fiche)


if __name__ == "__main__":
    sys.exit(GUARD.main(preflight, validate_output))
