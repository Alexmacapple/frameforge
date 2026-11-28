"""Synthèse Libra-TTS : refus avant toute écriture, et une vraie synthèse si l'outil est installé.

Les refus se testent sans le modèle, avec un faux moteur. La vraie synthèse demande `.venv-libra`
et le modèle figé (voir le README) ; sans eux, elle est sautée.
"""

import hashlib
import importlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
libra = importlib.import_module("synthesize_libra")

SENTENCES = (
    "La salle Érable est choisie parmi les trois salles.",
    "L'option vidéoprojecteur est cochée.",
)
VENV_PYTHON = CHAIN.parents[2] / ".venv-libra" / "bin" / "python"


def film(root, refs=("voice1.wav", "voice2.wav")):
    """Dossier de film réduit à sa fiche : une scène par phrase."""
    scenes = [
        {"narration": {"text": text, "audio_ref": ref}}
        for text, ref in zip(SENTENCES, refs)
    ]
    (root / "provenance-manifest.json").write_text(
        json.dumps({"scenes": scenes}, ensure_ascii=False)
    )
    return root


def fake_model(root, content=b"poids"):
    """Dossier de modèle factice, et les empreintes qui lui correspondent."""
    root.mkdir()
    expected = {}
    for name in libra.MODEL_SHA256:
        (root / name).parent.mkdir(exist_ok=True)
        (root / name).write_bytes(content + name.encode())
        expected[name] = hashlib.sha256(content + name.encode()).hexdigest()
    return root, expected


def tone(target, source="sine=frequency=220:duration=2", volume="0.5"):
    """Écrit un vrai fichier son, fabriqué par FFmpeg, à la place d'une voix."""
    subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-f",
            "lavfi",
            "-i",
            source,
            "-af",
            f"volume={volume}",
            "-ar",
            "24000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s16le",
            str(target),
        ],
        check=True,
    )


class FakeEngine:
    """Écrit un son de synthèse à la place de la voix, et compte ses appels.

    volumes donne le volume de chaque clip, dans l'ordre : un moteur qui ne sort pas deux phrases
    au même niveau, comme Libra-TTS.
    La source « sine » de FFmpeg sort à un huitième de l'amplitude : volume 6 donne un son fort.
    """

    def __init__(self, volumes=("6", "6"), source="sine=frequency=220:duration=2"):
        self.calls = []
        self.volumes = list(volumes)
        self.source = source

    def write(self, target, text, voice):
        self.calls.append((target.name, voice))
        tone(target, self.source, self.volumes[len(self.calls) - 1])
        return 2.0


