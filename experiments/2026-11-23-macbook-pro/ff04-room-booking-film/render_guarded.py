"""Rendu gardé du film de réservation de salle : paramètres du film, logique dans film-chain."""

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
PIN_MANIFEST_SHA256 = "32b548ff6d03c4cae9481463f1c9801e379803ab0bd47167f9c7613f714eaa84"
PIN_HTML_SHA256 = "39a4a620ecdd6f3aaf9fc3ad9bddf8273ed4edcfd09e6aba7e9d19844e2cec81"
PIN_OUTPUT_REFERENCE_SHA256 = (
    "72c7a0da7f774a5ab3679a0e75e6ade2c6df5f95e0dd0ba671898d1e356fa9cb"
)

GUARD = film_guard.FilmGuard(
    root=ROOT,
    prefix="film",
    media=MEDIA,
    config=CONFIG,
    pins_ref="input-pins.json",
    reference_ref="output-reference.json",
    output="media/room-booking.mp4",
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
    return GUARD.validate_output(path)


if __name__ == "__main__":
    sys.exit(GUARD.main(preflight, validate_output))
