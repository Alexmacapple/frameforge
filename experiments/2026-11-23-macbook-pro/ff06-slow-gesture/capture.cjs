// Capture de la page de réservation à confirmation lente : les gestes de ce film, calés sur la fiche.
// Navigateur, pointeur, horloge, journal et conversion viennent de film-chain/capture_lib.cjs.
// Un geste est déclenché LEAD secondes après le début de sa phrase. Une scène sans geste, comme
// l'arrivée de la confirmation, attend seulement son résultat : rien n'est accéléré ni coupé.
const fs = require('fs');
const path = require('path');
const { record } = require('../film-chain/capture_lib.cjs');

const FICHE = JSON.parse(fs.readFileSync(path.join(__dirname, 'provenance-manifest.json'), 'utf8'));
const LEAD = 0.5;
const GLIDE = 0.7;

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

record({
  filmDir: __dirname,
  url: 'file://' + path.join(__dirname, FICHE.source.ref),
  durationS: FICHE.film.duration_s,
  mediaRef: FICHE.capture.media_ref,
  eventsRef: FICHE.capture.events_ref,
  play: async ({ page, at, glide, clickHere, mark }) => {
    const room = page.getByRole('button', { name: /Salle Érable/ });
    const book = page.getByRole('button', { name: 'Réserver' });
    // Ce que chaque événement de résultat attend dans la page, et la cible du geste s'il y en a un.
    const waits = {
      room_selected: () => page.locator('.room[aria-pressed="true"]').waitFor(),
      projector_checked: () => page.locator('#projector:checked').waitFor(),
      pending_visible: () => page.locator('#result.pending').waitFor(),
      confirmation_visible: () => page.locator('#result.confirmed').waitFor(),
    };
    const targets = {
      room_clicked: () => corner(room),
      projector_clicked: () => afterText(page.locator('label.option')),
      book_clicked: () => corner(book),
    };
    let pendingText = null;
    for (const scene of FICHE.scenes) {
      const click = scene.gesture_events.find((name) => targets[name]);
      if (click) {
        const clickAt = scene.narration.start_s + LEAD;
        await at(clickAt - GLIDE - 0.1);
        await glide(await targets[click](), GLIDE * 1000);
        await at(clickAt);
        await clickHere(110);
        mark(click);
      }
      await waits[scene.result.event]();
      mark(scene.result.event);
      // L'état d'attente est relu dans la page au moment où il apparaît, pas supposé.
      if (scene.result.event === 'pending_visible') pendingText = await page.locator('#result').innerText();
    }
    await at(FICHE.film.duration_s - 0.4);

    return {
      lead_s: LEAD,
      observed: {
        room: await page.locator('.room[aria-pressed="true"]').getAttribute('data-room'),
        projector: await page.locator('#projector').isChecked(),
        pending: pendingText,
        confirmation: await page.locator('#result').innerText(),
      },
      result_box: await page.locator('#result').boundingBox(),
    };
  },
});
