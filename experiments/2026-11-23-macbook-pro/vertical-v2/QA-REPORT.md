# FrameForge — FF-06 / FF-08, prototype V2

Date : 23 novembre 2026. Machine : MacBook Pro Apple M2 Max. Essai documentaire et technique, **pas une validation éditoriale humaine**.

## Modifications par rapport à la V1

- Vidéo ramenée de 30,0 à **19,2 secondes** : suppression des 10,8 secondes d'image fixe de remplissage.
- Trois phrases locales `say` conservées, placées à 1,0 s, 6,8 s et 12,6 s. Durées mesurées des segments : 1,820272 s, 2,366032 s et 2,505079 s.
- Les changements visuels les plus importants de la capture source ont été repérés par différence de pixels entre images échantillonnées à 5 Hz : environ **1,6 s**, **7,4 s**, **13,2 s**. Ce sont des **estimations visuelles**, pas des événements instrumentés du navigateur.
- SRT et VTT recalés sur les débuts et durées nominales des trois segments. Leur concordance perceptive n'a pas été évaluée.

## Contrôles exécutés

| Contrôle | Résultat | Limite |
| --- | --- | --- |
| MP4 H.264, 1920×1080, 30 images/s | PASS | Métadonnées ffprobe |
| Durée totale 19,2 s | PASS | ffprobe |
| Décodage intégral FFmpeg | PASS | Aucun message d'erreur |
| Piste AAC | PASS | Présence, pas qualité perçue |
| Niveaux audio | Mesurés | Volume moyen -20,0 dB, maximum -1,0 dB ; aucun seuil métier approuvé |
| Détection des silences | Mesurée | Par `silencedetect` à -36 dB, pauses normales possibles |
| Échantillons de huit images | Extraits | Pas de revue visuelle indépendante de leur lisibilité |
| Sous-titres SRT et VTT | Présents | Minutage éditorial, non validé à l'écoute |
| Trois gestes et résultats DOM | Preuve V1 conservée | Pas de nouvelle capture instrumentée pour la V2 |

## Contrôles restant ouverts

- **FF-06 UNVERIFIED** : alignement exact des événements navigateur avec la vidéo, lisibilité de chaque geste, précision des sous-titres et synchronisation perceptive.
- **FF-08 UNVERIFIED** : revue indépendante de la fidélité, de la compréhension, des informations visuelles essentielles, de la confidentialité image par image et de l'accessibilité au lecteur d'écran.
- Aucun test de répétabilité sur une seconde prise ; aucun gain de temps démontré face à une réalisation directe.
- Aucun seuil de volume ou de tolérance temporelle imposé sans validation.

## Décision

**REUSE_EXISTING** pour le prototype : HyperFrames, agent-browser et FFmpeg ont suffi ; pas de besoin démontré pour un nouveau skill ou un moteur propre. **GO expérimentation**, mais **NO-GO validation MVP et diffusion** tant que les contrôles ouverts ne sont pas exécutés.

## Reproduction

Sources et voix du prototype V1 : `../vertical-30s/media/`. Copier la capture `three-gestures.webm` vers `three-gestures-30s.webm` et les trois voix `voice1.m4a`, `voice2.m4a`, `voice3.m4a` à côté de `index.html`. Rendre avec `npx --yes hyperframes@0.8.33 render -o prototype-v2.mp4`. Cette reproduction n'a pas été relancée depuis le dossier Git.
