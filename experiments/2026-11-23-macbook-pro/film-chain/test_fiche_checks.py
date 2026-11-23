"""Chaque motif de refus du contrôle de fiche, exercé sur les deux films.

Né de la contre-revue du 23 novembre 2026 (issue 15, constat 7). Un test qui vérifie seulement
qu'un contrôle est en échec ne voit pas la disparition d'un motif quand un autre motif du même
contrôle échoue aussi : chaque test vérifie donc le motif précis, par son texte.
"""

import copy
import importlib
import json
import sys
import unittest
from pathlib import Path

CHAIN = Path(__file__).resolve().parent
sys.path.insert(0, str(CHAIN))
m = importlib.import_module("check_manifest")
FILMS = {
    "formulaire": CHAIN.parent / "ff10-second-web-demo-transfer/form-pilot-kokoro",
    "reservation": CHAIN.parent / "ff04-room-booking-film",
}


def details(root, change=None, events=None):
    """Rend {contrôle: (statut, détail)} pour la fiche du film, éventuellement modifiée en mémoire."""
    data = json.loads((root / "provenance-manifest.json").read_text())
    if change:
        change(data)
    return {
        r["check"]: (r["status"], r["detail"])
        for r in m.check_data(data, root, events=events)
        if r["check"] != "open_check"
    }


