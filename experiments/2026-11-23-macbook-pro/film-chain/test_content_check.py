"""Contrôle du contenu du brouillon témoin (ticket 78).

Les témoins d'essai sont fabriqués par FFmpeg : quatre secondes, deux phrases, la première de
0,5 à 1,5 s, la seconde de 2,5 à 3,5 s. Aucun rendu HyperFrames n'est lancé.
"""

import importlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
content = importlib.import_module("content_check")

EXPERIMENTS = CHAIN.parent
MOVING = "testsrc2=size=320x180:rate=30:duration=4"
BLACK = "color=c=black:size=320x180:rate=30:duration=4"
STILL = "color=c=0x336699:size=320x180:rate=30:duration=4"
# Un son pendant chaque créneau de phrase, le silence ailleurs.
# Dans un graphe de filtres, la virgule sépare les filtres : celles des formules sont protégées.
BOTH_VOICES = r"between(t\,0.5\,1.5)+between(t\,2.5\,3.5)"
FIRST_VOICE_ONLY = r"between(t\,0.5\,1.5)"
NO_VOICE = "0"
NARRATIONS = [
    {"start_s": 0.5, "duration_s": 1.0},
    {"start_s": 2.5, "duration_s": 1.0},
]
APPROVED = (
    ("ff04-room-booking-film", "media/room-booking-draft.mp4"),
    ("ff47-film-fenetres-modales", "media/fenetres-modales-draft.mp4"),
    ("ff59-film-fenetres-modales-recap", "media/fenetres-modales-recap-draft.mp4"),
    (
        "ff10-second-web-demo-transfer/form-pilot-kokoro",
        "media/form-kokoro-pointeur-draft.mp4",
    ),
)


def witness(target, picture=MOVING, voices=BOTH_VOICES, sound=True):
    """Fabrique un témoin d'essai : une image, et un son présent là où « voices » vaut 1."""
    command = ["ffmpeg", "-v", "error", "-f", "lavfi", "-i", picture]
    if sound:
        command += [
            "-f",
            "lavfi",
            "-i",
            f"aevalsrc=0.4*sin(2*PI*220*t)*({voices}):d=4:s=48000",
            "-c:a",
            "aac",
        ]
    command += ["-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p"]
    subprocess.run([*command, str(target)], check=True)
    return target


def film(root, narrations=NARRATIONS):
    scenes = [
        {"narration": dict(n, text="phrase", audio_ref="v.wav")} for n in narrations
    ]
    (root / "provenance-manifest.json").write_text(
        json.dumps({"film": {"duration_s": 4}, "scenes": scenes})
    )
    return root


def measured(**changes):
    """Mesure d'un témoin sain, dont un test change un seul point."""
    out = {
        "duration_s": 4.0,
        "black_s": 0.0,
        "longest_still_s": 1.2,
        "lufs": -20.0,
        "silences": [(0.0, 0.5), (1.5, 2.5), (3.5, 4.0)],
    }
    out.update(changes)
    return out


class Verdict(unittest.TestCase):
    def reasons(self, **changes):
        return content.failures(measured(**changes), NARRATIONS)

    def test_healthy_witness_is_accepted(self):
        self.assertEqual(self.reasons(), [])

    def test_silent_film_is_refused(self):
        self.assertEqual(
            self.reasons(lufs=float("-inf"), silences=[(0.0, 4.0)]),
            ["son_muet", "voix_absente:1", "voix_absente:2"],
        )

    def test_barely_audible_film_is_refused(self):
        self.assertIn("son_muet", self.reasons(lufs=-61.0))

    def test_quiet_but_audible_film_is_accepted(self):
        self.assertEqual(self.reasons(lufs=-35.0), [])

    def test_sentence_without_voice_is_named_by_its_rank(self):
        self.assertEqual(
            self.reasons(silences=[(0.0, 0.5), (1.5, 4.0)]), ["voix_absente:2"]
        )

    def test_pause_inside_a_sentence_is_not_an_absent_voice(self):
        # Une demi-seconde de silence dans une phrase d'une seconde : la voix est là.
        self.assertEqual(
            self.reasons(silences=[(0.0, 0.5), (0.8, 1.3), (1.5, 2.5)]), []
        )

    def test_mostly_silent_sentence_is_refused(self):
        self.assertEqual(
            self.reasons(silences=[(0.0, 1.4), (1.5, 2.5)]), ["voix_absente:1"]
        )

    def test_mostly_black_film_is_refused(self):
        self.assertEqual(self.reasons(black_s=2.4), ["image_noire:60"])

    def test_short_black_opening_is_accepted(self):
        self.assertEqual(self.reasons(black_s=0.5), [])

    def test_single_still_over_the_whole_film_is_refused(self):
        self.assertEqual(self.reasons(longest_still_s=3.9), ["image_figee:98"])

    def test_long_still_of_a_screen_capture_is_accepted(self):
        # Mesuré sur les films approuvés : le plus long plan fixe tient jusqu'à 34 % du film.
        self.assertEqual(self.reasons(longest_still_s=2.0), [])

    def test_several_reasons_are_all_returned(self):
        self.assertEqual(
            self.reasons(black_s=4.0, longest_still_s=4.0, lufs=-70.0),
            ["son_muet", "image_noire:100", "image_figee:100"],
        )

    def test_film_without_sentences_is_only_judged_on_its_whole(self):
        self.assertEqual(content.failures(measured(), []), [])


