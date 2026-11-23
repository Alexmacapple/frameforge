"""Contrôle de la fiche de film (manifeste de provenance, FF-04).

La fiche relie chaque scène à son geste, son résultat observé, sa phrase et ses repères.
Elle n'est pas une preuve : ce contrôle la confronte aux fichiers qu'elle cite.
Chaque champ accepté est lu par au moins un contrôle ; tout autre champ est refusé.
Code de sortie : 0 tout passe, 1 au moins un FAIL, 2 aucun FAIL mais des UNVERIFIED.

PDG-LARGE-FILE-JUSTIFICATION: une seule responsabilité, confronter une fiche aux fichiers qu'elle
cite. Les treize contrôles partagent les mêmes données lues une fois ; les séparer en modules
ajouterait des interfaces sans consommateur. La longueur vient surtout du formatage automatique.
"""

import hashlib
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

SHOT_TYPES = {"fixed", "continuous_action", "title_card", "honest_cut", "result"}
EVIDENCE = {"observed", "reasoned", "planned", "unverified", "failed"}
APPROVAL = {"DRAFT", "REVIEWED", "APPROVED_FOR_RELEASE", "REVOKED"}
FIELDS = {
    "root": {"manifest_version", "pins_ref", "film", "source", "capture", "scenes"},
    "film": {
        "id",
        "duration_s",
        "composition_ref",
        "transcript_ref",
        "caption_refs",
        "output_ref",
        "output_sha256",
        "approval",
        "open_checks",
    },
    "approval": {"status", "ref"},
    "source": {"ref", "sha256", "authorization", "captured_on"},
    "capture": {"media_ref", "events_ref"},
    "scene": {
        "scene_id",
        "shot_type",
        "gesture_events",
        "result",
        "narration",
        "caption",
        "evidence_status",
    },
    "result": {"event", "observed_key", "expected"},
    "narration": {"text", "audio_ref", "start_s", "duration_s"},
    "caption": {"start_s", "end_s"},
}
CUE = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+) --> (\d+):(\d+):(\d+)[,.](\d+)\n(.+)")
AUDIO = re.compile(
    r'<audio[^>]*src="([^"]+)"[^>]*data-start="([\d.]+)"[^>]*data-duration="([\d.]+)"'
)
CAPTION = re.compile(
    r'<div id="caption\d+"[^>]*data-start="([\d.]+)"[^>]*data-duration="([\d.]+)"[^>]*>([^<]*)<'
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def cues(text):
    out = []
    for g in CUE.findall(text):
        h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, g[:8])
        out.append(
            (
                h1 * 3600 + m1 * 60 + s1 + ms1 / 1000,
                h2 * 3600 + m2 * 60 + s2 + ms2 / 1000,
                g[8].strip(),
            )
        )
    return out


def near(a, b, tolerance=0.0011):
    return abs(float(a) - float(b)) <= tolerance


def schema_problems(data):
    problems = []

    def same(obj, kind, where):
        if not isinstance(obj, dict) or set(obj) != FIELDS[kind]:
            extra = (
                sorted(set(obj) ^ FIELDS[kind])
                if isinstance(obj, dict)
                else ["objet attendu"]
            )
            problems.append(f"{where} : champs inattendus ou manquants {extra}")
            return False
        return True

    if same(data, "root", "fiche"):
        if same(data["film"], "film", "film"):
            same(data["film"]["approval"], "approval", "film.approval")
        same(data["source"], "source", "source")
        same(data["capture"], "capture", "capture")
        for i, scene in enumerate(data["scenes"]):
            if same(scene, "scene", f"scène {i + 1}"):
                for part in ("result", "narration", "caption"):
                    same(scene[part], part, f"scène {i + 1}.{part}")
    return problems


