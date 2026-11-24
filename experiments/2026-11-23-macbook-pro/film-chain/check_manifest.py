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
from html import unescape
from pathlib import Path, PurePosixPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_from_fiche import TITLE_END, TITLE_START

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
        "inputs_sha256",
        "approval",
        "open_checks",
    },
    # Version 2 de la fiche : titre d'ouverture et agrandissement de la capture, en plus.
    "film_v2": {"title", "capture_zoom"},
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
CUE_TIME = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+) --> (\d+):(\d+):(\d+)[,.](\d+)")
AUDIO = re.compile(
    r'<audio[^>]*src="([^"]+)"[^>]*data-start="([\d.]+)"[^>]*data-duration="([\d.]+)"'
)
TITLE = re.compile(
    r'<div id="title"[^>]*data-start="([\d.]+)"[^>]*data-duration="([\d.]+)"[^>]*>([^<]*)<'
)
VIDEO = re.compile(r'<video[^>]*src="([^"]+)"')
CAPTION = re.compile(
    r'<div id="caption\d+"[^>]*data-start="([\d.]+)"[^>]*data-duration="([\d.]+)"[^>]*>([^<]*)<'
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def cues(text):
    """Repères d'un fichier SRT ou VTT : (début, fin, texte entier du repère).

    Le texte reprend toutes les lignes du repère : une ligne ajoutée sous la phrase se voit.
    Une ligne de minutage illisible donne un repère sans temps, qui ne peut égaler aucune scène.
    """
    out = []
    for block in re.split(r"\n[ \t]*\n", text.strip()):
        lines = [line.strip() for line in block.splitlines()]
        at = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if at is None:
            continue
        timing = CUE_TIME.fullmatch(lines[at])
        said = "\n".join(lines[at + 1 :]).strip()
        if timing is None:
            out.append((-1.0, -1.0, said))
            continue
        h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, timing.groups())
        out.append(
            (
                h1 * 3600 + m1 * 60 + s1 + ms1 / 1000,
                h2 * 3600 + m2 * 60 + s2 + ms2 / 1000,
                said,
            )
        )
    return out


def near(a, b, tolerance=0.0011):
    return abs(float(a) - float(b)) <= tolerance


def inputs_fingerprint(pins, fiche_name="provenance-manifest.json"):
    """Empreinte de l'ensemble des entrées figées d'un film, fiche exclue.

    Inscrite dans la fiche quand l'empreinte du film rendu y est reportée : elle dit de quelles
    entrées ce film est sorti. La fiche est exclue, puisqu'elle porte elle-même cette valeur.
    """
    entries = {name: value for name, value in pins.items() if name != fiche_name}
    return hashlib.sha256(json.dumps(entries, sort_keys=True).encode()).hexdigest()


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_time(value):
    return is_number(value) and value >= 0


def is_text(value):
    """Une ligne de texte, sans espace en bord : ce qui est comparé est ce qui est écrit."""
    return (
        isinstance(value, str)
        and value != ""
        and value == value.strip()
        and "\n" not in value
    )


