"""Tests adverses du garde commun, joués sur chaque film : un film trafiqué ne doit pas passer.

Issus de la contre-revue du 23 novembre 2026 (issue 15). Chaque film d'essai est fabriqué sans
réencodage à partir du brouillon témoin du film, donc avec les mêmes images et le même son.
"""

import importlib.util
import json
import subprocess
import sys
import shutil
import tempfile
import unittest
from unittest import mock
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


def copied_inputs(module, tmp):
    """Copie des fichiers de premier niveau d'un film : tout ce que le précontrôle lit."""
    root = Path(tmp) / "film"
    root.mkdir()
    for path in module.GUARD.root.iterdir():
        if path.is_file():
            shutil.copyfile(path, root / path.name)
    return root


class PreflightTests(unittest.TestCase):
    """Chaque motif de refus du précontrôle, sur les deux films."""

    def refused(self, reason, alter):
        for name in FILMS:
            with self.subTest(film=name), tempfile.TemporaryDirectory() as tmp:
                module, _ = load(name)
                root = copied_inputs(module, tmp)
                alter(module, root)
                with self.assertRaisesRegex(ValueError, reason):
                    module.preflight(root / "baseline.html", root / "index.html")

    def test_untouched_copy_accepted(self):
        for name in FILMS:
            with self.subTest(film=name), tempfile.TemporaryDirectory() as tmp:
                module, _ = load(name)
                root = copied_inputs(module, tmp)
                self.assertTrue(module.preflight(root / "baseline.html", root / "index.html"))

    def test_changed_composition_refused(self):
        def alter(module, root):
            (root / "index.html").write_text((root / "index.html").read_text() + "<!-- -->")

        self.refused("reference_or_candidate_changed", alter)

    def test_changed_pins_file_refused(self):
        def alter(module, root):
            path = root / module.GUARD.pins_ref
            path.write_text(path.read_text() + "\n")

        self.refused("manifest_changed", alter)

    def test_changed_input_refused(self):
        def alter(module, root):
            (root / "capture.mp4").write_bytes(b"autre capture")

        self.refused("asset_changed:capture.mp4", alter)

    def test_changed_output_reference_refused(self):
        def alter(module, root):
            path = root / module.GUARD.reference_ref
            path.write_text(path.read_text() + "\n")

        self.refused("output_reference_changed", alter)


class InvalidOutputTests(unittest.TestCase):
    """Films invalides par leur forme, réencodés depuis le brouillon témoin."""

    def refused(self, reason, *encoding):
        for name in FILMS:
            with self.subTest(film=name), tempfile.TemporaryDirectory() as tmp:
                module, draft = load(name)
                target = Path(tmp) / "film.mp4"
                ffmpeg("-i", str(draft), *encoding, str(target))
                with self.assertRaisesRegex(ValueError, reason):
                    module.validate_output(target)

    def test_smaller_picture_refused(self):
        self.refused("output_video_invalid", "-vf", "scale=1280:720", "-c:v", "libx264", "-preset", "ultrafast",
                     "-pix_fmt", "yuv420p", "-c:a", "copy")

    def test_other_frame_rate_refused(self):
        self.refused("output_framerate_invalid", "-vf",
            "fps=20", "-c:v", "libx264", "-preset", "ultrafast",
                     "-pix_fmt", "yuv420p", "-c:a", "copy")

    def test_other_audio_codec_refused(self):
        self.refused("output_audio_invalid", "-c:v", "copy", "-c:a",
            "libmp3lame")

    def test_reencoded_picture_refused(self):
        self.refused("output_video_changed", "-vf", "hue=s=0", "-c:v", "libx264", "-preset", "ultrafast",
                     "-pix_fmt", "yuv420p", "-c:a", "copy")

    def test_reencoded_sound_refused(self):
        self.refused("output_audio_changed", "-c:v", "copy", "-af", "volume=0.5", "-c:a", "aac")


class ApprovedFilmTests(unittest.TestCase):
    """Issue 15, constats 8 et 9 : film approuvé à reproduire, film révoqué à ne pas rendre."""

    def test_render_must_reproduce_the_approved_film(self):
        for name in FILMS:
            with self.subTest(film=name):
                module, draft = load(name)
                fiche = module.load_fiche()
                fiche["film"]["output_sha256"] = "0" * 64
                with mock.patch.object(module, "load_fiche", return_value=fiche):
                    with self.assertRaisesRegex(ValueError, "output_differs_from_approved_film"):
                        module.validate_output(draft)

    def test_draft_without_fingerprint_is_not_compared(self):
        for name in FILMS:
            with self.subTest(film=name):
                module, draft = load(name)
                fiche = module.load_fiche()
                fiche["film"]["output_sha256"] = None
                with mock.patch.object(module, "load_fiche", return_value=fiche):
                    self.assertTrue(module.validate_output(draft))

    def test_revoked_film_is_not_rendered(self):
        for name in FILMS:
            with self.subTest(film=name), tempfile.TemporaryDirectory() as tmp:
                module, _ = load(name)
                root = copied_inputs(module, tmp)
                fiche = module.load_fiche()
                fiche["film"]["approval"]["status"] = "REVOKED"
                with mock.patch.object(module, "load_fiche", return_value=fiche):
                    with self.assertRaisesRegex(ValueError, "fiche_revoked"):
                        module.preflight(root / "baseline.html", root / "index.html")


if __name__ == "__main__":
    unittest.main()