class RealWitness(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = film(Path(tmp.name))

    def run_check(self, **options):
        return content.run(self.root, witness(self.root / "draft.mp4", **options))

    def test_healthy_witness_is_accepted(self):
        self.assertEqual(self.run_check(), [])

    def test_silent_witness_is_refused(self):
        self.assertEqual(
            self.run_check(voices=NO_VOICE),
            ["son_muet", "voix_absente:1", "voix_absente:2"],
        )

    def test_witness_missing_the_second_voice_is_refused(self):
        self.assertEqual(self.run_check(voices=FIRST_VOICE_ONLY), ["voix_absente:2"])

    def test_black_witness_is_refused(self):
        # Un écran noir est aussi une image figée : les deux motifs sont rendus.
        reasons = self.run_check(picture=BLACK)
        self.assertEqual(len(reasons), 2)
        self.assertRegex(reasons[0], r"^image_noire:(9\d|100)$")
        self.assertRegex(reasons[1], r"^image_figee:(9\d|100)$")

    def test_still_witness_is_refused(self):
        reasons = self.run_check(picture=STILL)
        self.assertEqual(len(reasons), 1)
        self.assertRegex(reasons[0], r"^image_figee:(9\d|100)$")

    def test_witness_without_any_sound_track_is_refused(self):
        self.assertEqual(self.run_check(sound=False), ["son_illisible"])

    def test_sound_without_any_picture_is_refused(self):
        target = self.root / "son.m4a"
        subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-f",
                "lavfi",
                "-i",
                "sine=frequency=220:duration=4",
                "-c:a",
                "aac",
                str(target),
            ],
            check=True,
        )
        self.assertEqual(content.run(self.root, target), ["temoin_illisible"])

    def test_file_that_is_not_a_film_is_refused(self):
        (self.root / "draft.mp4").write_text("pas un film")
        self.assertEqual(
            content.run(self.root, self.root / "draft.mp4"), ["temoin_illisible"]
        )


class WitnessReference(unittest.TestCase):
    """Un témoin refusé ne devient pas la référence du film."""

    def reference(self, **options):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = film(Path(tmp.name))
        draft = witness(root / "draft.mp4", **options)
        done = subprocess.run(
            [
                sys.executable,
                "-B",
                str(CHAIN / "witness_reference.py"),
                str(root),
                "--from",
                str(draft),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        return done, root

    def test_healthy_witness_becomes_the_reference(self):
        done, root = self.reference()
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertTrue((root / "output-reference.json").is_file())

    def test_silent_witness_never_becomes_the_reference(self):
        done, root = self.reference(voices=NO_VOICE)
        self.assertEqual(done.returncode, 2, done.stdout + done.stderr)
        self.assertIn("son_muet", done.stdout)
        self.assertFalse((root / "output-reference.json").exists())

    def test_witness_missing_one_voice_never_becomes_the_reference(self):
        done, root = self.reference(voices=FIRST_VOICE_ONLY)
        self.assertEqual(done.returncode, 2, done.stdout + done.stderr)
        self.assertIn("voix_absente:2", done.stdout)
        self.assertFalse((root / "output-reference.json").exists())


class ApprovedFilms(unittest.TestCase):
    def test_witnesses_of_the_chain_are_accepted(self):
        seen = 0
        for folder, draft in APPROVED:
            root = EXPERIMENTS / folder
            if not (root / draft).is_file():
                continue
            seen += 1
            with self.subTest(film=folder):
                self.assertEqual(content.run(root, root / draft), [])
        if not seen:
            self.skipTest("aucun brouillon témoin en local")


if __name__ == "__main__":
    unittest.main()
