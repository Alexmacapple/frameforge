"""Rendu gardé du film des fenêtres modales avec récapitulatif animé : paramètres du film."""

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
    "voice8.wav",
    "compositions/recapitulatif.html",
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
PIN_MANIFEST_SHA256 = "534935a22ae933bf9abdee3a2c1d1a696479bdd2353324572ea3d42a0fa6a324"
PIN_HTML_SHA256 = "72861787fab5e342b31cbfb32440c4438d5a011a19a763174f2b5133bfdecb83"
PIN_OUTPUT_REFERENCE_SHA256 = (
    "ea047a6f437ec607eb479d9f866754a0910a01d0aa2252a988f6dd9826f40614"
)

GUARD = film_guard.FilmGuard(
    root=ROOT,
    prefix="film",
    media=MEDIA,
    config=CONFIG,
    pins_ref="input-pins.json",
    reference_ref="output-reference.json",
    output="media/fenetres-modales-recap.mp4",
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
