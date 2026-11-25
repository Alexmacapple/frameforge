"""Écrit ou recale la fiche du film des fenêtres modales.

Sans option : fiche DRAFT avec les phrases, repères provisoires (avant synthèse).
--timeline : relit narration-synthesis.json et pose les repères depuis les durées mesurées.
"""

import hashlib
import json
import sys
from pathlib import Path

FILM = (
    Path(sys.argv[1])
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--")
    else Path(__file__).resolve().parent
)
GAP = 1.2  # silence entre deux phrases, le temps de voir le résultat
FIRST = 1.8  # après le titre (0,2 à 1,4 s)
TAIL = 2.5  # dernière image tenue après la dernière phrase

SCENES = [
    (
        "fautive-ouverture",
        ["bad_open_clicked", "bad_dialog_visible"],
        "bad_dialog_visible",
        "bad_focus_after_open",
        "open-bad",
        "Version fautive. On clique sur Supprimer mon compte. La fenêtre s'ouvre, mais le focus reste derrière, sur le bouton de la page.",
    ),
    (
        "fautive-tab",
        ["bad_tab_pressed", "bad_focus_left"],
        "bad_focus_left",
        "bad_focus_after_tab",
        "help-link",
        "On appuie sur Tab. Le focus part sur le lien Consulter l'aide, derrière la fenêtre. On ne sait plus où l'on est.",
    ),
    (
        "fautive-echap",
        ["bad_escape_pressed", "bad_still_open", "bad_cancel_clicked"],
        "bad_still_open",
        "bad_open_after_escape",
        True,
        "On appuie sur Échap. Rien ne se passe, la fenêtre reste ouverte. On la ferme à la souris, avec Annuler.",
    ),
    (
        "corrigee-ouverture",
        ["good_open_clicked", "good_focus_inside"],
        "good_focus_inside",
        "good_focus_after_open",
        "good-cancel",
        "Version corrigée. On clique de nouveau sur Supprimer mon compte. Le focus entre dans la fenêtre, sur Annuler, l'action la moins risquée.",
    ),
    (
        "corrigee-tab",
        ["good_tab1_pressed", "good_tab2_pressed", "good_focus_wrapped"],
        "good_focus_wrapped",
        "good_focus_after_two_tabs",
        "good-cancel",
        "Deux appuis sur Tab. Le focus passe sur Supprimer, puis revient sur Annuler. Il reste dans la fenêtre.",
    ),
    (
        "corrigee-echap",
        ["good_escape_pressed", "good_focus_restored"],
        "good_focus_restored",
        "good_focus_after_escape",
        "open-good",
        "On appuie sur Échap. La fenêtre se ferme, et le focus revient sur le bouton qui l'avait ouverte.",
    ),
    (
        "reprise-parcours",
        ["resume_tab_pressed", "resume_focus_next"],
        "resume_focus_next",
        "focus_after_resume",
        "next-step",
        "Un dernier appui sur Tab mène à l'étape suivante. Le parcours reprend là où il s'était arrêté.",
    ),
]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build(durations):
    t, scenes = FIRST, []
    for i, (sid, gestures, event, key, expected, text) in enumerate(SCENES):
        d = durations[i]
        scenes.append(
            {
                "scene_id": sid,
                "shot_type": "continuous_action",
                "gesture_events": gestures,
                "result": {"event": event, "observed_key": key, "expected": expected},
                "narration": {
                    "text": text,
                    "audio_ref": f"voice{i + 1}.wav",
                    "start_s": round(t, 3),
                    "duration_s": d,
                },
                "caption": {"start_s": round(t, 3), "end_s": round(t + d + 0.3, 3)},
                "evidence_status": "observed",
            }
        )
        t += d + GAP
    duration = round(t - GAP + TAIL)
    return {
        "manifest_version": 2,
        "pins_ref": "input-pins.json",
        "film": {
            "id": "fenetres-modales",
            "duration_s": duration,
            "composition_ref": "index.html",
            "transcript_ref": "transcript.txt",
            "caption_refs": ["captions.srt", "captions.vtt"],
            "output_ref": "media/fenetres-modales.mp4",
            "output_sha256": None,
            "inputs_sha256": None,
            "approval": {"status": "DRAFT", "ref": None},
            "open_checks": [
                "Visionnage humain du film",
                "Compréhension du film sans l'image (ticket 35)",
                "Conformité de la voix au texte de narration (ticket 36)",
                "Prononciation de Tab et Échap par la voix de synthèse",
                "Aucun lecteur d'écran testé : le film montre le focus clavier, pas une restitution vocale",
            ],
            "title": "Fenêtres modales : le focus au clavier",
            "capture_zoom": 1,
        },
        "source": {
            "ref": "modales.html",
            "sha256": sha(FILM / "modales.html"),
            "authorization": "Fixture locale du dépôt, écrite pour ce film, données fictives, aucun compte ni session réels.",
            "captured_on": "2026-11-25",
        },
        "capture": {"media_ref": "capture.mp4", "events_ref": "capture-events.json"},
        "scenes": scenes,
    }


# Une fiche qui porte déjà l'empreinte d'un film rendu ne se réécrit pas : l'empreinte serait perdue.
current = FILM / "provenance-manifest.json"
if current.is_file() and json.loads(current.read_text())["film"].get("output_sha256"):
    sys.exit("fiche d'un film déjà rendu : rien n'est réécrit")
if "--timeline" in sys.argv:
    synth = json.loads((FILM / "narration-synthesis.json").read_text())
    durations = [c["duration_s"] for c in synth["clips"]]
else:
    durations = [5.0] * len(SCENES)
(FILM / "provenance-manifest.json").write_text(
    json.dumps(build(durations), indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {"duration_s": build(durations)["film"]["duration_s"], "durations": durations}
    )
)
