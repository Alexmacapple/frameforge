# Le focus clavier — motion design à morphing continu

Adaptation du prompt « Hammy » (vidéo « La meilleure façon de créer des animations graphiques avec Claude AI ») à un sujet d'accessibilité. Même exigence créative ; sujet, références et cadre technique changés.

## Mission

Crée une animation de motion design d'environ 15 secondes qui fait comprendre **le bon comportement du focus clavier dans une fenêtre modale** : à l'ouverture, le focus entre dans la fenêtre ; Tab le fait tourner entre ses boutons sans en sortir ; Échap ferme la fenêtre et rend le focus au bouton qui l'avait ouverte.

Aborde ce projet comme un motion designer de tout premier plan qui réalise la pièce maîtresse de son portfolio. Prends la pleine maîtrise du concept, de la chorégraphie, du rythme et des transitions. Ne suis pas de structure de scènes imposée.

**Rien n'apparaît. Tout se transforme.** Un seul plan continu, sans coupe : chaque forme naît d'une transformation visible d'une forme qui existe déjà.

## Références, dans `references/`

- `modales.html` : la page de démonstration, avec une version fautive et une version corrigée de la fenêtre. Ouvre-la, lis son code : c'est la source de vérité du comportement.
- `narration-film-47.txt` : le texte du film pédagogique tourné sur cette page.
- `planche-film-47.png` : douze images de ce film.

Utilise-les pour comprendre le sujet, pas comme un storyboard à reproduire. Si une référence est inaccessible, signale-le plutôt que d'en inventer le contenu.

## Exigences de mouvement

Morphing de tracés, interpolation de formes, division et fusion, masquage, espace négatif, typographie cinétique, correspondance de formes : combine-les en un langage unifié, sans liste à cocher. Courbes d'animation soignées (anticipation, dépassement léger, stabilisation). Retenue : rien de décoratif sans raison.

L'animation doit **enseigner**, pas seulement impressionner : un spectateur qui ne connaît pas le sujet doit comprendre les trois comportements, en lisant les touches et les mots à l'écran.

## Cadre technique imposé

- **HyperFrames 0.8.33**, exactement : `npx --yes hyperframes@0.8.33 render DOSSIER --output=media/essai.mp4 --workers=2 --no-best-effort`, avec `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1` dans l'environnement. Ne pas installer de plugin ni d'autre version.
- Composition dans `index.html` à la racine de ce dossier, 1920 × 1080, 30 images par seconde.
- **Aucun réseau au rendu** : pas de GSAP ni de police chargés depuis un CDN. HyperFrames pilote tout objet de `window.__timelines["<id>"]` qui expose `duration()`, `seek(t)`, `totalTime(t)`, `time()`, `progress(p)`, `pause()`, `play()`, `timeScale()` ; écris l'état de chaque élément comme une fonction pure du temps. La racine porte `data-composition-id` ; la clé de `window.__timelines` doit être cet identifiant.
- Pas de son.
- Accessibilité de l'animation elle-même : aucun clignotement de plus de 3 éclairs par seconde ; contrastes de texte suffisants ; pas de mouvement violent plein écran.

## Livrables

- `index.html` et `media/essai.mp4`.
- `RAPPORT.md` : concept en quelques lignes, heure de début et de fin, nombre de rendus et de retouches, ce que tu as vérifié (et comment) et ce que tu n'as pas pu vérifier.
- Regarde ton propre rendu avant de conclure : extrais une douzaine d'images avec ffmpeg et examine-les ; corrige ce qui ne va pas.

## Contraintes absolues

- Aucune coupe, aucun fondu enchaîné déguisé en morphing, aucune apparition arbitraire.
- Fidèle au comportement réel de `modales.html` : n'invente aucun comportement.
- Ne travaille que dans ce dossier.

Fais en sorte que chaque transformation paraisse à la fois surprenante et inévitable.
