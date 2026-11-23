"""Tests adverses du garde commun, joués sur chaque film : un film trafiqué ne doit pas passer.

Issus de la contre-revue du 23 novembre 2026 (issue 15). Chaque film d'essai est fabriqué sans
réencodage à partir du brouillon témoin du film, donc avec les mêmes images et le même son.
"""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
film_guard = importlib.import_module("film_guard")
FILMS = {
    "formulaire": (
        "ff10-second-web-demo-transfer/form-pilot-kokoro",
        "media/form-kokoro-pointeur-draft.mp4",
    ),
    "reservation": ("ff04-room-booking-film", "media/room-booking-draft.mp4"),
}
# Réécrit les horodatages vidéo sans toucher aux images : première moitié deux fois plus vite, seconde
# plus lente, dernière image au même instant. Durée, nombre d'images et cadence moyenne inchangés.
DESYNC = r"if(lt(PTS\,HALF)\,PTS/2\,HALF/2+floor((PTS-HALF)*(LAST-HALF/2)/(LAST-HALF)))"


def load(name):
    folder, draft = FILMS[name]
    root = CHAIN.parent / folder
    spec = importlib.util.spec_from_file_location(
        f"render_guarded_{name}", root / "render_guarded.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, root / draft


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def tampered(kind, source, target):
    """Fabrique un film trafiqué ; toujours en copie de flux, jamais en réencodage."""
    if kind == "upside_down":
        ffmpeg("-display_rotation", "180", "-i", str(source), "-c", "copy", str(target))
    elif kind == "rotated":
        ffmpeg("-display_rotation", "90", "-i", str(source), "-c", "copy", str(target))
    elif kind == "squeezed":
        ffmpeg("-i", str(source), "-c", "copy", "-aspect", "4:3", str(target))
    elif kind == "desynchronized":
        stream = json.loads(
            subprocess.check_output(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-select_streams",
                    "v:0",
                    "-show_entries",
                    "stream=duration_ts,nb_frames",
                    "-of",
                    "json",
                    str(source),
                ]
            )
        )["streams"][0]
        ticks, frames = int(stream["duration_ts"]), int(stream["nb_frames"])
        last = ticks - ticks // frames
        expr = DESYNC.replace("HALF", str(ticks // 2)).replace("LAST", str(last))
        ffmpeg(
            "-i",
            str(source),
            "-map",
            "0",
            "-c",
            "copy",
            "-bsf:v",
            f"setts=pts={expr}:dts={expr}",
            str(target),
        )
    elif kind == "lying_subtitles":
        srt = target.with_suffix(".srt")
        srt.write_text(
            "1\n00:00:00,000 --> 00:00:14,000\nCe film montre autre chose.\n"
        )
        ffmpeg(
            "-i",
            str(source),
            "-i",
            str(srt),
            "-map",
            "0",
            "-map",
            "1",
            "-c",
            "copy",
            "-c:s",
            "mov_text",
            "-disposition:s:0",
            "default",
            str(target),
        )
    elif kind == "lying_title":
        ffmpeg(
            "-i",
            str(source),
            "-c",
            "copy",
            "-metadata",
            "title=Film officiel approuvé",
            str(target),
        )
    else:
        raise ValueError(kind)


class TamperedFilmTests(unittest.TestCase):
    def check(self, kind, reason):
        for name in FILMS:
            with self.subTest(film=name), tempfile.TemporaryDirectory() as tmp:
                module, draft = load(name)
                target = Path(tmp) / "film.mp4"
                tampered(kind, draft, target)
                with self.assertRaisesRegex(ValueError, reason):
                    module.validate_output(target)

    def test_witness_draft_accepted(self):
        for name in FILMS:
            with self.subTest(film=name):
                module, draft = load(name)
                self.assertTrue(module.validate_output(draft))

    def test_upside_down_film_rejected(self):
        self.check("upside_down", "output_display_altered")

    def test_rotated_film_rejected(self):
        self.check("rotated", "output_display_altered")

    def test_squeezed_film_rejected(self):
        self.check("squeezed", "output_display_altered")

    def test_desynchronized_film_rejected(self):
        self.check("desynchronized", "output_packets_changed")

    def test_film_with_lying_subtitle_track_rejected(self):
        self.check("lying_subtitles", "output_streams_invalid")

    def test_film_with_lying_title_rejected(self):
        self.check("lying_title", "output_tags_changed")

    def test_incomplete_output_reference_is_refused_not_ignored(self):
        for name in FILMS:
            with self.subTest(film=name), tempfile.TemporaryDirectory() as tmp:
                module, draft = load(name)
                reference = json.loads(
                    (module.GUARD.root / module.GUARD.reference_ref).read_text()
                )
                for missing in ("expected_packets_sha256", "expected_format_tags"):
                    partial = {k: v for k, v in reference.items() if k != missing}
                    (Path(tmp) / "reference.json").write_text(json.dumps(partial))
                    guard = film_guard.FilmGuard(
                        root=tmp,
                        prefix="film",
                        media=(),
                        config=(),
                        pins_ref="pins.json",
                        reference_ref="reference.json",
                        output="film.mp4",
                        pins=("", "", ""),
                    )
                    with self.assertRaisesRegex(
                        ValueError, "output_reference_incomplete"
                    ):
                        guard.validate_output(draft)


if __name__ == "__main__":
    unittest.main()
