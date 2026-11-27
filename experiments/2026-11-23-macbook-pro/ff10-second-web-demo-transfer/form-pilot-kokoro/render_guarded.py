"""Rendu gardé du film du formulaire (FF-10) : paramètres du film, logique dans film-chain."""

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / "film-chain"))
film_guard = importlib.import_module("film_guard")

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
PIN_MANIFEST_SHA256 = "e9ff5faef856f080b688b58a2d63b16ce1103d5400b759fc26f55da76acec210"
PIN_HTML_SHA256 = "4fd5bd62879513b88e538808f2b382fd99fe876f0351b698bd686c5ff84ee1ee"
PIN_OUTPUT_REFERENCE_SHA256 = (
    "3ac5e0d210f372632fede3122ce925273c1c3efc6a562739092686c6a955183d"
)

GUARD = film_guard.FilmGuard(
    root=ROOT,
    prefix="kokoro",
    media=MEDIA,
    config=CONFIG,
    pins_ref="kokoro-input-pins.json",
    reference_ref="kokoro-output-reference.json",
    output="media/form-kokoro-pointeur.mp4",
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
