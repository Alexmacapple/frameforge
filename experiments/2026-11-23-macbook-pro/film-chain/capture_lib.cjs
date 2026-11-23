// Partie commune des captures de démonstration web : navigateur, pointeur visible, horloge,
// journal des événements et conversion de la vidéo. Chaque film fournit seulement ses gestes.
//
// Ce qui est observé : les gestes Playwright réels du film et les états du DOM qu'il relit.
// Ce qui est ajouté pour la lisibilité : le pointeur orange, dessiné par un script injecté dans
// la page, qui suit les événements souris réels. La page filmée n'est pas modifiée.
//
// FF_CAPTURE_OUT : dossier de sortie de remplacement, pour essayer une capture sans toucher à
// celle du film, figée par empreinte. FF_PLAYWRIGHT : chemin du module Playwright.
const { chromium } = require(process.env.FF_PLAYWRIGHT
  || '/Users/alex/.local/share/shipguard-runtime/node_modules/playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const POINTER_NOTE = 'dessiné par script injecté, positions des événements souris réels';
const POINTER = `
(() => {
  const dot = document.createElement('div');
  dot.id = 'ff-pointer';
  dot.style.cssText = 'position:fixed;left:0;top:0;width:34px;height:34px;margin:-17px 0 0 -17px;' +
    'border-radius:50%;background:#ff6a00;border:4px solid #1b1b1b;box-sizing:border-box;' +
    'pointer-events:none;z-index:2147483647;transform:translate(-100px,-100px)';
  const place = (e) => { dot.style.transform = 'translate(' + e.clientX + 'px,' + e.clientY + 'px)'; };
  const attach = () => document.documentElement.appendChild(dot);
  if (document.documentElement) attach(); else document.addEventListener('DOMContentLoaded', attach);
  document.addEventListener('mousemove', place, true);
  document.addEventListener('mousedown', (e) => { place(e); dot.style.boxShadow = '0 0 0 18px rgba(255,106,0,.45)'; }, true);
  document.addEventListener('mouseup', () => { setTimeout(() => { dot.style.boxShadow = 'none'; }, 350); }, true);
})();`;

// record({ filmDir, url, durationS, mediaRef, eventsRef, play })
//   play({ page, at, glide, clickHere, mark }) joue les gestes du film et rend les champs à
//   ajouter au journal (au moins observed). at(s) attend l'instant s du film ; glide(point, ms)
//   déplace le pointeur ; clickHere(ms) clique là où il se trouve ; mark(nom) horodate.
async function capture({ filmDir, url, durationS, mediaRef, eventsRef, play }) {
  const outDir = process.env.FF_CAPTURE_OUT || filmDir;
  // La capture d'un film est figée par empreinte et n'existe qu'en un exemplaire local :
  // on ne l'écrase jamais. Pour une nouvelle prise, la retirer d'abord ou viser un autre dossier.
  for (const ref of [mediaRef, eventsRef]) {
    if (fs.existsSync(path.join(outDir, ref))) {
      throw new Error(`capture existante, non écrasée : ${path.join(outDir, ref)} (définir FF_CAPTURE_OUT)`);
    }
  }
  const media = path.join(outDir, 'media');
  fs.mkdirSync(media, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: media, size: { width: 1920, height: 1080 } },
  });
  await context.addInitScript(POINTER);
  const page = await context.newPage();
  const t0 = Date.now();
  const events = [];
  const mark = (name) => events.push({ name, script_s: (Date.now() - t0) / 1000 });
  const at = async (seconds) => {
    const wait = seconds * 1000 - (Date.now() - t0);
    if (wait > 0) await page.waitForTimeout(wait);
  };
  let pos = { x: 1500, y: 950 };
  const glide = async (dest, ms) => {
    const steps = Math.max(1, Math.round(ms / 20));
    const from = pos;
    for (let i = 1; i <= steps; i++) {
      const k = i / steps;
      const ease = k * k * (3 - 2 * k);
      await page.mouse.move(from.x + (dest.x - from.x) * ease, from.y + (dest.y - from.y) * ease);
      await page.waitForTimeout(20);
    }
    pos = dest;
  };
  const clickHere = (delay) => page.mouse.click(pos.x, pos.y, { delay });

  await page.goto(url);
  mark('page_loaded');
  await page.mouse.move(pos.x, pos.y);
  const extra = await play({ page, at, glide, clickHere, mark });
  const video = await page.video().path();
  await context.close();
  await browser.close();

  // Conversion à 30 images par seconde, une image clé par seconde (exigence de HyperFrames) ;
  // la dernière image est prolongée jusqu'à la durée du film.
  const raw = path.join(media, 'capture-pointer.webm');
  fs.renameSync(video, raw);
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', raw, '-vf',
    `fps=30,tpad=stop_mode=clone:stop_duration=6,trim=duration=${durationS},setpts=PTS-STARTPTS`,
    '-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p',
    '-r', '30', '-g', '30', '-keyint_min', '30', '-movflags', '+faststart',
    path.join(outDir, mediaRef)]);
  const report = { ...extra, events, pointer: POINTER_NOTE };
  fs.writeFileSync(path.join(outDir, eventsRef), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report));
}

function record(options) {
  return capture(options).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { record };
