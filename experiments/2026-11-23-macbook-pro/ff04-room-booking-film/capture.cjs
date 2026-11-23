// Capture de la page de réservation : les gestes de ce film, calés sur la fiche.
// Navigateur, pointeur, horloge, journal et conversion viennent de film-chain/capture_lib.cjs.
// Chaque geste est déclenché LEAD secondes après le début de sa phrase, lu dans la fiche.
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
    // Un geste par scène de la fiche, dans l'ordre : point visé, condition du résultat.
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
      await clickHere(110);
      mark(scene.gesture_events[0]);
      await gestures[i].done();
      mark(scene.result.event);
    }
    await at(FICHE.film.duration_s - 0.4);

    return {
      lead_s: LEAD,
      observed: {
        room: await page.locator('.room[aria-pressed="true"]').getAttribute('data-room'),
        projector: await page.locator('#projector').isChecked(),
        confirmation: await page.locator('#result').innerText(),
      },
      result_box: await page.locator('#result').boundingBox(),
    };
  },
});
