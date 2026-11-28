"""Rendu gardé du film de la phrase qui déborde (expérience FF-06) : paramètres du film, logique dans film-chain."""

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
PIN_MANIFEST_SHA256 = "426113c8d023128983525652259c297bf0b8d5fd5bcda2675ac35369e905c05e"
PIN_HTML_SHA256 = "a4b088ec431853eb30e2ac4587ea3f3f3ad75a8e7720d32a5cd901a5e6a9eb00"
PIN_OUTPUT_REFERENCE_SHA256 = (
    "a471919ab03fae036fa2e59bb57aaeafd9f1fc474c8bd64bc25ce75d20231c66"
)

GUARD = film_guard.FilmGuard(
    root=ROOT,
    prefix="film",
    media=MEDIA,
    config=CONFIG,
    pins_ref="input-pins.json",
    reference_ref="output-reference.json",
    output="media/overflowing-sentence.mp4",
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
