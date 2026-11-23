// Capture de la page de réservation, gestes calés sur les repères de narration de la fiche.
//
// Observé : trois clics Playwright réels et les états du DOM relus après coup.
// Ajouté pour la lisibilité : le pointeur orange, dessiné par un script injecté, qui suit les
// événements souris réels. La fixture booking.html n'est pas modifiée.
// Chaque geste est déclenché LEAD secondes après le début de sa phrase, lu dans la fiche.
const { chromium } = require('/Users/alex/.local/share/shipguard-runtime/node_modules/playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const FICHE = JSON.parse(fs.readFileSync(path.join(__dirname, 'provenance-manifest.json'), 'utf8'));
const MEDIA = path.join(__dirname, 'media');
const LEAD = 0.5;
const GLIDE = 0.7;

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

(async () => {
  fs.mkdirSync(MEDIA, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: { dir: MEDIA, size: { width: 1920, height: 1080 } },
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
  // Le pointeur vise le coin bas droit de la cible pour ne pas masquer son libellé.
  const corner = async (locator) => {
    const box = await locator.boundingBox();
    return { x: box.x + box.width - 16, y: box.y + box.height - 12 };
  };
  // Case à cocher : le clic vise la fin du libellé, pour que la coche reste visible ensuite.
  const afterText = async (locator) => {
    const box = await locator.boundingBox();
    const width = await locator.evaluate((el) => {
      const range = document.createRange();
      range.selectNodeContents(el);
      return range.getBoundingClientRect().width;
    });
    return { x: box.x + width + 26, y: box.y + box.height / 2 };
  };

  await page.goto('file://' + path.join(__dirname, FICHE.source.ref));
  mark('page_loaded');
  await page.mouse.move(pos.x, pos.y);
  const room = page.getByRole('button', { name: /Salle Érable/ });
  const projector = page.getByLabel('Ajouter un vidéoprojecteur');
  const book = page.getByRole('button', { name: 'Réserver' });
  // Un geste par scène de la fiche, dans l'ordre : cible, point visé, condition du résultat.
  const gestures = [
    { target: () => corner(room), done: () => page.locator('.room[aria-pressed="true"]').waitFor() },
    { target: () => afterText(page.locator('label.option')), done: () => page.locator('#projector:checked').waitFor() },
    { target: () => corner(book), done: () => page.locator('#result.visible').waitFor() },
  ];
  if (gestures.length !== FICHE.scenes.length) throw new Error('un geste attendu par scène de la fiche');
  for (let i = 0; i < gestures.length; i++) {
    const scene = FICHE.scenes[i];
    const clickAt = scene.narration.start_s + LEAD;
    await at(clickAt - GLIDE - 0.1);
    await glide(await gestures[i].target(), GLIDE * 1000);
    await at(clickAt);
    await page.mouse.click(pos.x, pos.y, { delay: 110 });
    mark(scene.gesture_events[0]);
    await gestures[i].done();
    mark(scene.result.event);
  }
  await at(FICHE.film.duration_s - 0.4);

  const observed = {
    room: await page.locator('.room[aria-pressed="true"]').getAttribute('data-room'),
    projector: await page.locator('#projector').isChecked(),
    confirmation: await page.locator('#result').innerText(),
  };
  const resultBox = await page.locator('#result').boundingBox();
  const video = await page.video().path();
  await context.close();
  await browser.close();

  // Conversion à 30 images par seconde, une image clé par seconde ; dernière image prolongée.
  const raw = path.join(MEDIA, 'capture-pointer.webm');
  fs.renameSync(video, raw);
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', raw, '-vf',
    `fps=30,tpad=stop_mode=clone:stop_duration=6,trim=duration=${FICHE.film.duration_s},setpts=PTS-STARTPTS`,
    '-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p',
    '-r', '30', '-g', '30', '-keyint_min', '30', '-movflags', '+faststart',
    path.join(__dirname, FICHE.capture.media_ref)]);
  const report = { lead_s: LEAD, events, observed, result_box: resultBox,
    pointer: 'dessiné par script injecté, positions des événements souris réels' };
  fs.writeFileSync(path.join(__dirname, FICHE.capture.events_ref), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report));
})().catch((e) => { console.error(e); process.exit(1); });