def check_data(data, root, events=None):
    root = Path(root)
    results = []

    def add(check, status, detail=""):
        results.append({"check": check, "status": status, "detail": detail})

    def verdict(check, problems):
        add(check, "FAIL" if problems else "PASS", " ; ".join(problems))

    def verdict_or_unverified(check, problems, gap):
        # Un manque déclaré dans la fiche n'est ni un succès ni une incohérence.
        if gap and not problems:
            add(check, "UNVERIFIED", gap)
        else:
            verdict(check, problems)

    problems = schema_problems(data)
    verdict("schema", problems)
    if problems:
        return results
    film, scenes = data["film"], data["scenes"]
    narrations = [s["narration"] for s in scenes]

    src = data["source"]
    problems = []
    # Une source externe (site public) n'a pas d'empreinte : son état filmé n'est pas vérifiable.
    external = src["sha256"] is None
    if not external and (
        not (root / src["ref"]).is_file() or sha(root / src["ref"]) != src["sha256"]
    ):
        problems.append("source absente ou modifiée")
    if not src["authorization"].strip():
        problems.append("autorisation non renseignée")
    try:
        date.fromisoformat(src["captured_on"])
    except ValueError:
        problems.append("date de capture invalide")
    verdict_or_unverified(
        "source", problems, "source externe non figée par empreinte" if external else ""
    )

    # La composition n'est pas exigée ici : son contenu est confronté à la fiche plus bas.
    pins = json.loads((root / data["pins_ref"]).read_text())
    refs = [
        data["capture"]["media_ref"],
        film["transcript_ref"],
        *film["caption_refs"],
        *[n["audio_ref"] for n in narrations],
    ]
    problems = [
        f"{ref} n'est pas figé par {data['pins_ref']}"
        for ref in refs
        if ref not in pins
    ]
    verdict("pinned_media", problems)

    texts = [n["text"] for n in narrations]
    transcript = [
        line.strip()
        for line in (root / film["transcript_ref"]).read_text().splitlines()
        if line.strip()
    ]
    caption_files = {
        ref: cues((root / ref).read_text()) for ref in film["caption_refs"]
    }
    problems = (
        [] if transcript == texts else ["la transcription diffère de la narration"]
    )
    problems += [
        f"{ref} : texte différent"
        for ref, c in caption_files.items()
        if [x[2] for x in c] != texts
    ]
    verdict("texts", problems)

    problems = []
    for ref, file_cues in caption_files.items():
        if len(file_cues) != len(scenes) or any(
            not near(c[0], s["caption"]["start_s"])
            or not near(c[1], s["caption"]["end_s"])
            for c, s in zip(file_cues, scenes)
        ):
            problems.append(f"{ref} : repères différents de la fiche")
    verdict("captions", problems)

    html = (root / film["composition_ref"]).read_text()
    audio, divs = AUDIO.findall(html), CAPTION.findall(html)
    problems = []
    if len(audio) != len(scenes) or any(
        a[0] != n["audio_ref"]
        or not near(a[1], n["start_s"])
        or not near(a[2], n["duration_s"])
        for a, n in zip(audio, narrations)
    ):
        problems.append("pistes de narration différentes de la composition")
    if len(divs) != len(scenes) or any(
        not near(d[0], s["caption"]["start_s"]) or d[2] != s["narration"]["text"]
        for d, s in zip(divs, scenes)
    ):
        problems.append("sous-titres incrustés différents de la fiche")
    verdict("composition", problems)

    problems, previous_end = [], 0.0
    for s in scenes:
        start, end = (
            s["narration"]["start_s"],
            s["narration"]["start_s"] + s["narration"]["duration_s"],
        )
        if start < previous_end:
            problems.append(f"{s['scene_id']} : narration qui chevauche la précédente")
        if end > film["duration_s"]:
            problems.append(f"{s['scene_id']} : narration au-delà de la fin du film")
        if s["caption"]["start_s"] > start or s["caption"]["end_s"] < end:
            problems.append(f"{s['scene_id']} : le sous-titre n'encadre pas la phrase")
        previous_end = end
    verdict("timeline", problems)

    if events is None and data["capture"]["events_ref"] is not None:
        events = json.loads((root / data["capture"]["events_ref"]).read_text())
    times = {e["name"]: e["script_s"] for e in events["events"]} if events else {}
    problems, untimed = [], []
    for s in scenes:
        names = s["gesture_events"]
        if events is None or not names or s["result"]["event"] is None:
            untimed.append(s["scene_id"])
            continue
        if any(n not in times for n in names) or s["result"]["event"] not in names:
            problems.append(f"{s['scene_id']} : événement absent de la capture")
            continue
        if [times[n] for n in names] != sorted(times[n] for n in names):
            problems.append(f"{s['scene_id']} : gestes dans le désordre")
        shown = times[s["result"]["event"]]
        if not s["caption"]["start_s"] <= shown <= s["caption"]["end_s"]:
            problems.append(
                f"{s['scene_id']} : résultat à {shown} s, hors du sous-titre qui l'annonce"
            )
    verdict_or_unverified(
        "gestures",
        problems,
        "repère du résultat non mesuré : " + ", ".join(untimed) if untimed else "",
    )

    problems = [
        f"{s['scene_id']} : résultat observé différent de l'attendu"
        for s in scenes
        if events is not None
        and s["evidence_status"] == "observed"
        and events["observed"].get(s["result"]["observed_key"])
        != s["result"]["expected"]
    ]
    verdict_or_unverified(
        "results",
        problems,
        ""
        if events is not None
        else "aucun journal de capture lisible par ce contrôle",
    )

    status = film["approval"]["status"]
    problems = [
        f"{s['scene_id']} : statut ou type de plan inconnu"
        for s in scenes
        if s["evidence_status"] not in EVIDENCE or s["shot_type"] not in SHOT_TYPES
    ]
    if status not in APPROVAL:
        problems.append("statut d'approbation inconnu")
    if status in ("REVIEWED", "APPROVED_FOR_RELEASE"):
        problems += [
            f"{s['scene_id']} : scène non observée dans un film {status}"
            for s in scenes
            if s["evidence_status"] != "observed"
        ]
    verdict("statuses", problems)

    approval = root / film["approval"]["ref"]
    problems = []
    if status != "DRAFT":
        text = approval.read_text() if approval.is_file() else ""
        # L'empreinte suffit pour une approbation éditoriale ; une autorisation de diffusion
        # doit en plus être écrite en toutes lettres dans le document.
        needs_wording = status == "APPROVED_FOR_RELEASE"
        if film["output_sha256"] not in text or (needs_wording and status not in text):
            problems.append(
                "le document d'approbation ne nomme pas cette version et ce statut"
            )
    verdict("approval", problems)

    problems, missing = [], []
    for n in narrations:
        clip = root / n["audio_ref"]
        if not clip.is_file():
            missing.append(n["audio_ref"])
            continue
        real = float(
            subprocess.check_output(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "csv=p=0",
                    str(clip),
                ]
            )
        )
        if abs(real - n["duration_s"]) > 0.02:
            problems.append(
                f"{n['audio_ref']} : durée réelle {real:.3f} s, créneau {n['duration_s']} s"
            )
    if missing and not problems:
        add(
            "measured_audio",
            "UNVERIFIED",
            "clips absents en local : " + ", ".join(missing),
        )
    else:
        verdict("measured_audio", problems)

    output = root / film["output_ref"]
    if not output.is_file():
        add("output_film", "UNVERIFIED", "film absent en local")
    else:
        verdict(
            "output_film",
            []
            if sha(output) == film["output_sha256"]
            else ["empreinte du film différente"],
        )

    for item in film["open_checks"]:
        add("open_check", "UNVERIFIED", item)
    return results


def exit_code(results):
    states = {r["status"] for r in results}
    return 1 if "FAIL" in states else 2 if "UNVERIFIED" in states else 0


def main():
    path = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path(__file__).resolve().parent / "provenance-manifest.json"
    )
    results = check_data(json.loads(path.read_text()), path.resolve().parent)
    for r in results:
        print(
            f"{r['status']:10s} {r['check']}"
            + (f" — {r['detail']}" if r["detail"] else "")
        )
    return exit_code(results)


if __name__ == "__main__":
    sys.exit(main())