class FicheCheckTests(unittest.TestCase):
    def expect(self, check, text, change=None, events_change=None):
        for name, root in FILMS.items():
            with self.subTest(film=name):
                events = None
                if events_change:
                    events = json.loads((root / "capture-events.json").read_text())
                    events_change(events)
                status, detail = details(root, change, events)[check]
                self.assertEqual(status, "FAIL", detail)
                self.assertIn(text, detail)

    def test_real_fiches_have_no_failure(self):
        for name, root in FILMS.items():
            with self.subTest(film=name):
                self.assertEqual(
                    [c for c, (s, _) in details(root).items() if s == "FAIL"], []
                )

    def test_empty_authorization(self):
        self.expect(
            "source",
            "autorisation non renseignée",
            lambda d: d["source"].update(authorization="  "),
        )

    def test_invalid_capture_date(self):
        self.expect(
            "source",
            "date de capture invalide",
            lambda d: d["source"].update(captured_on="hier"),
        )

    def test_changed_source(self):
        self.expect(
            "source",
            "source absente ou modifiée",
            lambda d: d["source"].update(sha256="0" * 64),
        )

    def test_unpinned_media(self):
        self.expect(
            "pinned_media",
            "n'est pas figé",
            lambda d: d["scenes"][0]["narration"].update(audio_ref="autre.wav"),
        )

    def test_narration_differs_from_transcript(self):
        self.expect(
            "texts",
            "la transcription diffère",
            lambda d: d["scenes"][0]["narration"].update(text="Autre phrase."),
        )

    def test_embedded_captions_differ_from_fiche(self):
        def change(d):
            d["scenes"][1]["caption"]["start_s"] -= 0.2

        self.expect("composition", "sous-titres incrustés différents", change)
        self.expect("captions", "repères différents", change)

    def test_narration_track_differs_from_composition(self):
        self.expect(
            "composition",
            "pistes de narration différentes",
            lambda d: d["scenes"][1]["narration"].update(duration_s=1.0),
        )

    def test_overlapping_narrations(self):
        def change(d):
            d["scenes"][1]["narration"]["start_s"] = (
                d["scenes"][0]["narration"]["start_s"] + 0.5
            )

        self.expect("timeline", "chevauche la précédente", change)

    def test_narration_beyond_end_of_film(self):
        self.expect(
            "timeline",
            "au-delà de la fin du film",
            lambda d: d["film"].update(duration_s=12),
        )

    def test_caption_not_framing_its_sentence(self):
        def change(d):
            d["scenes"][0]["caption"]["end_s"] = (
                d["scenes"][0]["narration"]["start_s"] + 1.0
            )

        self.expect("timeline", "n'encadre pas la phrase", change)

    def test_gesture_event_absent_from_capture(self):
        self.expect(
            "gestures",
            "événement absent de la capture",
            lambda d: d["scenes"][0]["gesture_events"].append("jamais_arrivé"),
        )

    def test_gestures_out_of_order(self):
        def swap(events):
            first, second = events["events"][1], events["events"][2]
            first["script_s"], second["script_s"] = (
                second["script_s"],
                first["script_s"],
            )

        self.expect("gestures", "gestes dans le désordre", events_change=swap)

    def test_result_outside_its_caption(self):
        def early(events):
            events["events"][-1]["script_s"] = 0.2
            events["events"][-2]["script_s"] = 0.1

        self.expect("gestures", "hors du sous-titre qui l'annonce", events_change=early)

    def test_observed_result_differs(self):
        self.expect(
            "results",
            "résultat observé différent",
            lambda d: d["scenes"][0]["result"].update(expected="autre chose"),
        )

    def test_unknown_approval_status(self):
        self.expect(
            "statuses",
            "statut d'approbation inconnu",
            lambda d: d["film"]["approval"].update(status="PEUT-ETRE"),
        )

    def test_unknown_scene_status(self):
        self.expect(
            "statuses",
            "statut ou type de plan inconnu",
            lambda d: d["scenes"][0].update(evidence_status="vu"),
        )

    def test_unobserved_scene_in_reviewed_film(self):
        self.expect(
            "statuses",
            "scène non observée",
            lambda d: d["scenes"][0].update(evidence_status="planned"),
        )

    def test_approval_document_does_not_name_the_film(self):
        self.expect(
            "approval",
            "ne nomme pas cette version",
            lambda d: d["film"].update(output_sha256="0" * 64),
        )

    def test_clip_duration_differs_from_its_slot(self):
        def change(d):
            d["scenes"][0]["narration"]["duration_s"] += 0.5

        self.expect("measured_audio", "durée réelle", change)

    def test_local_film_differs_from_fiche(self):
        self.expect(
            "output_film",
            "empreinte du film différente",
            lambda d: d["film"].update(output_sha256="1" * 64),
        )

    def test_observed_scene_whose_key_is_absent_from_the_journal(self):
        # Issue 15, constat 5 : « observé » sans observation ne peut pas répondre PASS.
        def change(d):
            d["scenes"][0]["result"]["observed_key"] = "cle_absente"
            d["scenes"][0]["result"]["expected"] = None

        self.expect("results", "clé observée absente du journal", change)

    def test_observed_scene_without_expected_value(self):
        self.expect("results", "résultat attendu non renseigné",
                    lambda d: d["scenes"][0]["result"].update(expected=None))

    def test_expected_value_is_compared_strictly(self):
        # True et 1 sont égaux en Python ; ce ne sont pas le même résultat observé.
        root = FILMS["reservation"]
        status, detail = details(root, lambda d: d["scenes"][1]["result"].update(expected=1))["results"]
        self.assertEqual(status, "FAIL", detail)
        self.assertIn("résultat observé différent", detail)

    def test_local_source_cannot_be_declared_without_fingerprint(self):
        self.expect("source", "source locale sans empreinte", lambda d: d["source"].update(sha256=None))

    def test_reviewed_film_without_journal_is_not_reported_as_passed(self):
        for name, root in FILMS.items():
            with self.subTest(film=name):
                found = details(root, lambda d: d["capture"].update(events_ref=None))
                self.assertEqual(found["statuses"][0], "UNVERIFIED", found["statuses"])
                self.assertIn("sans journal de capture lisible", found["statuses"][1])

    def test_inputs_changed_since_the_approved_render(self):
        # Constat de l'expérience de révision et reprise : une approbation périmée répondait PASS.
        self.expect("approval", "les entrées ont changé depuis le rendu du film approuvé",
                    lambda d: d["film"].update(inputs_sha256="0" * 64))

    def test_approved_film_without_inputs_fingerprint_is_not_reported_as_passed(self):
        for name, root in FILMS.items():
            with self.subTest(film=name):
                found = details(root, lambda d: d["film"].update(inputs_sha256=None))
                self.assertEqual(found["approval"][0], "UNVERIFIED", found["approval"])
                self.assertIn("entrées non figées", found["approval"][1])

    def test_draft_film_is_not_concerned(self):
        for name, root in FILMS.items():
            with self.subTest(film=name):
                def change(d):
                    d["film"].update(inputs_sha256=None, output_sha256=None)
                    d["film"]["approval"] = {"status": "DRAFT", "ref": None}

                self.assertEqual(details(root, change)["approval"][0], "PASS")

    def test_unknown_field(self):
        for name, root in FILMS.items():
            with self.subTest(film=name):
                data = copy.deepcopy(
                    json.loads((root / "provenance-manifest.json").read_text())
                )
                data["scenes"][0]["humeur"] = "calme"
                results = m.check_data(data, root)
                self.assertEqual(
                    [(r["check"], r["status"]) for r in results], [("schema", "FAIL")]
                )


if __name__ == "__main__":
    unittest.main()
