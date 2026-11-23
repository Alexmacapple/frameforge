"""Génère les fichiers texte du film depuis la fiche (provenance-manifest.json).

La fiche est la seule source : composition HyperFrames, sous-titres SRT et VTT, transcription.
L'habillage (cadre, couleurs, taille du texte) reste dans ce fichier. Il dépend de la version de la
fiche : la version 1 garde le bandeau d'origine, octet pour octet ; la version 2 ajoute un titre
d'ouverture, met les sous-titres en cartouche et agrandit la capture selon film.capture_zoom.
Sans option, les fichiers sont écrits. Avec --check, rien n'est écrit : code 1 si un fichier
présent diffère de ce que la fiche génère. Un chemin de fiche en argument vise un autre film.
"""

import html
import json
import sys
from pathlib import Path

HEAD = (
    '<!doctype html><html lang="fr"><head><meta charset="utf-8"><style>*{box-sizing:border-box}'
    "html,body{margin:0;width:1920px;height:1080px;overflow:hidden;background:#111;color:white;"
    "font-family:Arial,sans-serif}</style></head><body>\n"
)
CAPTION_STYLE = (
    "position:absolute;bottom:0;width:100%;background:#111;color:white;text-align:center;"
    "padding:20px;font-size:38px"
)
VIDEO_STYLE = "position:absolute;inset:0;width:100%;height:100%;object-fit:fill"
# Version 2. Le cartouche se pose sur le fond clair de la page filmée, d'où l'ombre portée.
HEAD_V2 = HEAD.replace("background:#111;color:white", "background:#f6f7fa;color:white")
CARTOUCHE_STYLE = (
    "position:absolute;left:50%;bottom:44px;transform:translateX(-50%);max-width:1680px;"
    "width:max-content;background:rgba(17,17,17,.9);color:#fff;text-align:center;"
    "padding:18px 36px;border-radius:14px;font-size:42px;line-height:1.3;"
    "box-shadow:0 10px 30px rgba(17,24,39,.22)"
)
TITLE_STYLE = CARTOUCHE_STYLE.replace(
    "font-size:42px", "font-size:46px;font-weight:700"
)
# Le titre s'affiche de TITLE_START à TITLE_END ; le premier sous-titre ne doit pas commencer avant.
TITLE_START, TITLE_END = 0.2, 1.4


def number(value):
    """Écrit 10 et non 10.0, 2.78 et non 2.7800000000000002."""
    return format(round(float(value), 3), "g")


def clock(seconds, separator):
    millis = round(float(seconds) * 1000)
    return f"{millis // 3600000:02d}:{millis // 60000 % 60:02d}:{millis // 1000 % 60:02d}{separator}{millis % 1000:03d}"


def video_style(zoom):
    """Capture agrandie depuis le haut, centrée en largeur : ce qui dépasse du cadre est rogné."""
    side = number((1 - zoom) * 50)
    size = number(zoom * 100)
    return f"position:absolute;left:{side}%;top:0;width:{size}%;height:{size}%;object-fit:fill"


def composition(fiche):
    v2 = fiche["manifest_version"] == 2
    caption_style = CARTOUCHE_STYLE if v2 else CAPTION_STYLE
    capture_style = video_style(fiche["film"]["capture_zoom"]) if v2 else VIDEO_STYLE
    duration = number(fiche["film"]["duration_s"])
    root_open = (
        f'<div id="root" data-composition-id="main" data-no-timeline data-start="0" data-duration="{duration}" '
        'data-width="1920" data-height="1080">'
    )
    video = (
        f'<video id="form-capture" class="clip" src="{fiche["capture"]["media_ref"]}" muted playsinline '
        f'data-start="0" data-duration="{duration}" data-track-index="0" style="{capture_style}"></video>'
    )
    lines = [root_open, video]
    if v2:
        lines.append(
            f'<div id="title" class="clip" data-start="{number(TITLE_START)}" '
            f'data-duration="{number(TITLE_END - TITLE_START)}" data-track-index="7" '
            f'style="{TITLE_STYLE}">{html.escape(fiche["film"]["title"], quote=False)}</div>'
        )
    for i, scene in enumerate(fiche["scenes"], 1):
        voice, caption = scene["narration"], scene["caption"]
        lines.append(
            f'<audio id="voice{i}" src="{voice["audio_ref"]}" data-start="{number(voice["start_s"])}" '
            f'data-duration="{number(voice["duration_s"])}" data-track-index="{i}"></audio>'
        )
        lines.append(
            f'<div id="caption{i}" class="clip" data-start="{number(caption["start_s"])}" '
            f'data-duration="{number(caption["end_s"] - caption["start_s"])}" data-track-index="6" '
            f'style="{caption_style}">{html.escape(voice["text"], quote=False)}</div>'
        )
    return (HEAD_V2 if v2 else HEAD) + "\n".join(lines) + "\n</div></body></html>\n"


def subtitles(fiche, separator, numbered):
    blocks = []
    for i, scene in enumerate(fiche["scenes"], 1):
        cue = f"{clock(scene['caption']['start_s'], separator)} --> {clock(scene['caption']['end_s'], separator)}"
        blocks.append(
            (f"{i}\n" if numbered else "") + f"{cue}\n{scene['narration']['text']}\n"
        )
    return "\n".join(blocks)


def render(fiche):
    """Contenu de chaque fichier, par nom, tel que la fiche le détermine."""
    film = fiche["film"]
    files = {
        film["composition_ref"]: composition(fiche),
        # Le titre est un texte affiché que la voix ne dit pas : il ouvre la transcription.
        film["transcript_ref"]: (film["title"] + "\n" if "title" in film else "")
        + "".join(s["narration"]["text"] + "\n" for s in fiche["scenes"]),
    }
    for ref in film["caption_refs"]:
        if ref.endswith(".srt"):
            files[ref] = subtitles(fiche, ",", numbered=True)
        elif ref.endswith(".vtt"):
            files[ref] = "WEBVTT\n\n" + subtitles(fiche, ".", numbered=False)
        else:
            raise ValueError("format de sous-titres non pris en charge : " + ref)
    return files


def stale_files(fiche, root):
    """Fichiers absents ou différents de ce que la fiche génère."""
    root = Path(root)
    return sorted(
        name
        for name, text in render(fiche).items()
        if not (root / name).is_file() or (root / name).read_bytes() != text.encode()
    )


def main():
    # Sans chemin, la fiche du dossier courant ; avec un chemin, celle du film visé.
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = (
        Path(paths[0]).resolve() if paths else Path.cwd() / "provenance-manifest.json"
    )
    fiche, root = json.loads(path.read_text()), path.parent
    stale = stale_files(fiche, root)
    if "--check" in sys.argv[1:]:
        print(json.dumps({"status": "FAIL" if stale else "PASS", "stale": stale}))
        return 1 if stale else 0
    for name in stale:
        (root / name).write_text(render(fiche)[name])
    print(json.dumps({"status": "PASS", "written": stale}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
