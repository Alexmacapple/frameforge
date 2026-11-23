// Capture du formulaire avec pointeur visible, gestes calés sur les repères de la narration.
//
// Ce qui est observé : les trois gestes réels (clics et frappes Playwright) et les états du DOM.
// Ce qui est ajouté pour la lisibilité : le pointeur orange, dessiné par un script injecté dans
// la page, qui suit les événements souris réels. La fixture form.html n'est pas modifiée.
const { chromium } = require('/Users/alex/.local/share/shipguard-runtime/node_modules/playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const FORM = path.join(__dirname, '..', 'form-pilot', 'form.html');
const MEDIA = path.join(__dirname, 'media');
// Décalage constaté entre l'horloge du script et le temps de la vidéo, en millisecondes.
const VIDEO_OFFSET_MS = Number(process.env.FF_VIDEO_OFFSET_MS || 0);
// Repères en secondes de film. La parole commence à 1,855 s, 5,540 s et 10,375 s.
const PLAN = {
  nameGlide: 0.9, nameClick: 1.55, nameType: 1.9,
  emailGlide: 4.6, emailClick: 5.25, emailType: 5.6,
  sendGlide: 9.5, sendClick: 10.45, end: 15.3,
};

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
    const wait = seconds * 1000 - VIDEO_OFFSET_MS - (Date.now() - t0);
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
  // Le pointeur vise le bord droit de la cible pour ne masquer ni le texte saisi ni le libellé.
  const target = async (locator, kind) => {
    const box = await locator.boundingBox();
    if (kind === 'button') return { x: box.x + box.width - 14, y: box.y + box.height - 10 };
    return { x: box.x + box.width * 0.85, y: box.y + box.height / 2 };
  };

  await page.goto('file://' + FORM);
  mark('page_loaded');
  await page.mouse.move(pos.x, pos.y);
  const name = page.getByLabel('Votre nom');
  const email = page.getByLabel('Votre adresse électronique');
  const send = page.getByRole('button', { name: 'Envoyer la demande' });

  await at(PLAN.nameGlide);
  await glide(await target(name, 'field'), 500);
  await at(PLAN.nameClick);
  await page.mouse.click(pos.x, pos.y, { delay: 90 });
  mark('name_clicked');
  await at(PLAN.nameType);
  await page.keyboard.type('Camille Martin', { delay: 75 });
  mark('name_typed');

  await at(PLAN.emailGlide);
  await glide(await target(email, 'field'), 500);
  await at(PLAN.emailClick);
  await page.mouse.click(pos.x, pos.y, { delay: 90 });
  mark('email_clicked');
  await at(PLAN.emailType);
  await page.keyboard.type('camille@example.test', { delay: 85 });
  mark('email_typed');

  await at(PLAN.sendGlide);
  await glide(await target(send, 'button'), 700);
  await at(PLAN.sendClick);
  await page.mouse.click(pos.x, pos.y, { delay: 120 });
  mark('send_clicked');
  await page.getByRole('status').getByText('Demande enregistrée pour Camille Martin.').waitFor();
  mark('confirmation_visible');
  await at(PLAN.end);

  const observed = {
    name: await page.locator('#name').inputValue(),
    email: await page.locator('#email').inputValue(),
    confirmation: await page.locator('#result').innerText(),
  };
  const video = await page.video().path();
  await context.close();
  await browser.close();

  // Conversion à 30 images par seconde, une image clé par seconde (exigence de HyperFrames) ;
  // la dernière image est prolongée jusqu'à 16 s.
  const raw = path.join(MEDIA, 'capture-pointer.webm');
  fs.renameSync(video, raw);
  const out = path.join(__dirname, 'capture.mp4');
  execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', raw, '-vf',
    'fps=30,tpad=stop_mode=clone:stop_duration=6,trim=duration=16,setpts=PTS-STARTPTS',
    '-an', '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p',
    '-r', '30', '-g', '30', '-keyint_min', '30', '-movflags', '+faststart', out]);
  const report = { plan: PLAN, video_offset_ms: VIDEO_OFFSET_MS, events, observed,
    pointer: 'dessiné par script injecté, positions des événements souris réels' };
  fs.writeFileSync(path.join(__dirname, 'capture-events.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report));
})().catch((e) => { console.error(e); process.exit(1); });
