# FrameForge — V3 recadrée : correction du bandeau SYNC et de la lisibilité

Date : 23 novembre 2026. Source : `../vertical-v3/media/capture.webm`. HyperFrames 0.8.33, mêmes trois voix et sous-titres que la V3.

## Correction appliquée

Le montage d'origine laissait apparaître le bandeau rouge « SYNC » au début. Le nouvel `index.html` agrandit la capture (180 %) et la recentre sur l'interface TodoMVC. Cela masque le bandeau dans les images de contrôle et rend les tâches plus grandes, sans altérer les gestes de la capture source. **Ce n'est pas une prise native sans marqueur** : le bandeau est hors cadre, non supprimé du fichier source.

## Contrôles exécutés

- MP4 de **9,5 secondes**, H.264 + AAC, rendu HyperFrames terminé et décodage intégral FFmpeg **PASS**.
- Images extraites à **0,5, 1,6, 3,8, 6,5 et 9,2 s** ; planche `contact-sheet.png` examinée.
- Sur ces cinq images : **aucun bandeau SYNC visible** ; tâche 1 présente à 1,6 s, deux tâches à 3,8 s, première tâche cochée/barrée à 6,5 et 9,2 s.
- Cadrage plus serré : interface principale plus lisible ; certains éléments périphériques de la page sont volontairement hors cadre.
- Trois pistes vocales, mêmes timings et mêmes textes SRT/VTT/transcription que la V3. **Aucune nouvelle validation perceptive de la narration**.

## Limites

- Cinq images examinées, **pas une inspection exhaustive des 285 images**. Absence d'artefact sur tout le film non démontrée.
- La capture originale a été instrumentée et conserve son bandeau hors cadre.
- Exactitude de la parole à l'écoute, synchronisation perceptive, compréhension sans vision, confidentialité exhaustive et revue humaine indépendante **NOT RUN**.
- Aucun alignement temporel exact ni seuil ±250 ms démontré.

## Décision

**PASS technique et amélioration visuelle sur les échantillons**, **UNVERIFIED pour FF-06 et FF-08**. Le film n'est pas validé pour diffusion. Avant clôture : inspection de toutes les images, écoute et revue indépendante, puis éventuellement une prise propre native avec cadrage adapté.

Pour reproduire, placer `../vertical-v3/media/capture.webm` sous `capture.webm` et les voix de `../vertical-v2/media/` à côté de `index.html`, puis exécuter `npx --yes hyperframes@0.8.33 render -o reframed.mp4`.
