"""Tests de l'outil qui refige les empreintes d'un film."""

import hashlib
import importlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
r = importlib.import_module("repin")

GUARD_FILE = """PIN_MANIFEST_SHA256 = "{manifest}"
PIN_HTML_SHA256 = "{html}"
PIN_OUTPUT_REFERENCE_SHA256 = (
    "{reference}"
)
GUARD = dict(pins_ref="pins.json", reference_ref="reference.json", output="media/film.mp4")
"""


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_receipt(root, output="media/film.mp4", pins="pins.json"):
    """Reçu tel que le garde l'écrit après un rendu fait depuis les entrées présentes."""
    names = json.loads((root / pins).read_text())
    fresh = {name: sha(root / name) for name in names}
    (root / (output + ".receipt.json")).write_text(
        json.dumps(
            {
                "output_sha256": sha(root / output),
                "inputs_sha256": r.inputs_fingerprint(fresh),
            }
        )
    )


def make_film(root):
    """Petit dossier de film cohérent : deux entrées figées, une référence, une fiche, un garde."""
    (root / "index.html").write_text("<p>composition</p>\n")
    (root / "clip.wav").write_bytes(b"son")
    (root / "reference.json").write_text("{}\n")
    (root / "provenance-manifest.json").write_text(
        json.dumps({"film": {"output_sha256": None}}) + "\n"
    )
    pins = {
        name: sha(root / name)
        for name in ("index.html", "clip.wav", "provenance-manifest.json")
    }
    (root / "pins.json").write_text(json.dumps(pins, indent=2) + "\n")
    (root / "render_guarded.py").write_text(
        GUARD_FILE.format(
            manifest=sha(root / "pins.json"),
            html=sha(root / "index.html"),
            reference=sha(root / "reference.json"),
        )
    )


class RepinTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        make_film(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_consistent_film_has_nothing_stale(self):
        self.assertEqual(r.stale(self.root), [])

    def test_changed_input_is_reported_and_check_writes_nothing(self):
        (self.root / "clip.wav").write_bytes(b"autre son")
        before = (
            (self.root / "pins.json").read_bytes(),
            (self.root / "render_guarded.py").read_bytes(),
        )
        self.assertEqual(
            r.stale(self.root), ["PIN_MANIFEST_SHA256", "pins.json:clip.wav"]
        )
        self.assertEqual(
            before,
            (
                (self.root / "pins.json").read_bytes(),
                (self.root / "render_guarded.py").read_bytes(),
            ),
        )

    def test_refresh_makes_the_film_consistent_again(self):
        (self.root / "clip.wav").write_bytes(b"autre son")
        (self.root / "index.html").write_text("<p>autre composition</p>\n")
        (self.root / "reference.json").write_text('{"a": 1}\n')
        changed = r.refresh(self.root)
        self.assertEqual(r.stale(self.root), [])
        self.assertIn("PIN_OUTPUT_REFERENCE_SHA256", changed)
        self.assertIn("PIN_HTML_SHA256", changed)
        self.assertEqual(
            json.loads((self.root / "pins.json").read_text())["clip.wav"],
            sha(self.root / "clip.wav"),
        )

    def test_refresh_never_adds_or_drops_a_pinned_file(self):
        (self.root / "nouveau.txt").write_text("non déclaré\n")
        r.refresh(self.root)
        self.assertEqual(
            sorted(json.loads((self.root / "pins.json").read_text())),
            ["clip.wav", "index.html", "provenance-manifest.json"],
        )

    def test_missing_pinned_file_is_refused(self):
        (self.root / "clip.wav").unlink()
        with self.assertRaisesRegex(ValueError, "fichier figé absent : clip.wav"):
            r.refresh(self.root)

    def test_record_output_writes_the_film_fingerprint_into_the_fiche(self):
        (self.root / "media").mkdir()
        (self.root / "media/film.mp4").write_bytes(b"film")
        write_receipt(self.root)
        r.record_output(self.root, validate=lambda path: True)
        fiche = json.loads((self.root / "provenance-manifest.json").read_text())
        self.assertEqual(
            fiche["film"]["output_sha256"], sha(self.root / "media/film.mp4")
        )
        self.assertEqual(r.stale(self.root), [])

    def snapshot(self):
        return {p.name: p.read_bytes() for p in self.root.iterdir() if p.is_file()}

    def refused(self, reason):
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, reason):
            r.record_output(self.root, validate=lambda path: True)
        self.assertEqual(before, self.snapshot())

    def rendered_film(self):
        (self.root / "media").mkdir()
        (self.root / "media/film.mp4").write_bytes(b"film")
        write_receipt(self.root)

    def test_record_output_refuses_a_film_without_render_receipt(self):
        self.rendered_film()
        (self.root / "media/film.mp4.receipt.json").unlink()
        self.refused("film sans reçu de rendu")

    def test_record_output_refuses_an_input_changed_after_the_render(self):
        # Revue ShipGuard, constat r1-z01-001 : entrée modifiée après le rendu, sans nouveau rendu.
        self.rendered_film()
        (self.root / "clip.wav").write_bytes(b"autre son")
        self.refused("les entrées ont changé depuis le rendu")

    def test_refreezing_does_not_launder_an_input_changed_after_the_render(self):
        self.rendered_film()
        (self.root / "clip.wav").write_bytes(b"autre son")
        r.refresh(self.root)
        self.refused("les entrées ont changé depuis le rendu")

    def test_record_output_refuses_the_receipt_of_another_film(self):
        self.rendered_film()
        (self.root / "media/film.mp4").write_bytes(b"autre film")
        self.refused("le reçu de rendu ne correspond pas à ce film")

    def test_record_output_refuses_an_unreadable_receipt(self):
        self.rendered_film()
        for text in ("pas du json", "{}", "[]"):
            with self.subTest(receipt=text):
                (self.root / "media/film.mp4.receipt.json").write_text(text)
                self.refused("reçu de rendu illisible")

    def test_record_output_refuses_a_missing_film(self):
        with self.assertRaisesRegex(ValueError, "film absent"):
            r.record_output(self.root)

    def test_record_output_refuses_a_film_the_guard_rejects_and_writes_nothing(self):
        # Issue 15, constat 6.
        (self.root / "media").mkdir()
        (self.root / "media/film.mp4").write_bytes(b"pas un film")
        before = {p.name: p.read_bytes() for p in self.root.iterdir() if p.is_file()}

        def reject(path):
            raise ValueError("film_output_duration_invalid")

        with self.assertRaisesRegex(ValueError, "film refusé par le garde"):
            r.record_output(self.root, validate=reject)
        self.assertEqual(
            before, {p.name: p.read_bytes() for p in self.root.iterdir() if p.is_file()}
        )

    def test_record_output_writes_nothing_when_a_pinned_file_is_missing(self):
        (self.root / "media").mkdir()
        (self.root / "media/film.mp4").write_bytes(b"film")
        (self.root / "clip.wav").unlink()
        before = (self.root / "provenance-manifest.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "fichier figé absent : clip.wav"):
            r.record_output(self.root, validate=lambda path: True)
        self.assertEqual(before, (self.root / "provenance-manifest.json").read_bytes())

    def test_nothing_is_written_when_a_guard_constant_is_missing(self):
        guard = self.root / "render_guarded.py"
        guard.write_text(guard.read_text().replace("PIN_HTML_SHA256", "AUTRE_NOM"))
        (self.root / "clip.wav").write_bytes(b"autre son")
        (self.root / "media").mkdir()
        (self.root / "media/film.mp4").write_bytes(b"film")
        before = self.snapshot()
        for call in (
            lambda: r.refresh(self.root),
            lambda: r.record_output(self.root, validate=lambda path: True),
        ):
            with self.assertRaisesRegex(ValueError, "constante introuvable"):
                call()
            self.assertEqual(
                before,
                {p.name: p.read_bytes() for p in self.root.iterdir() if p.is_file()},
            )

    def test_record_output_needs_a_guard_that_can_validate(self):
        (self.root / "media").mkdir()
        (self.root / "media/film.mp4").write_bytes(b"film")
        with self.assertRaisesRegex(ValueError, "garde du film sans validate_output"):
            r.record_output(self.root)


class RealFilmsTests(unittest.TestCase):
    def test_both_films_are_consistent(self):
        for film in (
            "ff10-second-web-demo-transfer/form-pilot-kokoro",
            "ff04-room-booking-film",
        ):
            self.assertEqual(r.stale(D.parent / film), [], film)


class RealGuardTests(unittest.TestCase):
    """Sur une copie complète du film de réservation, avec son vrai garde."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        for name in (
            "film-chain",
            "ff10-hyperframes-guarded-integration",
            "ff04-room-booking-film",
        ):
            shutil.copytree(
                D.parent / name,
                root / name,
                ignore=shutil.ignore_patterns("__pycache__", ".ruff_cache", "*.webm"),
            )
        self.film = root / "ff04-room-booking-film"
        # La copie n'a pas été rendue ici : le reçu dit ce que le garde aurait écrit pour ce film.
        write_receipt(self.film, "media/room-booking.mp4", "input-pins.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_real_film_is_recorded_without_any_change(self):
        self.assertEqual(r.record_output(self.film), [])
        self.assertEqual(r.stale(self.film), [])

    def test_recording_the_film_also_records_the_inputs_it_came_from(self):
        r.record_output(self.film)
        fiche = json.loads((self.film / "provenance-manifest.json").read_text())
        pins = json.loads((self.film / "input-pins.json").read_text())
        self.assertEqual(fiche["film"]["inputs_sha256"], r.inputs_fingerprint(pins))

    def test_changed_input_makes_the_approval_stale_before_any_render(self):
        # Une entrée change puis les empreintes sont refigées, sans toucher à l'approbation.
        with (self.film / "transcript.txt").open("a") as handle:
            handle.write("Phrase ajoutée.\n")
        r.refresh(self.film)
        check = importlib.import_module("check_manifest")
        fiche = json.loads((self.film / "provenance-manifest.json").read_text())
        found = {
            x["check"]: (x["status"], x["detail"])
            for x in check.check_data(fiche, self.film)
            if x["check"] != "open_check"
        }
        self.assertEqual(found["approval"][0], "FAIL", found["approval"])
        self.assertIn("les entrées ont changé", found["approval"][1])

    def test_text_file_in_place_of_the_film_is_refused_and_nothing_is_written(self):
        fiche = (self.film / "provenance-manifest.json").read_bytes()
        (self.film / "media/room-booking.mp4").write_text("ceci n'est pas un film\n")
        with self.assertRaisesRegex(ValueError, "film refusé par le garde"):
            r.record_output(self.film)
        self.assertEqual(fiche, (self.film / "provenance-manifest.json").read_bytes())
        self.assertEqual(r.stale(self.film), [])


if __name__ == "__main__":
    unittest.main()
