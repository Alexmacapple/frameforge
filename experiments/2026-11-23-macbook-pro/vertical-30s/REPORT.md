# Prototype vertical de 30 secondes — essai, non validation du MVP

23 novembre 2026, MacBook Pro Apple M2 Max. Source : TodoMVC React public, données fictives. Versions : agent-browser 0.31.1, HyperFrames 0.8.33, FFmpeg 9.0.1, macOS 26.5.2.

## Ce qui a été exécuté

1. Enregistrement navigateur avec agent-browser, ajout de « Première tâche », ajout de « Deuxième tâche », puis coche de la première. Assertions DOM exécutées après chaque geste : 1 tâche, puis 2 tâches, puis la première terminée.
2. Capture WebM VP8 de 19,2 secondes. Trois repères d'horloge UTC consignés pendant le parcours, mais **pas** de preuve d'alignement frame-accurate.
3. Synthèse française locale avec `say -v Thomas -r 155` de trois phrases : durées 1,820272 s, 2,366032 s et 2,505079 s. Conversion AAC.
4. Composition HyperFrames de 30 s : capture réelle de 0 à 19,2 s ; image finale figée et signalée de 19,2 à 30 s ; trois segments de voix et légendes positionnés aux secondes 2, 9 et 16. Les timings sont **des hypothèses éditoriales**, pas des repères extraits automatiquement du navigateur.
5. Rendu MP4 H.264 1920×1080 et AAC, 30,000 s, 765699 octets, décodage intégral FFmpeg réussi. SHA-256 du MP4 : `bcc46e76d12d7e31de2025a285c104091d8509f700532f395f0b5e99931de4a7`. Temps de rendu annoncé par HyperFrames : 37,7 s.

## Livrables

- `media/prototype-30s.mp4` : vidéo expérimentale, non approuvée
- `media/three-gestures.webm` : capture originale de ce scénario
- `media/voice1.m4a`, `voice2.m4a`, `voice3.m4a` : segments vocaux
- `media/final.png` : image finale
- `index.html`, `hyperframes.json`, `package.json` : composition
- `captions.srt`, `captions.vtt`, `transcript.txt` : alternatives textuelles

## Limites et décision

- **PASS technique** : capture des trois gestes avec assertions DOM, MP4 de 30 s avec audio, décodage intégral, fichiers SRT/VTT/transcription présents.
- **UNVERIFIED** : synchronisation réelle des gestes et de la voix, qualité de l'écoute, fidélité de chaque image, lisibilité de toutes les légendes, confidentialité image par image, accessibilité éditoriale et reproductibilité sur une deuxième exécution.
- **NON CONFORME au résultat éditorial visé** : 10,8 s d'image finale fixe, ce qui montre que la durée cible ne doit pas être obtenue artificiellement par remplissage. Le MP4 n'est pas une démonstration finalisée ni autorisée à diffuser.
- Aucun moteur ou adaptateur FrameForge n'a été développé ; la chaîne a été réalisée avec les outils existants.
- **Prochaine expérience discriminante** : établir des repères de gestes depuis les médias/événements, construire le montage à partir des durées mesurées et vérifier indépendamment le résultat ; comparer à une solution manuelle et mesurer le temps humain.
