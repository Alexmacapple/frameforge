# Insert animé dans un film gardé (ticket 59)

25 novembre 2026, MacBook Pro, `main` à `b3c527e`. Essai d'un schéma animé du focus dans une fenêtre modale, écrit par Claude en composition HyperFrames, sans le plugin `/hyperframes`.

## Verdict

- **Reproductibilité : PASS.** Trois rendus des mêmes entrées donnent le même fichier, octet pour octet (`0460013a…a236`), avec les mêmes empreintes de flux vidéo et de paquets que mesure le garde. Le critère d'arrêt du ticket n'est pas déclenché.
- **Apport pour le spectateur : oui.** Alex, le 25 novembre 2026, après visionnage de `media/rendu-2.mp4` : le schéma aide à comprendre le piège du focus mieux que le film 47 seul. Jugement d'une seule personne, qui connaît déjà le sujet : ce n'est pas l'écoute d'un spectateur qui découvre le film (#35).
- **Intégration au film 47 : non faite.** La fiche n'a pas de place pour un insert ; l'insert est rendu seul, avec les options du garde. L'intégrer demande une évolution de la fiche, à décider si l'apport est confirmé.

## Ce qui a été fait

- Trois phrases, une par étape, synthétisées avec les réglages du film 47 (voix `ff_siwis`, vitesse 1,2, graine 20261123) : 2,875 s, 3,525 s, 3,625 s. Empreintes dans `narration-synthesis.json` ; les clips ne sont pas versionnés.
- `build_insert.py` écrit la composition, les sous-titres et la transcription. Sous-titres découpés par la règle de la fiche en version 3 (#60), cartouche de la chaîne.
- Animation sans GSAP : la documentation de HyperFrames charge GSAP depuis un CDN, ce qui ferait dépendre le rendu du réseau. Le moteur pilote tout objet de `window.__timelines` qui sait se positionner (`seek`, `totalTime`, `duration`) ; l'état de chaque élément est ici une fonction pure du temps.
- `render_insert.py` rend sur une copie isolée des entrées, avec les options du garde (HyperFrames 0.8.33, `--workers=2`, `--no-best-effort`, télémétrie coupée), sans écraser un rendu.
- Plugin `/hyperframes` non installé : rien de nouveau installé, ses deux préalables (version, télémétrie) sont sans objet.

## Mesures

- Durée de l'insert : **12,0 s**, au-delà des 5 à 8 s visées ; c'est la voix qui l'impose (trois phrases, 10 s de parole).
- Fabrication : environ **4 minutes** de la synthèse de la voix au rendu reproductible (16:44 à 16:48), lecture préalable de la documentation de HyperFrames non comptée.
- Rendu : 11 à 13 s par passage.
- Retouches : **une**. La planche du premier rendu a montré le cadre du focus loin des boutons : positions lues par rapport au parent (`offsetLeft`) au lieu de l'image entière. Corrigé par `getBoundingClientRect` ; la boucle à deux lobes est devenue une ellipse autour des deux boutons.

## Limites

- Le mouvement a été vérifié sur des planches de 16 images, pas image par image.
- L'insert n'a pas été écouté sans l'image (#35) ni comparé à ses sous-titres (#36).
- Reproductibilité mesurée sur ce Mac seulement, trois rendus le même jour.

## Fichiers

- Versionnés : `phrases.json`, `synthesize_kokoro.py`, `narration-synthesis.json`, `build_insert.py`, `index.html`, `captions.srt`, `transcript.txt`, `hyperframes.json`, `render_insert.py`.
- En local, non versionnés : `voice1.wav` à `voice3.wav`, `media/rendu-1.mp4` (avant retouche), `media/rendu-2.mp4` à `media/rendu-4.mp4` (identiques), leurs planches.
