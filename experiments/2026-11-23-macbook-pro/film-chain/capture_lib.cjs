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
  || require('path').join(require('os').homedir(), '.local/share/shipguard-runtime/node_modules/playwright'));
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

// Un nom est pris dès qu'il existe, même si c'est un lien qui ne mène nulle part : existsSync
// suit les liens et dirait le nom libre.
const taken = (file) => fs.lstatSync(file, { throwIfNoEntry: false }) !== undefined;

// record({ filmDir, url, durationS, mediaRef, eventsRef, play })
//   play({ page, at, glide, clickHere, mark, appear }) joue les gestes du film et rend les champs
//   à ajouter au journal (au moins observed). at(s) attend l'instant s du film ; glide(point, ms)
//   déplace le pointeur ; clickHere(ms) clique là où il se trouve ; mark(nom) horodate ;
//   appear(sélecteur) attend qu'un élément soit affiché, à une image près.
async function capture({ filmDir, url, durationS, mediaRef, eventsRef, play }) {
  const outDir = process.env.FF_CAPTURE_OUT || filmDir;
  // La capture d'un film est figée par empreinte et n'existe qu'en un exemplaire local :
  // on ne l'écrase jamais. Pour une nouvelle prise, la retirer d'abord ou viser un autre dossier.
  for (const ref of [mediaRef, eventsRef]) {
    // Un nom de dépôt reste dans le dossier visé : ni chemin absolu, ni « .. », ni sous-dossier
    // qui serait un lien vers ailleurs.
    const parts = typeof ref === 'string' ? ref.split(/[\\/]/) : [];
    const through = parts.slice(0, -1).map((_, i) => path.join(outDir, ...parts.slice(0, i + 1)));
    if (!parts.length || path.isAbsolute(ref) || parts.includes('..')
      || through.some((dir) => taken(dir) && fs.lstatSync(dir).isSymbolicLink())) {
      throw new Error(`nom de dépôt hors du dossier de la capture, refusé : ${ref}`);
    }
    if (taken(path.join(outDir, ref))) {
      throw new Error(`capture existante, non écrasée : ${path.join(outDir, ref)} (définir FF_CAPTURE_OUT)`);
    }
  }
  // La prise brute va dans media : si ce nom est un lien, elle sortirait du dossier visé.
  const media = path.join(outDir, 'media');
  if (taken(media) && fs.lstatSync(media).isSymbolicLink()) {
    throw new Error(`media est un lien, rien n'est écrit à travers : ${media}`);
  }
  // Tout est produit dans un dossier de travail, puis posé à son nom final sans écraser : une
  // interruption ne laisse ni capture partielle au nom du film, ni fichier à moitié écrit.
  fs.mkdirSync(outDir, { recursive: true });
  const work = fs.mkdtempSync(path.join(outDir, '.capture-'));
  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      recordVideo: { dir: work, size: { width: 1920, height: 1080 } },
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
    // Pour dater un résultat qui se fait attendre : la page est relue à chaque image affichée.
    // locator.waitFor espace ses essais jusqu'à une demi-seconde, et mark() daterait alors le
    // résultat de 0,3 à 0,5 s trop tard (mesuré le 24 novembre 2026, Playwright 1.64.1).
    const appear = (selector) => page.waitForFunction((sel) => {
      const el = document.querySelector(sel);
      return Boolean(el) && el.getClientRects().length > 0;
    }, selector);

    await page.goto(url);
    mark('page_loaded');
    await page.mouse.move(pos.x, pos.y);
    const extra = await play({ page, at, glide, clickHere, mark, appear });
    // Le journal sert de preuve des résultats : sans observations, il ne prouve rien.
    if (!extra || typeof extra.observed !== 'object' || extra.observed === null) {
      throw new Error('play() doit rendre un objet avec le champ observed');
    }
    const video = await page.video().path();
    await context.close();
    await browser.close();
    browser = null;

    // Conversion à 30 images par seconde, une image clé par seconde (exigence de HyperFrames) ;
    // la dernière image est prolongée jusqu'à la durée du film.
    const converted = path.join(work, 'capture.mp4');
    execFileSync('ffmpeg', ['-v', 'error', '-i', video, '-vf',
      `fps=30,tpad=stop_mode=clone:stop_duration=6,trim=duration=${durationS},setpts=PTS-STARTPTS`,
      '-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p',
      '-r', '30', '-g', '30', '-keyint_min', '30', '-movflags', '+faststart', converted]);
    const report = { ...extra, events, pointer: POINTER_NOTE };
    const journal = path.join(work, 'journal.json');
    fs.writeFileSync(journal, JSON.stringify(report, null, 2) + '\n');
    // linkSync refuse un nom déjà pris : le contrôle fait au début ne suffit pas si un fichier
    // est apparu entre-temps.
    fs.linkSync(converted, path.join(outDir, mediaRef));
    try {
      fs.linkSync(journal, path.join(outDir, eventsRef));
    } catch (e) {
      // Pas de capture sans son journal : celle qui vient d'être posée est retirée.
      fs.unlinkSync(path.join(outDir, mediaRef));
      throw e;
    }
    // La prise brute est gardée pour examen, sous un nom libre : une prise précédente reste.
    fs.mkdirSync(media, { recursive: true });
    let raw = path.join(media, 'capture-pointer.webm');
    for (let n = 2; taken(raw); n++) raw = path.join(media, `capture-pointer-${n}.webm`);
    fs.copyFileSync(video, raw, fs.constants.COPYFILE_EXCL);
    console.log(JSON.stringify(report));
  } finally {
    if (browser) await browser.close().catch(() => {});
    fs.rmSync(work, { recursive: true, force: true });
  }
}

function record(options) {
  return capture(options).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { record };