def is_ref(value):
    """Chemin relatif qui reste dans le dossier du film."""
    if not isinstance(value, str) or not value or value != value.strip():
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def is_sha(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def is_string(value):
    return isinstance(value, str)


def optional(check):
    return lambda value: value is None or check(value)


def list_of(check, at_least=0):
    return lambda value: (
        isinstance(value, list)
        and len(value) >= at_least
        and all(check(v) for v in value)
    )


# Forme attendue de chaque valeur. Un champ absent d'ici n'est contraint que par sa présence.
SHAPES = {
    "root": {"pins_ref": is_ref, "scenes": list_of(lambda v: True, at_least=1)},
    "film": {
        "id": is_text,
        "duration_s": lambda v: is_number(v) and v > 0,
        "composition_ref": is_ref,
        "transcript_ref": is_ref,
        "caption_refs": list_of(is_ref),
        "output_ref": is_ref,
        "output_sha256": optional(is_sha),
        "inputs_sha256": optional(is_sha),
        "open_checks": list_of(is_string),
    },
    "approval": {"status": is_string, "ref": optional(is_string)},
    "source": {
        "ref": is_text,
        "sha256": optional(is_sha),
        "authorization": is_string,
        "captured_on": is_string,
    },
    "capture": {"media_ref": is_ref, "events_ref": optional(is_ref)},
    "scene": {
        "scene_id": is_text,
        "shot_type": is_string,
        "gesture_events": list_of(is_string),
        "evidence_status": is_string,
    },
    "result": {"event": optional(is_string), "observed_key": optional(is_string)},
    "narration": {
        "text": is_text,
        "audio_ref": is_ref,
        "start_s": is_time,
        "duration_s": is_time,
    },
    "caption": {"start_s": is_time, "end_s": is_time},
}


def journal_is_readable(events):
    """Forme du journal de capture que les contrôles lisent : événements datés, observations."""
    return (
        isinstance(events, dict)
        and isinstance(events.get("observed"), dict)
        and isinstance(events.get("events"), list)
        and all(
            isinstance(e, dict)
            and is_string(e.get("name"))
            and is_number(e.get("script_s"))
            for e in events["events"]
        )
    )


def schema_problems(data):
    problems = []

    def same(obj, kind, where, more=frozenset()):
        if not isinstance(obj, dict) or set(obj) != FIELDS[kind] | more:
            extra = (
                sorted(set(obj) ^ (FIELDS[kind] | more))
                if isinstance(obj, dict)
                else ["objet attendu"]
            )
            problems.append(f"{where} : champs inattendus ou manquants {extra}")
            return False
        odd = sorted(
            f for f, check in SHAPES.get(kind, {}).items() if not check(obj[f])
        )
        if odd:
            problems.append(f"{where} : valeur de forme inattendue pour {odd}")
            return False
        return True

    if same(data, "root", "fiche"):
        version = data["manifest_version"]
        if type(version) is not int or version not in (1, 2):
            problems.append(f"version de fiche inconnue : {version!r}")
        v2 = FIELDS["film_v2"] if version == 2 else frozenset()
        if same(data["film"], "film", "film", v2):
            same(data["film"]["approval"], "approval", "film.approval")
            if v2:
                title, zoom = data["film"]["title"], data["film"]["capture_zoom"]
                if not isinstance(title, str) or not title.strip():
                    problems.append("film : titre vide")
                if (
                    isinstance(zoom, bool)
                    or not isinstance(zoom, (int, float))
                    or not 1 <= zoom <= 1.5
                ):
                    problems.append(
                        "film : agrandissement de la capture hors de 1 à 1,5"
                    )
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
    # Seule une adresse en ligne peut se passer d'empreinte : un fichier local se hache.
    if external and not src["ref"].startswith(("http://", "https://")):
        problems.append("source locale sans empreinte")
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
    # Figé ne suffit pas : l'empreinte inscrite doit être celle du fichier présent.
    absent = sorted(name for name in pins if not (root / name).is_file())
    problems += [
        f"{name} : empreinte figée différente du fichier"
        for name in sorted(pins)
        if name not in absent and sha(root / name) != pins[name]
    ]
    verdict_or_unverified(
        "pinned_media",
        problems,
        "fichiers figés absents en local : " + ", ".join(absent) if absent else "",
    )

    texts = [n["text"] for n in narrations]
    transcript = [
        line.strip()
        for line in (root / film["transcript_ref"]).read_text().splitlines()
        if line.strip()
    ]
    caption_files = {
        ref: cues((root / ref).read_text()) for ref in film["caption_refs"]
    }
    # En version 2, le titre affiché ouvre la transcription ; les sous-titres ne le portent pas.
    spoken_and_shown = ([film["title"]] if "title" in film else []) + texts
    problems = (
        []
        if transcript == spoken_and_shown
        else ["la transcription diffère de la narration"]
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

    page = (root / film["composition_ref"]).read_text()
    # Une adresse est écrite échappée dans la page (« & » devient « &amp; ») : elle se compare
    # une fois rendue lisible, comme le texte des sous-titres.
    audio = [(unescape(a[0]), *a[1:]) for a in AUDIO.findall(page)]
    divs = CAPTION.findall(page)
    problems = []
    # Une piste que le motif ne reconnaît pas (attributs dans un autre ordre) reste une piste.
    if page.count("<audio") != len(audio):
        problems.append("piste audio non reconnue dans la composition")
    if [unescape(v) for v in VIDEO.findall(page)] != [
        data["capture"]["media_ref"]
    ] or page.count("<video") != 1:
        problems.append("la composition ne montre pas la seule capture de la fiche")
    if len(audio) != len(scenes) or any(
        a[0] != n["audio_ref"]
        or not near(a[1], n["start_s"])
        or not near(a[2], n["duration_s"])
        for a, n in zip(audio, narrations)
    ):
        problems.append("pistes de narration différentes de la composition")
    if len(divs) != len(scenes) or any(
        not near(d[0], s["caption"]["start_s"])
        or not near(d[1], s["caption"]["end_s"] - s["caption"]["start_s"])
        # Le texte est écrit échappé dans la page : il se compare une fois rendu lisible.
        or unescape(d[2]) != s["narration"]["text"]
        for d, s in zip(divs, scenes)
    ):
        problems.append("sous-titres incrustés différents de la fiche")
    titles = [(float(t[0]), float(t[1]), unescape(t[2])) for t in TITLE.findall(page)]
    wanted = (
        [(TITLE_START, TITLE_END - TITLE_START, film["title"])]
        if "title" in film
        else []
    )
    if (
        page.count('id="title"') != len(titles)
        or len(titles) != len(wanted)
        or any(
            not near(t[0], w[0]) or not near(t[1], w[1]) or t[2] != w[2]
            for t, w in zip(titles, wanted)
        )
    ):
        problems.append("titre incrusté différent de la fiche")
    verdict("composition", problems)

    problems, previous_end = [], 0.0
    if "title" in film and scenes[0]["caption"]["start_s"] < TITLE_END:
        problems.append("pas de place pour le titre avant le premier sous-titre")
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
    # Un journal de forme inattendue n'est pas lu : il est signalé, et rien n'est tenu pour observé.
    journal = []
    if events is not None and not journal_is_readable(events):
        journal, events = ["journal de capture de forme inattendue"], None
    times = {e["name"]: e["script_s"] for e in events["events"]} if events else {}
    problems, untimed = list(journal), []
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

    # Une scène « observée » doit avoir une observation lisible : clé présente dans le journal,
    # valeur attendue renseignée, et égalité stricte (True n'est pas 1).
    problems, compared = list(journal), 0
    for s in scenes:
        if events is None or s["evidence_status"] != "observed":
            continue
        compared += 1
        key, wanted = s["result"]["observed_key"], s["result"]["expected"]
        if key not in events["observed"]:
            problems.append(f"{s['scene_id']} : clé observée absente du journal")
        elif wanted is None:
            problems.append(f"{s['scene_id']} : résultat attendu non renseigné")
        elif (
            type(events["observed"][key]) is not type(wanted)
            or events["observed"][key] != wanted
        ):
            problems.append(
                f"{s['scene_id']} : résultat observé différent de l'attendu"
            )
    verdict_or_unverified(
        "results",
        problems,
        "aucun journal de capture lisible par ce contrôle"
        if events is None
        # Rien à comparer n'est pas « tout est conforme ».
        else ""
        if compared
        else "aucune scène déclarée observée : aucun résultat comparé",
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
    # Sans journal lisible, des scènes qui se disent observées ne sont pas vérifiées. Pour un
    # brouillon c'est un manque ; pour un film approuvé c'est un échec (décision du 24 novembre
    # 2026, issue 15) : l'approbation s'appuie sur ce que le film dit avoir observé.
    claimed = [s["scene_id"] for s in scenes if s["evidence_status"] == "observed"]
    unproven = (
        "scènes déclarées observées sans journal de capture lisible : "
        + ", ".join(claimed)
        if events is None and claimed
        else ""
    )
    if unproven and status in ("REVIEWED", "APPROVED_FOR_RELEASE"):
        problems.append(
            f"film {status} sans journal de capture lisible : " + ", ".join(claimed)
        )
    verdict_or_unverified("statuses", problems, unproven)

    # Un brouillon n'a ni document d'approbation ni, avant son premier rendu, d'empreinte de film.
    fingerprint, approval_ref = film["output_sha256"], film["approval"]["ref"]
    problems = []
    stale_gap = ""
    if status != "DRAFT":
        approval = root / approval_ref if approval_ref else None
        text = approval.read_text() if approval and approval.is_file() else ""
        if not fingerprint or fingerprint not in text:
            problems.append("le document d'approbation ne nomme pas cette version")
        # Le document d'approbation est une trace humaine distincte : ni la fiche, ni une copie
        # de la fiche, ni un fichier que la fiche cite ou que le garde fige.
        own = {
            "provenance-manifest.json",
            data["pins_ref"],
            film["composition_ref"],
            *([data["capture"]["events_ref"]] if data["capture"]["events_ref"] else []),
            *refs,
            *pins,
        }
        if approval and approval.resolve() in {(root / name).resolve() for name in own}:
            problems.append(
                "le document d'approbation est un fichier cité ou figé par la fiche"
            )
        try:
            json.loads(text)
            problems.append(
                "le document d'approbation est un fichier de données, pas une trace humaine"
            )
        except ValueError:
            pass
        # Aucune preuve d'autorisation de diffusion n'est définie par le projet : un mot dans un
        # fichier n'en est pas une. Ce statut est refusé tant que cette preuve n'existe pas.
        if status == "APPROVED_FOR_RELEASE":
            problems.append(
                "autorisation de diffusion : aucune preuve vérifiable n'est définie, statut refusé"
            )
        # L'approbation porte sur un film ; ce film est sorti de certaines entrées. Si elles ont
        # changé depuis, l'approbation ne couvre plus ce que la fiche décrit aujourd'hui.
        if film["inputs_sha256"] is None:
            stale_gap = "entrées non figées au moment du rendu approuvé : approbation non rattachée aux entrées"
        elif film["inputs_sha256"] != inputs_fingerprint(pins):
            problems.append("les entrées ont changé depuis le rendu du film approuvé")
    verdict_or_unverified("approval", problems, stale_gap)

    problems, missing = [], []
    for n in narrations:
        clip = root / n["audio_ref"]
        if not clip.is_file():
            missing.append(n["audio_ref"])
            continue
        try:
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
                    ],
                    timeout=30,
                )
            )
        except (subprocess.SubprocessError, ValueError):
            problems.append(f"{n['audio_ref']} : durée illisible par ffprobe")
            continue
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
    if not fingerprint:
        add(
            "output_film",
            "UNVERIFIED",
            "film pas encore rendu : aucune empreinte dans la fiche",
        )
    elif not output.is_file():
        add("output_film", "UNVERIFIED", "film absent en local")
    else:
        verdict(
            "output_film",
            [] if sha(output) == fingerprint else ["empreinte du film différente"],
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
        else Path.cwd() / "provenance-manifest.json"
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
