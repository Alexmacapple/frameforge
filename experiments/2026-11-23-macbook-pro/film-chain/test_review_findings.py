"""Constats de la revue ShipGuard du 23 novembre 2026, un test par motif corrigé.

Chaque test rejoue le cas signalé sur une copie du film de réservation : fichiers texte copiés,
médias liés, rien n'est écrit dans le dossier du film. Les identifiants (r1-z01-003…) renvoient au
rapport de la revue ; « logique » désigne l'audit de bout en bout qui l'a complétée.
"""

import contextlib
import importlib
import importlib.util
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
m = importlib.import_module("check_manifest")
b = importlib.import_module("build_from_fiche")
r = importlib.import_module("repin")
film_guard = importlib.import_module("film_guard")
SOURCE = CHAIN.parent / "ff04-room-booking-film"
TEXT = (".json", ".html", ".srt", ".vtt", ".txt", ".md", ".py")


def load_guard(root):
    spec = importlib.util.spec_from_file_location(
        f"guard_{root.name}", root / "render_guarded.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FilmCopy(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        # Même nom de dossier que le film : son garde retrouve film-chain par le dossier parent.
        self.root = Path(tmp.name) / "experiments" / SOURCE.name
        self.root.mkdir(parents=True)
        (self.root.parent / "film-chain").symlink_to(CHAIN)
        (self.root.parent / "ff10-hyperframes-guarded-integration").symlink_to(
            CHAIN.parent / "ff10-hyperframes-guarded-integration"
        )
        for path in SOURCE.iterdir():
            if path.is_file() and path.suffix in TEXT:
                (self.root / path.name).write_bytes(path.read_bytes())
            elif not path.name.startswith(".") and path.name != "__pycache__":
                (self.root / path.name).symlink_to(path)

    def fiche(self):
        return json.loads((self.root / "provenance-manifest.json").read_text())

    def details(self, change=None, events=None):
        data = self.fiche()
        if change:
            change(data)
        return {
            x["check"]: (x["status"], x["detail"])
            for x in m.check_data(data, self.root, events=events)
            if x["check"] != "open_check"
        }

    def expect(self, check, text, change=None, events=None, status="FAIL"):
        got = self.details(change, events)[check]
        self.assertEqual(got[0], status, got)
        self.assertIn(text, got[1])

    def edit(self, name, old, new, count=1):
        path = self.root / name
        text = path.read_text()
        self.assertEqual(len(re.findall(old, text)), count, f"{old} dans {name}")
        path.write_text(re.sub(old, new, text))


class ShapeTests(FilmCopy):
    """r1-z01-006, 008, 015, 036 et r1-z02-008, 009 : une valeur mal formée est un refus nommé."""

    def test_copy_of_the_real_film_has_no_failure(self):
        self.assertEqual([c for c, (s, _) in self.details().items() if s == "FAIL"], [])

    def test_wrong_shapes_are_refused_by_name_not_by_a_crash(self):
        cases = (
            ("start_s", lambda d: d["scenes"][0]["narration"].update(start_s="1.5")),
            ("start_s", lambda d: d["scenes"][0]["narration"].update(start_s=None)),
            ("duration_s", lambda d: d["film"].update(duration_s=True)),
            ("scenes", lambda d: d.update(scenes=[])),
            ("caption_refs", lambda d: d["film"].update(caption_refs="captions.srt")),
            ("output_sha256", lambda d: d["film"].update(output_sha256="e")),
            ("inputs_sha256", lambda d: d["film"].update(inputs_sha256=12)),
            (
                "transcript_ref",
                lambda d: d["film"].update(transcript_ref="../ailleurs.txt"),
            ),
            ("media_ref", lambda d: d["capture"].update(media_ref="/tmp/capture.mp4")),
            ("text", lambda d: d["scenes"][0]["narration"].update(text="Phrase. ")),
            ("text", lambda d: d["scenes"][0]["narration"].update(text="Une\ndeux")),
            ("gesture_events", lambda d: d["scenes"][0].update(gesture_events=None)),
        )
        for field, change in cases:
            with self.subTest(field=field):
                data = self.fiche()
                change(data)
                results = m.check_data(data, self.root)
                self.assertEqual(
                    [(x["check"], x["status"]) for x in results], [("schema", "FAIL")]
                )
                self.assertIn("valeur de forme inattendue", results[0]["detail"])
                self.assertIn(field, results[0]["detail"])

    def test_version_must_be_the_integer_1_2_or_3(self):
        for version in (True, 1.0, 2.0, 3.0, "1", 4, 0, None):
            with self.subTest(version=version):
                self.expect(
                    "schema",
                    "version de fiche inconnue",
                    lambda d, v=version: d.update(manifest_version=v),
                )

    def test_unknown_field_is_named(self):
        self.expect("schema", "humeur", lambda d: d["scenes"][0].update(humeur="calme"))


class PinnedTests(FilmCopy):
    """r1-z01-007 : figé ne suffit pas, l'empreinte doit être celle du fichier."""

    def test_pinned_fingerprint_that_is_not_the_file_is_refused(self):
        self.edit(
            "input-pins.json", r'("voice1\.wav": ")[0-9a-f]{64}', r"\g<1>" + "0" * 64
        )
        self.expect(
            "pinned_media", "voice1.wav : empreinte figée différente du fichier"
        )

    def test_missing_pinned_file_is_unverified_not_passed(self):
        (self.root / "voice1.wav").unlink()
        self.expect(
            "pinned_media",
            "fichiers figés absents en local : voice1.wav",
            status="UNVERIFIED",
        )


class TextFileTests(FilmCopy):
    def test_line_added_under_a_subtitle_is_seen(self):
        # r1-z01-009 et r1-z02-002 : seul le motif des sous-titres doit parler.
        self.edit("captions.srt", r"\A(1\n[^\n]+\n[^\n]+\n)", r"\g<1>Ligne ajoutée.\n")
        status, detail = self.details()["texts"]
        self.assertEqual((status, detail), ("FAIL", "captions.srt : texte différent"))

    def test_unreadable_timing_line_is_not_skipped(self):
        self.edit("captions.vtt", r"00:00:01\.500 --> ", "00:00:01.500 -> --> ")
        self.expect("captions", "captions.vtt : repères différents de la fiche")


class CompositionTests(FilmCopy):
    def test_embedded_subtitle_duration_is_compared(self):
        # r1-z01-003
        self.edit(
            "index.html",
            r'(id="caption1" class="clip" data-start="[\d.]+" data-duration=")[\d.]+',
            r"\g<1>0.1",
        )
        self.expect("composition", "sous-titres incrustés différents de la fiche")

    def test_audio_track_with_reordered_attributes_is_seen(self):
        # r1-z01-005
        self.edit(
            "index.html",
            r"</div></body>",
            '<audio data-start="1" src="autre.wav"></audio></div></body>',
        )
        self.expect("composition", "piste audio non reconnue dans la composition")

    def test_second_or_other_video_is_seen(self):
        self.edit(
            "index.html",
            r"</div></body>",
            '<video src="autre.mp4"></video></div></body>',
        )
        self.expect(
            "composition", "la composition ne montre pas la seule capture de la fiche"
        )
        self.setUp()
        self.edit("index.html", r'src="capture\.mp4"', 'src="autre.mp4"')
        self.expect(
            "composition", "la composition ne montre pas la seule capture de la fiche"
        )

    def test_text_with_markup_characters_is_accepted_once_generated(self):
        # r1-z01-004 : le texte est écrit échappé, il se compare lisible.
        said = "Salle A & B : <12 places>"

        def change(d):
            d["scenes"][0]["narration"]["text"] = said

        data = self.fiche()
        change(data)
        for name, text in b.render(data).items():
            (self.root / name).write_text(text)
        got = self.details(change)
        self.assertEqual(
            (got["composition"][0], got["texts"][0]), ("PASS", "PASS"), got
        )


class JournalTests(FilmCopy):
    def test_malformed_journal_is_reported_and_nothing_is_taken_as_observed(self):
        # r1-z01-012
        for journal in (
            {},
            {"events": [{"name": 1}], "observed": {}},
            {"events": [], "observed": []},
            [],
        ):
            with self.subTest(journal=journal):
                got = self.details(events=journal)
                self.assertEqual(got["gestures"][0], "FAIL", got["gestures"])
                self.assertIn(
                    "journal de capture de forme inattendue", got["gestures"][1]
                )
                self.assertIn(
                    "journal de capture de forme inattendue", got["results"][1]
                )

    def test_no_observed_scene_is_not_reported_as_all_results_matching(self):
        # r1-z01-037
        def change(d):
            d["film"]["approval"] = {"status": "DRAFT", "ref": None}
            for scene in d["scenes"]:
                scene["evidence_status"] = "planned"

        self.expect(
            "results", "aucune scène déclarée observée", change, status="UNVERIFIED"
        )


class ApprovalTests(FilmCopy):
    def test_data_file_is_not_an_approval_document(self):
        # r1-z02-007
        sha = self.fiche()["film"]["output_sha256"]
        (self.root / "approbation.json").write_text(json.dumps({"approuvé": sha}))
        self.expect(
            "approval",
            "fichier de données, pas une trace humaine",
            lambda d: d["film"]["approval"].update(ref="approbation.json"),
        )

    def test_composition_or_journal_is_not_an_approval_document(self):
        # r1-z01-014
        for name in ("index.html", "capture-events.json"):
            with self.subTest(document=name):
                self.expect(
                    "approval",
                    "fichier cité ou figé par la fiche",
                    lambda d, n=name: d["film"]["approval"].update(ref=n),
                )


class MeasuredAudioTests(FilmCopy):
    def test_unreadable_clip_is_a_named_failure(self):
        # r1-z01-011
        for failure in (
            subprocess.CalledProcessError(1, ["ffprobe"]),
            subprocess.TimeoutExpired(["ffprobe"], 30),
        ):
            with (
                self.subTest(failure=type(failure).__name__),
                mock.patch.object(m.subprocess, "check_output", side_effect=failure),
            ):
                self.expect(
                    "measured_audio", "voice1.wav : durée illisible par ffprobe"
                )


class GenerationTests(FilmCopy):
    def test_generation_refuses_to_write_over_an_input_or_outside_the_film(self):
        # r1-z01-002
        cases = (
            lambda d: d["film"].update(transcript_ref="capture.mp4"),
            lambda d: d["film"].update(transcript_ref="voice1.wav"),
            lambda d: d["film"].update(composition_ref="../index.html"),
            lambda d: d["film"].update(caption_refs=["provenance-manifest.json"]),
            lambda d: d["film"].update(transcript_ref="index.html"),
            lambda d: d["film"].update(transcript_ref="notes.md"),
        )
        for change in cases:
            data = self.fiche()
            change(data)
            with (
                self.subTest(film=data["film"]),
                self.assertRaisesRegex(ValueError, "nom de fichier généré refusé"),
            ):
                b.render(data)

    def test_subtitle_format_the_generator_does_not_know_is_refused(self):
        data = self.fiche()
        data["film"]["caption_refs"] = ["sous-titres.txt"]
        with self.assertRaisesRegex(
            ValueError, "format de sous-titres non pris en charge"
        ):
            b.render(data)

    def test_times_keep_the_thousandth_whatever_their_size(self):
        # r1-z01-016
        self.assertEqual(
            [b.number(v) for v in (10, 2.78, 0.2, -10, 1234.5678, 3600.001, 0)],
            ["10", "2.78", "0.2", "-10", "1234.568", "3600.001", "0"],
        )

    def run_cli(self, module, *args):
        out = io.StringIO()
        with (
            mock.patch.object(sys, "argv", ["outil", *args]),
            contextlib.redirect_stdout(out),
        ):
            return module.main(), out.getvalue()

    def snapshot(self):
        return {
            p.name: p.read_bytes()
            for p in self.root.iterdir()
            if p.is_file() and not p.is_symlink()
        }

    def test_mistyped_option_writes_nothing(self):
        # r1-z01-018 et 019 : la fiche est d'abord rendue périmée, pour qu'une écriture se voie.
        self.edit("transcript.txt", r"\A", "Ligne en trop.\n")
        before = self.snapshot()
        fiche = str(self.root / "provenance-manifest.json")
        for module, args in (
            (b, ("--chek", fiche)),
            (r, (str(self.root), "--chek")),
            (r, (str(self.root), "--record_output")),
        ):
            with self.subTest(outil=module.__name__, args=args[-1]):
                code, _ = self.run_cli(module, *args)
                self.assertEqual(code, 2)
                self.assertEqual(before, self.snapshot())

    def test_generation_refuses_a_fiche_its_schema_rejects(self):
        # r1-z01-020
        self.edit(
            "provenance-manifest.json",
            r'"manifest_version": 1',
            '"manifest_version": 7',
        )
        self.edit("transcript.txt", r"\A", "Ligne en trop.\n")
        before = self.snapshot()
        code, said = self.run_cli(b, str(self.root / "provenance-manifest.json"))
        self.assertEqual((code, json.loads(said)["status"]), (2, "BLOCKED"))
        self.assertEqual(before, self.snapshot())

    def test_check_still_reports_stale_files_and_writing_still_writes(self):
        self.edit("transcript.txt", r"\A", "Ligne en trop.\n")
        fiche = str(self.root / "provenance-manifest.json")
        self.assertEqual(self.run_cli(b, "--check", fiche)[0], 1)
        self.assertEqual(self.run_cli(b, fiche)[0], 0)
        self.assertEqual(self.run_cli(b, "--check", fiche)[0], 0)


class RepinTests(FilmCopy):
    def run_repin(self, *args):
        out = io.StringIO()
        with (
            mock.patch.object(sys, "argv", ["repin.py", *args]),
            contextlib.redirect_stdout(out),
        ):
            return r.main(), out.getvalue()

    def test_command_line_reports_fresh_stale_and_unreadable(self):
        # r1-z02-011
        self.assertEqual(self.run_repin(str(self.root), "--check")[0], 0)
        self.edit("transcript.txt", r"\A", "Ligne en trop.\n")
        code, said = self.run_repin(str(self.root), "--check")
        self.assertEqual((code, json.loads(said)["status"]), (1, "FAIL"))
        self.assertEqual(self.run_repin()[0], 2)
        (self.root / "provenance-manifest.json").write_text("{}")
        (self.root / "media").unlink()
        (self.root / "media").mkdir()
        (self.root / "media/room-booking.mp4").write_bytes(b"film")
        code, said = self.run_repin(str(self.root), "--record-output")
        self.assertEqual((code, json.loads(said)["status"]), (2, "BLOCKED"))

    def test_nothing_stale_means_nothing_rewritten(self):
        # Audit logique : --check disait PASS, puis repin réécrivait sans le dire.
        pins = self.root / "input-pins.json"
        compact = json.dumps(json.loads(pins.read_text()))
        pins.write_text(compact)
        self.edit(
            "render_guarded.py",
            r'(PIN_MANIFEST_SHA256 = ")[0-9a-f]{64}',
            r"\g<1>" + r.sha(pins),
        )
        self.assertEqual(r.stale(self.root), [])
        self.assertEqual(r.refresh(self.root), [])
        self.assertEqual(pins.read_text(), compact)

    def test_revoked_film_is_not_recorded(self):
        # Audit logique : record-output inscrivait les empreintes sur une fiche révoquée.
        self.edit(
            "provenance-manifest.json", r'"status": "REVIEWED"', '"status": "REVOKED"'
        )
        r.refresh(self.root)
        before = (self.root / "provenance-manifest.json").read_bytes()
        output = self.root / "media/room-booking.mp4"
        receipt = Path(str(output) + ".receipt.json")
        pins = {
            n: r.sha(self.root / n)
            for n in json.loads((self.root / "input-pins.json").read_text())
        }
        with (
            tempfile.TemporaryDirectory() as tmp,
            mock.patch.object(
                r, "receipt_path", return_value=Path(tmp) / "recu.json"
            ) as where,
        ):
            where.return_value.write_text(
                json.dumps(
                    {
                        "output_sha256": r.sha(output),
                        "inputs_sha256": r.inputs_fingerprint(pins),
                    }
                )
            )
            with self.assertRaisesRegex(ValueError, "approbation retirée"):
                r.record_output(self.root, validate=lambda path: True)
        self.assertEqual(before, (self.root / "provenance-manifest.json").read_bytes())
        self.assertFalse(receipt.exists() and receipt.parent == self.root)


class GuardAndFicheTests(FilmCopy):
    """r1-z01-013, r1-z03-014 et audit logique : le garde et la fiche parlent des mêmes fichiers."""

    def refused(self, reason, change):
        guard = load_guard(self.root)
        fiche = guard.load_fiche()
        change(fiche)
        with (
            mock.patch.object(guard, "load_fiche", return_value=fiche),
            mock.patch.object(guard, "fiche_failures", return_value=[]),
            mock.patch.object(guard.fiche_build, "stale_files", return_value=[]),
            self.assertRaisesRegex(ValueError, reason),
        ):
            guard.preflight(self.root / "baseline.html", self.root / "index.html")

    def test_untouched_copy_passes_the_preflight(self):
        guard = load_guard(self.root)
        self.assertTrue(
            guard.preflight(self.root / "baseline.html", self.root / "index.html")
        )

    def test_fiche_checked_against_another_pins_file_is_refused(self):
        self.refused(
            "guard_differs_from_fiche:pins_ref",
            lambda d: d.update(pins_ref="copie-des-empreintes.json"),
        )

    def test_fiche_naming_another_output_is_refused(self):
        self.refused(
            "guard_differs_from_fiche:output",
            lambda d: d["film"].update(output_ref="media/autre.mp4"),
        )

    def test_fiche_citing_a_clip_the_guard_does_not_carry_is_refused(self):
        self.refused(
            "guard_differs_from_fiche:media",
            lambda d: d["scenes"][0]["narration"].update(
                audio_ref="voix-non-figee.wav"
            ),
        )

    def test_erasing_the_inputs_fingerprint_does_not_reopen_the_render(self):
        self.refused(
            "approval_not_tied_to_inputs",
            lambda d: d["film"].update(inputs_sha256=None),
        )

    def test_draft_without_inputs_fingerprint_is_rendered(self):
        guard = load_guard(self.root)
        fiche = guard.load_fiche()
        fiche["film"].update(inputs_sha256=None, output_sha256=None)
        fiche["film"]["approval"] = {"status": "DRAFT", "ref": None}
        with (
            mock.patch.object(guard, "load_fiche", return_value=fiche),
            mock.patch.object(guard, "fiche_failures", return_value=[]),
        ):
            self.assertTrue(
                guard.preflight(self.root / "baseline.html", self.root / "index.html")
            )


if __name__ == "__main__":
    unittest.main()
