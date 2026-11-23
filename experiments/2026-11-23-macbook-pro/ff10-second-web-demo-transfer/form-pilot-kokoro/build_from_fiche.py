"""Génère les fichiers texte du film depuis la fiche (provenance-manifest.json).

La fiche est la seule source : composition HyperFrames, sous-titres SRT et VTT, transcription.
L'habillage (cadre, couleurs, taille du texte) est propre à ce film et reste dans ce fichier.
Sans option, les fichiers sont écrits. Avec --check, rien n'est écrit : code 1 si un fichier
présent diffère de ce que la fiche génère. Un chemin de fiche en argument vise un autre film.
"""

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
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


def number(value):
    """Écrit 10 et non 10.0, 2.78 et non 2.7800000000000002."""
    return format(round(float(value), 3), "g")


def clock(seconds, separator):
    millis = round(float(seconds) * 1000)
    return f"{millis // 3600000:02d}:{millis // 60000 % 60:02d}:{millis // 1000 % 60:02d}{separator}{millis % 1000:03d}"


def composition(fiche):
    duration = number(fiche["film"]["duration_s"])
    root_open = (
        f'<div id="root" data-composition-id="main" data-no-timeline data-start="0" data-duration="{duration}" '
        'data-width="1920" data-height="1080">'
    )
    video = (
        f'<video id="form-capture" class="clip" src="{fiche["capture"]["media_ref"]}" muted playsinline '
        f'data-start="0" data-duration="{duration}" data-track-index="0" style="{VIDEO_STYLE}"></video>'
    )
    lines = [root_open, video]
    for i, scene in enumerate(fiche["scenes"], 1):
        voice, caption = scene["narration"], scene["caption"]
        lines.append(
            f'<audio id="voice{i}" src="{voice["audio_ref"]}" data-start="{number(voice["start_s"])}" '
            f'data-duration="{number(voice["duration_s"])}" data-track-index="{i}"></audio>'
        )
        lines.append(
            f'<div id="caption{i}" class="clip" data-start="{number(caption["start_s"])}" '
            f'data-duration="{number(caption["end_s"] - caption["start_s"])}" data-track-index="6" '
            f'style="{CAPTION_STYLE}">{html.escape(voice["text"], quote=False)}</div>'
        )
    return HEAD + "\n".join(lines) + "\n</div></body></html>\n"


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
        film["transcript_ref"]: "".join(
            s["narration"]["text"] + "\n" for s in fiche["scenes"]
        ),
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
    # Sans chemin, la fiche de ce dossier ; avec un chemin, celle d'un autre film.
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = Path(paths[0]).resolve() if paths else ROOT / "provenance-manifest.json"
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
