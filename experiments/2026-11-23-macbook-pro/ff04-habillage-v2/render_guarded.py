"""Rendu gardé du film de réservation, habillage de la version 2 de la fiche : paramètres du film, logique dans film-chain."""

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
PIN_MANIFEST_SHA256 = "43679e5739910ca572912b9ad36aec75dc6815c989c26b82a944a945574a0b67"
PIN_HTML_SHA256 = "5a127053a9ea04d7cf0fecf72154f39fe8ded6331007394d411775a32b1d30ed"
PIN_OUTPUT_REFERENCE_SHA256 = (
    "95de483edf8344b00d59b15c7088c5ddd8cfc8946faa5946d0d80cc5d2ce60e8"
)

GUARD = film_guard.FilmGuard(
    root=ROOT,
    prefix="film",
    media=MEDIA,
    config=CONFIG,
    pins_ref="input-pins.json",
    reference_ref="output-reference.json",
    output="media/room-booking-v2.mp4",
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