class FilmCase(unittest.TestCase):
    """Un film réduit à sa fiche, un modèle factice et un faux moteur."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.model, self.expected = fake_model(self.root / "modele")
        (self.root / "film").mkdir()
        self.film = film(self.root / "film")
        self.engine = FakeEngine()

    def run_synthesis(self, **changes):
        options = {
            "film": self.film,
            "model": self.model,
            "voice": "nina",
            "load": lambda model: self.engine,
            "expected": self.expected,
        }
        options.update(changes)
        return libra.synthesize(**options)

    def written(self):
        return sorted(
            p.name for p in self.film.iterdir() if p.name != "provenance-manifest.json"
        )

    def refused(self, reason, **changes):
        with self.assertRaisesRegex(ValueError, reason):
            self.run_synthesis(**changes)
        self.assertEqual(self.engine.calls, [])


class RefusalTests(FilmCase):
    def test_untouched_film_is_synthesized_and_reported(self):
        report = self.run_synthesis()
        self.assertEqual(
            self.engine.calls, [("voice1.wav", "nina"), ("voice2.wav", "nina")]
        )
        self.assertEqual(
            self.written(), ["narration-synthesis.json", "voice1.wav", "voice2.wav"]
        )
        on_disk = json.loads((self.film / "narration-synthesis.json").read_text())
        self.assertEqual(on_disk, report)
        self.assertEqual(report["engine"], "libra-tts")
        self.assertEqual(report["model_revision"], libra.MODEL_REVISION)
        self.assertEqual(report["code_commit"], libra.CODE_COMMIT)
        self.assertEqual([c["text"] for c in report["clips"]], list(SENTENCES))
        for clip in report["clips"]:
            self.assertEqual(
                clip["sha256"],
                hashlib.sha256(
                    (self.film / clip["audio_ref"]).read_bytes()
                ).hexdigest(),
            )

    def test_existing_clip_is_never_overwritten(self):
        (self.film / "voice2.wav").write_bytes(b"clip approuve")
        self.refused("clip_deja_present:voice2.wav")
        self.assertEqual((self.film / "voice2.wav").read_bytes(), b"clip approuve")
        # Le premier clip, lui, était libre : rien n'est écrit tant que tout n'est pas libre.
        self.assertEqual(self.written(), ["voice2.wav"])

    def test_existing_report_is_never_overwritten(self):
        (self.film / "narration-synthesis.json").write_text("{}")
        self.refused("rapport_deja_present")
        self.assertEqual((self.film / "narration-synthesis.json").read_text(), "{}")

    def test_clip_outside_the_film_is_refused(self):
        for ref in ("../voice1.wav", "media/voice1.wav", "/tmp/voice1.wav", ""):
            with self.subTest(ref=ref):
                film(self.film, refs=(ref, "voice2.wav"))
                self.refused("nom_de_clip_refuse")

    def test_clip_through_a_link_is_refused(self):
        (self.film / "voice1.wav").symlink_to(self.root / "ailleurs.wav")
        self.refused("clip_deja_present:voice1.wav")
        self.assertFalse((self.root / "ailleurs.wav").exists())

    def test_two_scenes_naming_the_same_clip_are_refused(self):
        film(self.film, refs=("voice1.wav", "voice1.wav"))
        self.refused("clip_cite_deux_fois:voice1.wav")

    def test_unknown_voice_is_refused(self):
        self.refused("voix_inconnue:siwis", voice="siwis")

    def test_model_with_other_weights_is_refused(self):
        name = min(libra.MODEL_SHA256)
        (self.model / name).write_bytes(b"autres poids")
        self.refused(f"modele_different:{name}")

    def test_model_with_a_missing_file_is_refused(self):
        name = max(libra.MODEL_SHA256)
        (self.model / name).unlink()
        self.refused(f"modele_absent:{name}")

    def test_film_without_fiche_is_refused(self):
        (self.film / "provenance-manifest.json").unlink()
        self.refused("fiche_absente")

    def test_engine_that_writes_nothing_is_a_failure(self):
        class Mute(FakeEngine):
            def write(self, target, text, voice):
                self.calls.append((target.name, voice))
                return 0.0

        self.engine = Mute()
        with self.assertRaisesRegex(ValueError, "aucun_son:voice1.wav"):
            self.run_synthesis()
        self.assertNotIn("narration-synthesis.json", self.written())

    def test_every_file_the_engine_reads_is_frozen(self):
        # Poids, configuration, découpage du texte et lexiques : sept fichiers, sept empreintes.
        self.assertEqual(len(libra.MODEL_SHA256), 7)
        self.assertIn("model.safetensors", libra.MODEL_SHA256)
        self.assertIn("tokenizer.json", libra.MODEL_SHA256)
        for digest in libra.MODEL_SHA256.values():
            self.assertRegex(digest, r"^[0-9a-f]{64}$")


class LevelTests(FilmCase):
    """Chaque clip est ramené au niveau de Kokoro par un réglage de volume seul."""

    def clip(self, report, rank):
        return report["clips"][rank]

    def test_loud_clip_is_brought_down_to_the_target(self):
        report = self.run_synthesis()
        for clip in report["clips"]:
            self.assertLess(clip["gain_db"], -3)
            self.assertGreater(clip["source_lufs"], libra.TARGET_LUFS + 3)
            self.assertAlmostEqual(clip["lufs"], libra.TARGET_LUFS, delta=0.5)
            self.assertLessEqual(clip["true_peak_dbtp"], libra.MAX_TRUE_PEAK_DBTP)

    def test_clips_of_different_levels_end_at_the_same_level(self):
        self.engine = FakeEngine(volumes=("6", "1"))
        report = self.run_synthesis()
        before = [c["source_lufs"] for c in report["clips"]]
        after = [c["lufs"] for c in report["clips"]]
        self.assertGreater(abs(before[0] - before[1]), 10)
        self.assertLess(abs(after[0] - after[1]), 0.5)

    def test_reported_level_is_the_level_of_the_clip_on_disk(self):
        report = self.run_synthesis()
        for clip in report["clips"]:
            lufs, peak = libra.measure(self.film / clip["audio_ref"])
            self.assertEqual((clip["lufs"], clip["true_peak_dbtp"]), (lufs, peak))

    def test_quiet_clip_is_raised_only_as_far_as_its_peaks_allow(self):
        # Des pointes fortes sur un fond faible : monter au niveau visé ferait saturer.
        spiky = "aevalsrc=if(lt(mod(t\\,0.25)\\,0.002)\\,0.9\\,0.004*sin(2*PI*220*t)):d=2:s=24000"
        self.engine = FakeEngine(source=spiky, volumes=("1.0", "1.0"))
        report = self.run_synthesis()
        clip = self.clip(report, 0)
        self.assertTrue(clip["peak_limited"])
        self.assertLess(clip["lufs"], libra.TARGET_LUFS - 1)
        self.assertLessEqual(clip["true_peak_dbtp"], libra.MAX_TRUE_PEAK_DBTP)

    def test_silent_clip_is_refused_and_no_report_is_written(self):
        self.engine = FakeEngine(volumes=("6", "0"))
        with self.assertRaisesRegex(ValueError, "clip_muet:voice2.wav"):
            self.run_synthesis()
        self.assertNotIn("narration-synthesis.json", self.written())

    def test_clip_does_not_name_the_ffmpeg_that_wrote_it(self):
        # Sinon le même clip changerait d'empreinte avec la version de FFmpeg (ticket 73).
        self.run_synthesis()
        for name in ("voice1.wav", "voice2.wav"):
            self.assertNotIn(b"Lavf", (self.film / name).read_bytes())

    def test_nothing_but_clips_and_report_is_left_in_the_film(self):
        self.run_synthesis()
        self.assertEqual(
            self.written(), ["narration-synthesis.json", "voice1.wav", "voice2.wav"]
        )

    def test_clip_that_is_not_sound_is_refused(self):
        class NotSound(FakeEngine):
            def write(self, target, text, voice):
                self.calls.append((target.name, voice))
                target.write_bytes(text.encode())
                return 2.0

        self.engine = NotSound()
        with self.assertRaisesRegex(ValueError, "niveau_illisible:voice1.wav"):
            self.run_synthesis()
        self.assertNotIn("narration-synthesis.json", self.written())

    def test_failed_volume_change_is_refused_and_leaves_no_partial_file(self):
        real_run = subprocess.run

        def run(command, **options):
            # Le réglage de niveau, pas le son d'essai : lui seul écrit un gain en décibels.
            if any(str(part).endswith("dB") for part in command):
                raise subprocess.CalledProcessError(1, command)
            return real_run(command, **options)

        with mock.patch.object(libra.subprocess, "run", side_effect=run):
            with self.assertRaisesRegex(ValueError, "niveau_non_regle:voice1.wav"):
                self.run_synthesis()
        self.assertEqual(self.written(), ["voice1.wav"])

    def test_peak_still_too_high_after_the_change_is_refused(self):
        # Ne doit pas arriver, le gain étant plafonné : si cela arrive, le clip n'est pas rapporté.
        with mock.patch.object(
            libra, "measure", side_effect=[(-10.0, -3.0), (-23.0, -0.5)]
        ):
            with self.assertRaisesRegex(ValueError, "crete_trop_haute:voice1.wav"):
                self.run_synthesis()
        self.assertNotIn("narration-synthesis.json", self.written())

    def test_same_sound_gives_the_same_clip_twice(self):
        self.run_synthesis()
        first = (self.film / "voice1.wav").read_bytes()
        for name in self.written():
            (self.film / name).unlink()
        self.engine = FakeEngine()
        self.run_synthesis()
        self.assertEqual((self.film / "voice1.wav").read_bytes(), first)


@unittest.skipUnless(
    VENV_PYTHON.is_file() and (libra.DEFAULT_MODEL / "config.json").is_file(),
    "Libra-TTS non installé sur ce Mac (.venv-libra ou modèle absent)",
)
class RealSynthesisTests(unittest.TestCase):
    def synthesize(self, root):
        return subprocess.run(
            [
                "sandbox-exec",
                "-p",
                "(version 1)(allow default)(deny network*)",
                str(VENV_PYTHON),
                str(CHAIN / "synthesize_libra.py"),
                str(film(root)),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=600,
        )

    def test_same_clips_twice_without_network(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            first, second = self.synthesize(Path(a)), self.synthesize(Path(b))
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            for name in ("voice1.wav", "voice2.wav"):
                clip = Path(a, name).read_bytes()
                self.assertGreater(len(clip), 24000)
                self.assertEqual(clip, Path(b, name).read_bytes())
            report = json.loads(Path(a, "narration-synthesis.json").read_text())
            self.assertEqual(report["voice"], "nina")
            self.assertTrue(all(c["duration_s"] > 1 for c in report["clips"]))

    def test_second_run_on_the_same_film_is_refused(self):
        with tempfile.TemporaryDirectory() as a:
            self.assertEqual(self.synthesize(Path(a)).returncode, 0)
            before = Path(a, "voice1.wav").read_bytes()
            again = self.synthesize(Path(a))
            self.assertEqual(again.returncode, 1, again.stdout + again.stderr)
            self.assertIn("rapport_deja_present", again.stdout)
            self.assertEqual(Path(a, "voice1.wav").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
