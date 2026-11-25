"""Génère la composition de l'insert animé (ticket 59) et ses sous-titres.

Schéma du piège du focus réussi, en trois temps calés sur les trois phrases : la fenêtre s'ouvre
et le focus y entre ; Tab le fait tourner entre Annuler et Supprimer ; Échap ferme la fenêtre et
rend le focus au bouton de départ.

L'animation n'utilise pas GSAP : HyperFrames 0.8.33 pilote tout objet de window.__timelines qui
sait se positionner (seek, totalTime, duration). Ici, l'état de chaque élément est une fonction
pure du temps : aucun réseau au rendu, et la même image pour le même instant.

Les sous-titres suivent la règle de la fiche en version 3 (build_from_fiche.split_caption).
"""

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "film-chain"))
b = importlib.import_module("build_from_fiche")

FIRST, GAP, PAD, TAIL = 0.4, 0.4, 0.3, 0.8


def timings():
    clips = json.loads((ROOT / "narration-synthesis.json").read_text())["clips"]
    out, t = [], FIRST
    for clip in clips:
        out.append((clip, round(t, 3), round(t + clip["duration_s"], 3)))
        t += clip["duration_s"] + GAP
    return out, round(t - GAP + TAIL, 3)


def pseudo_fiche(steps):
    """La forme que caption_cues lit : version 3, une scène par phrase."""
    return {
        "manifest_version": 3,
        "scenes": [
            {
                "narration": {"text": clip["text"]},
                "caption": {"start_s": start, "end_s": round(end + PAD, 3)},
            }
            for clip, start, end in steps
        ],
    }


SCRIPT = r"""
(function () {
  const T = __TIMES__, D = __DURATION__;
  const $ = (id) => document.getElementById(id);
  const clamp = (x) => Math.min(1, Math.max(0, x));
  const seg = (t, a, b) => clamp((t - a) / (b - a));
  const inOut = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
  // Léger dépassement à l'arrivée, puis stabilisation.
  const back = (x) => { const c = 1.4; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  const mix = (a, b, k) => a + (b - a) * k;
  // Position à l'écran, mesurée par rapport à l'image entière, agrandissement de la fenêtre compris.
  const box = (id) => {
    const r = $(id).getBoundingClientRect(), o = $("__ROOT__").getBoundingClientRect();
    return [r.left - o.left, r.top - o.top, r.width, r.height];
  };
  let cur = 0;

  function ringTo(r, a, b, k) {
    const p = a.map((v, i) => mix(v, b[i], k));
    r.style.left = p[0] - 10 + "px"; r.style.top = p[1] - 10 + "px";
    r.style.width = p[2] + 20 + "px"; r.style.height = p[3] + 20 + "px";
  }

  function at(t) {
    const [s1, s2, s3] = T;
    const page = box("page-button"), cancel = box("cancel"), del = box("delete");
    // Ouverture, puis fermeture de la fenêtre.
    const open = inOut(seg(t, s1 + 0.2, s1 + 1.0)) * (1 - inOut(seg(t, s3 + 0.4, s3 + 1.1)));
    $("dialog").style.opacity = open;
    $("dialog").style.transform = "scale(" + mix(0.9, 1, open) + ")";
    $("backdrop").style.opacity = 0.35 * open;
    // Le focus : bouton de la page, Annuler, Supprimer, Annuler, bouton de la page.
    const legs = [
      [page, cancel, s1 + 0.9, s1 + 1.7],
      [cancel, del, s2 + 0.35, s2 + 0.8],
      [del, cancel, s2 + 1.65, s2 + 2.1],
      [cancel, page, s3 + 0.6, s3 + 1.5],
    ];
    let from = page, to = page, k = 0;
    for (const [a, b, start, end] of legs) {
      if (t >= start) { from = a; to = b; k = t >= end ? 1 : back(seg(t, start, end)); }
    }
    ringTo($("ring"), from, to, k);
    // La touche : Tab pendant la deuxième phrase, Échap pendant la troisième, enfoncée à chaque appui.
    const key = $("key");
    const shown = seg(t, s2 - 0.2, s2) * (1 - seg(t, s3 + 1.4, s3 + 1.8));
    key.style.opacity = shown;
    key.textContent = t < s3 - 0.1 ? "Tab" : "Échap";
    const presses = [s2 + 0.3, s2 + 1.6, s3 + 0.3];
    const down = presses.some((p) => t >= p && t < p + 0.18);
    key.style.transform = "translateX(-50%) scale(" + (down ? 0.92 : 1) + ")";
    key.style.boxShadow = down ? "0 2px 0 #adb5bd" : "0 8px 0 #adb5bd";
    // La boucle sous les deux boutons se dessine pendant les deux appuis sur Tab.
    const loop = $("loop-path"), length = loop.getTotalLength();
    loop.style.strokeDasharray = length;
    loop.style.strokeDashoffset = length * (1 - inOut(seg(t, s2 + 0.4, s2 + 2.2)));
    $("loop").style.opacity = open;
  }

  const timeline = {
    duration: () => D,
    time: () => cur,
    totalTime(t) { if (t === undefined) return cur; cur = t; at(t); return this; },
    seek(t) { if (t === undefined) return cur; cur = t; at(t); return this; },
    progress(p) { if (p === undefined) return cur / D; cur = p * D; at(cur); return this; },
    pause() { return this; },
    play() { return this; },
    timeScale() { return 1; },
  };
  window.__timelines = window.__timelines || {};
  window.__timelines["__KEY__"] = timeline;
  at(0);
})();
"""

