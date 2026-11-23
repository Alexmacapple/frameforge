// Capture du formulaire : les gestes de ce film, calés sur les repères de la narration.
// Navigateur, pointeur, horloge, journal et conversion viennent de film-chain/capture_lib.cjs.
const path = require('path');
const { record } = require('../../film-chain/capture_lib.cjs');

// Repères en secondes de film. La parole commence à 1,855 s, 5,540 s et 10,375 s.
const PLAN = {
  nameGlide: 0.9, nameClick: 1.55, nameType: 1.9,
  emailGlide: 4.6, emailClick: 5.25, emailType: 5.6,
  sendGlide: 9.5, sendClick: 10.45, end: 15.3,
};

// Le pointeur vise le bord droit de la cible pour ne masquer ni le texte saisi ni le libellé.
const target = async (locator, kind) => {
  const box = await locator.boundingBox();
  if (kind === 'button') return { x: box.x + box.width - 14, y: box.y + box.height - 10 };
  return { x: box.x + box.width * 0.85, y: box.y + box.height / 2 };
};

record({
  filmDir: __dirname,
  url: 'file://' + path.join(__dirname, '..', 'form-pilot', 'form.html'),
  durationS: 16,
  mediaRef: 'capture.mp4',
  eventsRef: 'capture-events.json',
  play: async ({ page, at, glide, clickHere, mark }) => {
    const name = page.getByLabel('Votre nom');
    const email = page.getByLabel('Votre adresse électronique');
    const send = page.getByRole('button', { name: 'Envoyer la demande' });

    await at(PLAN.nameGlide);
    await glide(await target(name, 'field'), 500);
    await at(PLAN.nameClick);
    await clickHere(90);
    mark('name_clicked');
    await at(PLAN.nameType);
    await page.keyboard.type('Camille Martin', { delay: 75 });
    mark('name_typed');

    await at(PLAN.emailGlide);
    await glide(await target(email, 'field'), 500);
    await at(PLAN.emailClick);
    await clickHere(90);
    mark('email_clicked');
    await at(PLAN.emailType);
    await page.keyboard.type('camille@example.test', { delay: 85 });
    mark('email_typed');

    await at(PLAN.sendGlide);
    await glide(await target(send, 'button'), 700);
    await at(PLAN.sendClick);
    await clickHere(120);
    mark('send_clicked');
    await page.getByRole('status').getByText('Demande enregistrée pour Camille Martin.').waitFor();
    mark('confirmation_visible');
    await at(PLAN.end);

    return {
      plan: PLAN,
      observed: {
        name: await page.locator('#name').inputValue(),
        email: await page.locator('#email').inputValue(),
        confirmation: await page.locator('#result').innerText(),
      },
    };
  },
});
