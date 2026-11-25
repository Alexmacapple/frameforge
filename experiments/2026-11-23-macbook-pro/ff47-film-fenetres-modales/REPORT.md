# Film de référence : fenêtres modales et focus clavier (ticket 47)

Produit le 25 novembre 2026 sur le MacBook Pro, depuis `main` à `b8dc9f0`, branche `feature/film-fenetres-modales`. Chaîne utilisée : `film-chain/` telle quelle, sans modification ni nouveau skill. Statut : **REVIEWED** le 25 novembre à 11 h 12, approbation éditoriale d'Alex consignée dans `EDITORIAL-APPROVAL.md` pour l'empreinte `d10c50b8…0845`. Aucune autorisation de diffusion.

## Le film

- Sujet validé le 25 novembre : accessibilité des fenêtres modales, public développeurs web, français.
- 54 secondes, 7 scènes, une seule capture continue d'une page locale (`modales.html`) qui porte deux versions de la même fenêtre de suppression de compte.
- Version fautive : la fenêtre s'ouvre mais le focus reste sur la page ; Tab part sur un lien derrière la fenêtre ; Échap ne fait rien ; fermeture à la souris.
- Version corrigée : `dialog` natif ouvert par `showModal()`, focus initial sur Annuler (l'action la moins risquée), Tab qui boucle dans la fenêtre, Échap qui ferme, focus rendu au bouton d'ouverture, puis reprise du parcours.
- Livrables locaux, non versionnés : `media/fenetres-modales.mp4`, `media/fenetres-modales-son-seul.m4a` (pour le ticket 35). Versionnés : `captions.srt`, `captions.vtt`, `transcript.txt`.
- Écart au storyboard du ticket 47 : pas de scène d'introduction de 8 secondes. Chaque scène de la chaîne doit porter un geste observé ; le titre d'ouverture (« Fenêtres modales : le focus au clavier ») tient lieu d'introduction.

## Preuves

- Capture : 17 événements datés et 11 observations relevées dans le DOM pendant la prise (`capture-events.json`), toutes égales à l'attendu. Les touches sont de vraies frappes Playwright ; le pointeur n'est dessiné que pour les clics.
- Sonde préalable de la page, hors film : mêmes états, plus un témoin négatif (en version corrigée, un clic sur l'arrière-plan est bloqué).
- `check_manifest.py` : 13 PASS, 5 UNVERIFIED déclarés (contrôles humains), code 2.
- Garde : deux rendus gardés successifs, même empreinte `d10c50b8657efe9e8f218231200c588eb35d61411c5bd79b5467607c31d0a845`, égale à celle portée par la fiche. `repin.py --check` : PASS.
- `test_fenetres_modales.py` : 9 tests, exit 0, dont trois cas négatifs (clip de voix altéré refusé, focus sorti de la fenêtre corrigée refusé par la fiche, résultat daté hors de son sous-titre refusé).
- Planche de 12 images du premier brouillon regardée par l'agent : focus visible à chaque étape, pointeur garé hors de l'action. Elle a fait trouver un défaut (fenêtre qui débordait de quelques pixels à droite), corrigé avant la seconde prise.

## Mesures

Horodatages de la session, temps de calcul compris. Temps actif de l'agent et temps de calcul ne sont pas séparés.

- 10:53 à 10:54 : reprise, lecture des documents, vérification de l'environnement (voix Kokoro 0.9.4, ffmpeg 9.0.1, Node 24, HyperFrames 0.8.33 en cache).
- 10:54 à 10:55 : page de démonstration et sonde de son comportement.
- 10:55 à 10:56 : fiche brouillon et synthèse des 7 phrases (10 s de calcul).
- 10:56 à 10:57 : première capture (61 s).
- 10:57 à 10:59 : lecture du garde, recherche du réglage de télémétrie, premier brouillon témoin (59 s).
- 10:59 à 11:01 : planche, défaut trouvé, correction, seconde capture : **une reprise**.
- 11:01 à 11:02 : second brouillon témoin (57 s), référence de sortie, empreintes.
- 11:02 à 11:04 : deux rendus gardés (59 et 58 s).
- 11:04 à 11:06 : tests du film, compte rendu.
- Total : environ 13 minutes, du « ok » d'Alex au film gardé. Une intervention humaine (le « ok »), une reprise, aucune erreur de rendu.
- Non mesuré : le temps humain de visionnage et d'écoute, encore à venir.

## Difficultés relevées pour le ticket 56

Consignées sans être corrigées, comme le demande le brief. Pour chacune : besoin, preuve, existant, limite, bénéfice attendu.

1. **Écrire la fiche.** Besoin : poser les repères depuis les durées mesurées. Preuve : `ecrire_fiche.py`, écrit pour ce film. Existant : le README dit « poser les repères dans la fiche », sans outil. Limite : un script par film, qui peut écraser une fiche rendue (garde ajoutée à la main). Bénéfice : moins d'erreurs de calcul, et le même script pour le prochain film.
2. **Référence de sortie du brouillon témoin.** Besoin : `output-reference.json` depuis le brouillon. Preuve : `reference_sortie.py`, écrit pour ce film en réutilisant les fonctions du garde. Existant : aucune commande ; le rendu du témoin lui-même se fait à la main (copie isolée, `npx hyperframes render`). Bénéfice : l'étape 6 du README devient une commande.
3. **Télémétrie de HyperFrames activée sur ce Mac.** Preuve : `~/.hyperframes/config.json` porte `telemetryEnabled: true` et 101 rendus réussis comptés. Le garde transmet l'environnement tel quel au rendu. Existant : `HYPERFRAMES_NO_TELEMETRY=1` et `DO_NOT_TRACK=1`, lus par le paquet 0.8.33 (relevé dans `dist/cli.js`), posés à la main pour les rendus de ce film et dans son `package.json`. Limite : les rendus des autres films n'en bénéficient pas ; absence de trafic non mesurée. Décision à prendre par Alex (`hyperframes telemetry disable`, ou variable posée par le garde commun).
4. **Contrôle de fiche sans fichier d'empreintes.** Preuve : `check_manifest.py` sort sur une trace Python (`FileNotFoundError`) au lieu d'un FAIL lisible. Bénéfice : un verdict, comme pour les autres manques.
5. **Sous-titres longs.** Preuve : une phrase par repère, jusqu'à 135 caractères sur deux lignes de cartouche. Existant : aucun découpage dans `build_from_fiche.py`. Limite : lisibilité à juger au visionnage, pas mesurée.
6. **Planche d'images.** Preuve : le README demande de « regarder une planche », sans outil ; le ffmpeg de ce Mac n'a pas le filtre `drawtext`, la planche est donc sans horodatage. Elle a pourtant trouvé le seul défaut du film. C'est le besoin que la contre-revue de #56 réserve à un essai du contrôle visuel de HyperFrames : à comparer d'abord à cette planche simple.
7. **Prononciation non vérifiable par l'agent.** Preuve : seuls des modèles de transcription anglais sont présents (`faster-whisper` `.en`). « Tab » et « Échap » restent à écouter (ticket 36).
8. **Avertissement de HyperFrames.** `timeline_track_too_dense` (7 éléments sur une piste) : sans effet sur le rendu, rien à faire.

Suites données le même jour : les constats 1 et 2 sont repris dans la chaîne (`film-chain/place_cues.py` et `film-chain/witness_reference.py`), qui redonnent exactement les valeurs de ce film ; les deux scripts écrits pour lui sont retirés. Le constat 4 est corrigé dans `check_manifest.py`. Le constat 3 est tranché : télémétrie coupée par Alex sur le MacBook Pro (`hyperframes telemetry disable`).

## Ce qui reste à faire

- Fait : visionnage et approbation éditoriale par Alex (« très bien », puis « oui » à la question d'approbation). Médias copiés dans `~/Claude-worktrees/frameforge-medias-approuves/2026-11-25/`, empreintes vérifiées par `shasum -c`.
- Tickets 35 et 36 : écoute sans l'image par une personne qui découvre le film, voix comparée aux sous-titres phrase par phrase.
- Aucun lecteur d'écran n'a été testé : le film montre le focus clavier et l'état du DOM, pas une restitution vocale. Les recommandations citées sont celles du motif de dialogue modal du W3C ; aucun critère RGAA n'est cité dans le film.
- Aucune diffusion ni copie du film hors de ce Mac sans accord d'Alex sur la version et la destination.