STYLE = """
#page{position:absolute;left:160px;top:300px;width:600px;height:340px;background:#fff;
 border-radius:18px;box-shadow:0 4px 18px rgba(17,24,39,.08);padding:44px;color:#111}
#page h2{margin:0 0 70px;font-size:40px}
.button{position:absolute;display:flex;align-items:center;justify-content:center;font-size:32px;
 border-radius:10px}
#page-button{left:44px;top:190px;width:380px;height:84px;border:2px solid #343a40;color:#111;
 background:#fff}
#backdrop{position:absolute;inset:0;background:#111827;opacity:0}
#dialog{position:absolute;left:900px;top:250px;width:820px;height:440px;background:#fff;
 border-radius:20px;box-shadow:0 20px 50px rgba(17,24,39,.25);padding:48px 60px;color:#111;
 transform-origin:30% 50%;opacity:0}
#dialog h2{margin:0 0 12px;font-size:44px}
#dialog p{margin:0;font-size:30px;color:#495057}
#cancel{left:60px;top:250px;width:240px;height:88px;border:2px solid #343a40;background:#fff}
#delete{left:340px;top:250px;width:280px;height:88px;background:#c92a2a;color:#fff}
#loop{position:absolute;left:0;top:0;width:820px;height:440px;overflow:visible}
#ring{position:absolute;border:6px solid #f76707;border-radius:16px;pointer-events:none}
#key{position:absolute;left:50%;top:90px;min-width:220px;height:104px;padding:0 36px;
 transform:translateX(-50%);background:#fff;border:3px solid #343a40;border-radius:16px;
 display:flex;align-items:center;justify-content:center;font-size:48px;font-weight:700;
 color:#111;opacity:0}
"""


# Les éléments animés, un bloc par ligne de la composition.
VISUALS = [
    (
        '<div id="page"><h2>Supprimer son compte</h2>'
        '<div id="page-button" class="button">Supprimer mon compte</div></div>'
    ),
    '<div id="backdrop"></div>',
    (
        '<div id="dialog"><h2>Supprimer votre compte ?</h2>'
        "<p>Cette action est définitive.</p>"
        '<svg id="loop" viewBox="0 0 820 440"><path id="loop-path" fill="none" '
        'stroke="#f76707" stroke-width="4" stroke-linecap="round" opacity=".7" '
        'd="M 30 294 A 310 78 0 1 0 650 294 A 310 78 0 1 0 30 294"/></svg>'
        '<div id="cancel" class="button">Annuler</div>'
        '<div id="delete" class="button">Supprimer</div></div>'
    ),
    '<div id="ring"></div>',
    '<div id="key">Tab</div>',
]


def script(times, duration, root_id, key):
    """Animation : instants des trois phrases, durée, racine mesurée, clé de la timeline."""
    return (
        SCRIPT.replace("__TIMES__", json.dumps(times))
        .replace("__DURATION__", b.number(duration))
        .replace("__ROOT__", root_id)
        .replace("__KEY__", key)
    )


def embedded(times, duration):
    """Sous-composition pour un film : l'animation seule, sans voix ni sous-titres.

    Voix et sous-titres viennent de la fiche du film. La racine et la clé de la timeline portent
    leur propre nom, pour ne pas se confondre avec celles du film.
    """
    return (
        b.HEAD_V2.replace("</style>", STYLE.replace("\n", "") + "</style>")
        + f'<div id="insert-root" data-composition-id="insert" data-start="0" '
        f'data-duration="{b.number(duration)}" data-width="1920" data-height="1080" '
        # Fond déclaré : l'insert couvre la capture, qui s'arrête quand il commence.
        'style="position:absolute;inset:0;background:#f6f7fa">\n'
        + "\n".join(VISUALS)
        + f"\n<script>{script(times, duration, 'insert-root', 'insert')}</script>"
        + "\n</div></body></html>\n"
    )


def composition(steps, duration):
    fiche = pseudo_fiche(steps)
    parts = [
        b.HEAD_V2.replace("</style>", STYLE.replace("\n", "") + "</style>"),
        (
            f'<div id="root" data-composition-id="main" data-start="0" '
            f'data-duration="{b.number(duration)}" data-width="1920" data-height="1080">'
        ),
        *VISUALS,
    ]
    for i, (clip, start, _) in enumerate(steps, 1):
        parts.append(
            f'<audio id="voice{i}" src="{clip["audio_ref"]}" data-start="{b.number(start)}" '
            f'data-duration="{b.number(clip["duration_s"])}"></audio>'
        )
    shown = 0
    for cues in b.caption_cues(fiche):
        for start, end, lines in cues:
            shown += 1
            parts.append(
                f'<div id="caption{shown}" class="clip" data-start="{b.number(start)}" '
                f'data-duration="{b.number(end - start)}" '
                f'style="{b.CARTOUCHE_STYLE}">{" ".join(lines)}</div>'
            )
    times = [start for _, start, _ in steps]
    parts.append(f"<script>{script(times, duration, 'root', 'main')}</script>")
    return "\n".join(parts) + "\n</div></body></html>\n"


def main():
    steps, duration = timings()
    (ROOT / "index.html").write_text(composition(steps, duration))
    srt = b.subtitles(pseudo_fiche(steps), ",", numbered=True)
    (ROOT / "captions.srt").write_text(srt)
    (ROOT / "transcript.txt").write_text("".join(c["text"] + "\n" for c, _, _ in steps))
    print(
        json.dumps(
            {"status": "PASS", "duration_s": duration, "steps": [s[1:] for s in steps]}
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
