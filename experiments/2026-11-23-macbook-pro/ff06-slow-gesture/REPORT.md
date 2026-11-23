# Cas temporel adversarial — un geste plus lent que la voix

23 novembre 2026, MacBook Pro. Second cas de l'expérience 2 de la feuille de route adoptée (issue 13 ; issue 6). Playwright 1.64.1, HyperFrames 0.8.33, FFmpeg 9.0.1, Kokoro 0.9.4. Relevé établi par un agent ; aucun visionnage humain.

## Hypothèse à réfuter

« Les contraintes temporelles usuelles ne font pas disparaître geste, résultat ou parole. » Échec si un mot, un résultat ou une attente significative disparaît sans que ce soit signalé.

## Le cas

Copie du film de réservation de salle. Un seul changement dans la page (`booking-slow.html`) : après le clic sur « Réserver », un état « Réservation en cours… » s'affiche, et la confirmation n'arrive que six secondes plus tard. Le film approuvé, ses entrées et les outils communs ne sont pas touchés.

## Cas naïf : la fiche du film témoin, la page lente

La fiche est reprise telle quelle : trois scènes, quinze secondes, la troisième phrase annonce la confirmation.

- La capture s'arrête à 15 s. La confirmation arrive après : le journal la relève à 16,03 s.
- **Rendu direct par HyperFrames, sans vérificateur : code 0, aucun avertissement. Le message de confirmation n'apparaît dans aucune image du film** (saturation de la zone de message mesurée sur les 450 images : jamais de vert), alors que la voix l'annonce.
- **Contrôle de la fiche : refus avant tout rendu.** `FAIL gestures — reservation-confirmee : résultat à 16.027 s, hors du sous-titre qui l'annonce`.

La perte existe donc sans la chaîne, et la chaîne existante la signale. Rien à corriger dans les outils.

## Version ajustée

L'attente est gardée en entier et dite. La fiche passe à quatre scènes et vingt secondes :

1. « Choisir la salle Érable. »
2. « Ajouter un vidéoprojecteur. »
3. « La réservation est envoyée. » : clic, puis état d'attente observé dans la page.
4. « Un message confirme la salle et l'option. » : scène sans geste, placée à l'arrivée de la confirmation.

Seuls la fiche et les gestes de `capture.cjs` ont été écrits ; composition, sous-titres et transcription sortent de la fiche.

Mesures sur le film rendu par le garde (`media/slow-gesture.mp4`, SHA-256 `499cc9e7acbddd3d8a1556c8dc442190f8c5573346b71f198fc062bbb7b940c6`, DRAFT) :

- Fiche : 13 PASS, 3 UNVERIFIED (les trois contrôles humains ouverts), 0 FAIL.
- Deux rendus gardés successifs identiques à l'octet ; aucun processus Chrome restant.
- Les quatre phrases sont entières dans le film : corrélation minimale avec les clips d'origine, par demi-seconde, de 0,999.
- L'attente est visible sans coupe ni accélération : état gris à 9,63 s, message vert à 15,63 s, soit 6,00 s, la durée réelle de la page.
- Pointeur visible aux trois clics (23 à 25 pixels de sa couleur 0,15 s après chaque clic).
- Les trois gestes suivent le début de leur phrase de 0,32 à 0,37 s.

## Ce que l'essai a révélé

**Le journal date un résultat attendu avec environ 0,4 s de retard.** Pour la confirmation, le journal dit 16,03 s ; l'image dit 15,63 s. Pour un résultat qui suit un clic, l'écart est de 0,1 s. Conséquence dans ce film : la quatrième phrase commence à être prononcée à 15,98 s, 0,35 s *après* l'apparition du message, et non juste avant comme le laisse croire le journal. Le sous-titre, lui, s'ouvre à 15,6 s, en même temps que le message. Ce n'est pas une disparition, et le contrôle de la fiche reste du bon côté (il refuse plus tôt, pas plus tard) ; mais un contrôle de synchronisation fin ne peut pas s'appuyer sur le journal pour une scène sans geste. Cause non établie (hypothèse à vérifier : délai d'interrogation de l'attente Playwright).

**Le repère de la scène d'attente vient d'une première capture.** La phrase 4 est placée à 15,6 s parce que la capture naïve avait mesuré le délai. Avec une page au délai variable, ce repère serait faux d'une capture à l'autre ; la fiche le refuserait, mais il faudrait capturer d'abord et placer la voix ensuite.

## Verdict

L'hypothèse n'est pas réfutée pour ce cas : sans garde, HyperFrames livre un film où le résultat annoncé n'apparaît jamais, sans avertissement ; avec la chaîne, ce film est refusé avant rendu, et la version ajustée montre toute l'attente et toutes les phrases.

## Non vérifié

- Visionnage et écoute par une personne ; compréhension sans l'image ; voix comparée au texte.
- Six secondes d'attente à l'écran sont-elles supportables pour un spectateur ? Jugement éditorial, non tranché ici.
- Délai variable, résultat qui n'arrive jamais, page distante.
- Temps de travail : environ vingt-cinq minutes d'agent, estimation non chronométrée.

## Reproduire

Les médias ne sont pas versionnés. `synthesize_kokoro.py` (environnement Kokoro hors dépôt), `node capture.cjs`, `python3 -B ../film-chain/repin.py .`, puis `python3 -B render_guarded.py`. La voix Kokoro n'étant pas reproductible à l'échantillon, un film refait n'aura pas la même empreinte.
