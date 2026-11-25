# Rapport : « Le focus clavier », motion design à morphing continu

## Concept

L'anneau de focus orange est l'unique personnage du film. Tout le reste naît de lui ou de ce qu'il a déjà engendré, en un seul plan continu de 16 s :

- un point orange, d'où sort par balayage l'étiquette « Le focus clavier », s'étire en anneau ;
- l'anneau se contracte en bouton « Supprimer mon compte », et le bouton se dilate en page, dont le contenu se découvre par masquage ;
- une copie de l'anneau tombe comme une goutte, se remplit et devient la touche du clavier, puis cette touche s'étire en légende ;
- appui sur **Entrée** : une copie du bouton se soulève et grandit jusqu'à devenir la fenêtre. Le libellé « Supprimer mon compte » se recompose en « Supprimer votre compte ? » (« mon » roule vers « votre »). Un bouton unique se divise en Annuler et Supprimer, la page s'assombrit et l'anneau entre sur Annuler ;
- **Tab** : l'anneau passe sur Supprimer. Au **Tab** suivant, il sort par le bord droit de la fenêtre, masqué par elle, et rentre par le bord gauche sur Annuler. L'espace négatif de la fenêtre se lit comme une boucle fermée ;
- **Échap** : tout se replie dans l'ordre inverse, les boutons fusionnent et la fenêtre rentre dans le bouton d'origine, sur lequel l'anneau revient ;
- **Tab** : l'anneau rejoint « Étape suivante », et le parcours reprend.

Les légendes suivent la triade de la page de référence : **Entre / Reste / Revient / Reprend**.

## Horaires et itérations

- Début : 2026-11-25 17:56:17 CET. Fin : 2026-11-25 18:11:14 CET.
- Rendus : 5 au total. Quatre rendus complets de `media/essai.mp4` avec la commande imposée, plus un rendu de sondage en qualité « draft » vers le scratchpad, lancé pour diagnostiquer les polices.
- Retouches : 3 séries, soit 10 modifications.
  1. Après le rendu 1 :
     - polices locales ;
     - mots du titre attachés au repère de la fenêtre (ils se superposaient à l'étiquette du bouton) ;
     - masque du mot « mon/votre » resserré ;
     - départ de l'anneau retardé, pour qu'il n'arrive qu'une fois les boutons formés ;
     - fenêtre compactée ;
     - mesures de texte recalculées au rendu.
  2. Après le rendu 3 :
     - remplissage du point vidé plus tôt (il formait un rectangle brun terne) ;
     - légende qui dépassait de la touche avant son élargissement.
  3. Après le rendu 4 : étiquette d'ouverture révélée par balayage depuis le point, car le glissement montrait d'abord « er ».

## Ce qui a été vérifié, et comment

- **Fidélité à `modales.html`** : lecture du code de la version corrigée. `showModal()` puis `first.focus()` donne le focus initial sur Annuler. Tab depuis Supprimer revient sur Annuler. L'événement `close` déclenche `opener.focus()`. Le lien suivant dans l'ordre du document est « Étape suivante ». La vidéo montre ces comportements, et seulement eux. La touche Entrée ouvre la fenêtre parce que c'est le comportement natif d'un `<button>` qui a le focus (même gestionnaire de clic) : c'est la seule libre adaptation par rapport à la narration, qui parle de clic.
- **Aucun réseau au rendu** :
  - diagnostic : au premier rendu, HyperFrames 0.8.33 a substitué Inter à « Avenir Next » et « Helvetica Neue » (table `FONT_ALIAS_MAP`) et l'a téléchargée depuis Google Fonts ;
  - correction : une famille « FocusSans » déclarée par `@font-face` en `local()` ; le compilateur ne traite pas les familles déjà déclarées ;
  - preuve : les trois derniers rendus ont tourné dans un `sandbox-exec` qui refuse tout réseau sortant hors boucle locale, avec un `HYPERFRAMES_FONT_CACHE_DIR` vide. On a obtenu un code de sortie 0, aucune ligne « Fetched … font » et un cache resté vide. Le blocage a été contrôlé à part : `curl` vers fonts.googleapis.com échoue dans le bac à sable (code 7) et répond 200 hors de lui.
- **Format** (ffprobe) : h264, 1920 × 1080, 30 i/s, 480 images, 16,0 s, sans piste audio.
- **Lint HyperFrames** : 0 erreur, 1 avertissement (fichier de plus de 400 lignes). Il est conservé volontairement : un plan unique se prête mal au découpage en sous-compositions.
- **Examen visuel** : quatre planches de 12 images extraites avec ffmpeg, plus deux images en pleine résolution. Les défauts repérés ont été corrigés, puis contrôlés sur la planche suivante.
- **Clignotement** : luminance moyenne (YAVG) mesurée sur les 480 images. Elle reste entre 34 et 98, avec un saut maximal de 8,25 d'une image à l'autre, toujours dans des transitions progressives : aucun éclair. Il n'y a aucun mouvement plein écran ; seul l'assombrissement de l'arrière-plan couvre l'écran, en 0,8 s.
- **Contrastes de texte** (WCAG, calculés) : légende 14,9:1, touche 16,3:1, titre 16,3:1, description 9,6:1, bouton rouge 6,5:1, lien 6,4:1, étiquette d'ouverture 10,3:1. L'anneau atteint 5,1:1 sur fond sombre et 3,6:1 sur blanc (au moins 3:1 pour un élément graphique).

## Ce qui n'a pas pu être vérifié

- Pas de visionnage en temps réel image par image : la qualité des courbes (anticipation, dépassement) a été jugée sur des images fixes et d'après le code des courbes.
- Les textes de la page sous l'assombrissement (fenêtre ouverte) ont un contraste réduit, non mesuré. C'est volontaire, puisqu'ils figurent l'arrière-plan inerte, mais ils ne servent pas de support de lecture.
- Le rendu dépend de la police système Avenir Next de macOS. Sur une machine qui n'a pas cette police, `local()` échoue et le texte retombe sur `sans-serif` : la mise en page reste juste, car les mesures sont refaites au rendu, mais le dessin change. Cela n'a pas été testé hors de cette machine.
- Le test de lecture « par un spectateur qui ne connaît pas le sujet » n'a pas été mené avec une vraie personne.
