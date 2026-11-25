"""Rendu gardé du film des fenêtres modales : paramètres du film, logique dans film-chain."""

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "film-chain"))
film_guard = importlib.import_module("film_guard")

MEDIA = (
    "capture.mp4",
    "voice1.wav",
    "voice2.wav",
    "voice3.wav",
    "voice4.wav",
    "voice5.wav",
    "voice6.wav",
    "voice7.wav",
)
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
PIN_MANIFEST_SHA256 = "8ef3433c505a4e0f9645a1f14811ca0f9c9907cf7ff1d72caaad6608697a7b49"
PIN_HTML_SHA256 = "ca9bec8348fa81daeea571a0d27d6159bbcb52d31e43ba9fc3036d5cc7a5b539"
PIN_OUTPUT_REFERENCE_SHA256 = (
    "af96f2b74848c8ed2dabc1a652a528149474761de355a4bf70f3be053d8b8ebb"
)

GUARD = film_guard.FilmGuard(
    root=ROOT,
    prefix="film",
    media=MEDIA,
    config=CONFIG,
    pins_ref="input-pins.json",
    reference_ref="output-reference.json",
    output="media/fenetres-modales.mp4",
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
