// Capture de la page des fenêtres modales : les gestes de ce film, calés sur la fiche.
// Navigateur, pointeur, horloge, journal et conversion viennent de film-chain/capture_lib.cjs.
// Chaque geste est déclenché à un décalage fixe après le début de sa phrase, au moment où la
// phrase le nomme. Les touches sont de vraies frappes clavier Playwright ; le pointeur ne bouge
// que pour les clics, puis s'écarte pour ne masquer ni le focus ni la fenêtre.
const fs = require('fs');
const path = require('path');
const { record } = require('../film-chain/capture_lib.cjs');

const FICHE = JSON.parse(fs.readFileSync(path.join(__dirname, 'provenance-manifest.json'), 'utf8'));
const GLIDE = 0.7;
const PARK = { x: 1760, y: 110 }; // coin haut droit, vide sur la page

// Le pointeur vise le coin bas droit de la cible pour ne pas masquer son libellé.
const corner = async (locator) => {
  const box = await locator.boundingBox();
  return { x: box.x + box.width - 16, y: box.y + box.height - 12 };
};

record({
  filmDir: __dirname,
  url: 'file://' + path.join(__dirname, FICHE.source.ref),
  durationS: FICHE.film.duration_s,
  mediaRef: FICHE.capture.media_ref,
  eventsRef: FICHE.capture.events_ref,
  play: async ({ page, at, glide, clickHere, mark }) => {
    const observed = {};
    const active = () => page.evaluate(() => document.activeElement.id || document.activeElement.tagName);
    // Le résultat est daté à l'image où le focus arrive : la page est relue à chaque image.
    const focusOn = (id) => page.waitForFunction((x) => document.activeElement.id === x, id);
    const start = (i) => FICHE.scenes[i].narration.start_s;
    if (FICHE.scenes.length !== 7) throw new Error('sept scènes attendues dans la fiche');

    const click = async (locator, atS, name) => {
      await at(atS - GLIDE - 0.1);
      await glide(await corner(locator), GLIDE * 1000);
      await at(atS);
      await clickHere(110);
      mark(name);
    };
    const press = async (key, atS, name) => {
      await at(atS);
      await page.keyboard.press(key);
      mark(name);
    };
    const park = () => glide(PARK, 600);

    // 1. Version fautive : la fenêtre s'ouvre, le focus reste sur le bouton de la page.
    await click(page.locator('#open-bad'), start(0) + 2.6, 'bad_open_clicked');
    await page.locator('#bad-overlay.open').waitFor();
    mark('bad_dialog_visible');
    observed.bad_focus_after_open = await active();
    await park();

    // 2. Tab : le focus part sur un lien de la page, derrière la fenêtre.
    await press('Tab', start(1) + 1.0, 'bad_tab_pressed');
    await focusOn('help-link');
    mark('bad_focus_left');
    observed.bad_focus_after_tab = await active();

    // 3. Échap : rien ne se passe. Fermeture à la souris, avec Annuler.
    await press('Escape', start(2) + 1.0, 'bad_escape_pressed');
    await page.waitForTimeout(400);
    observed.bad_open_after_escape = await page.locator('#bad-overlay.open').isVisible();
    mark('bad_still_open');
    await click(page.locator('#bad-cancel'), start(2) + 4.2, 'bad_cancel_clicked');
    observed.bad_closed_by_cancel = (await page.locator('#bad-overlay.open').count()) === 0;
    await park();

    // 4. Version corrigée : le focus entre dans la fenêtre, sur Annuler.
    await click(page.locator('#open-good'), start(3) + 3.0, 'good_open_clicked');
    await focusOn('good-cancel');
    mark('good_focus_inside');
    observed.good_focus_after_open = await active();
    observed.good_dialog_named = (await page.getByRole('dialog', { name: 'Supprimer votre compte ?' }).count()) === 1;
    await park();

    // 5. Deux Tab : Supprimer, puis retour sur Annuler.
    await press('Tab', start(4) + 1.0, 'good_tab1_pressed');
    await focusOn('good-delete');
    observed.good_focus_after_one_tab = await active();
    await press('Tab', start(4) + 3.0, 'good_tab2_pressed');
    await focusOn('good-cancel');
    mark('good_focus_wrapped');
    observed.good_focus_after_two_tabs = await active();

    // 6. Échap : la fenêtre se ferme, le focus revient sur le bouton d'ouverture.
    await press('Escape', start(5) + 1.0, 'good_escape_pressed');
    await focusOn('open-good');
    mark('good_focus_restored');
    observed.good_focus_after_escape = await active();
    observed.good_open_after_escape = await page.locator('#good-dialog').evaluate((d) => d.open);

    // 7. Tab : l'étape suivante, le parcours reprend.
    await press('Tab', start(6) + 1.2, 'resume_tab_pressed');
    await focusOn('next-step');
    mark('resume_focus_next');
    observed.focus_after_resume = await active();

    await at(FICHE.film.duration_s - 0.4);
    return { observed };
  },
});
