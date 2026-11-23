# FrameForge V4 — narration des résultats observés

Date : 23 novembre 2026. **Prototype expérimental, non validé pour diffusion.**

## Hypothèse

Une narration qui explicite les résultats des trois gestes permet de comprendre le film sans vision, à confirmer par une écoute indépendante.

## Source et modifications

- Source : `../vertical-v3/media/capture.webm` (capture instrumentée ; le bandeau rouge SYNC reste hors du cadrage, il n'est pas supprimé de la source).
- Capture **ralentie uniformément d'un facteur 1,7** avec FFmpeg (`setpts=1.7*PTS,fps=30`), afin de laisser du temps à une narration plus explicite. **Les gestes ne sont pas rejoués en temps réel** et aucun nouveau geste n'a été capturé.
- Recadrage 180 % repris de la V3. Composition via **HyperFrames 0.8.33** ; voix française locale macOS `Thomas`, débit 205 mots/minute ; aucun nouveau moteur.
- Narration, sous-titres et transcription :
  1. « Une première tâche apparaît dans la liste. »
  2. « Une deuxième tâche apparaît. Les deux tâches sont visibles. »
  3. « La première tâche est cochée et barrée. La deuxième reste à faire. »
- Départs voix : 2,55 s / 6,65 s / 11,20 s. Durées mesurées : 1,892 s / 2,797 s / 3,389 s. Les trois annonces interviennent après l'apparition des résultats dans la vidéo ralentie, d'après les images échantillonnées.
- Le script de préparation a été exécuté localement ; les éléments de composition et médias sont versionnés dans ce dossier. Pour le rendu HyperFrames, les médias sont attendus à la racine de la composition ; sur le Mac d'essai, des liens symboliques locaux pointaient vers `media/`. Pour une réexécution, copier `media/capture.webm` et `media/voice{1,2,3}.m4a` à côté de `index.html` puis exécuter `npx --yes hyperframes@0.8.33 render -o media/prototype-v4.mp4`. Aucun nouveau système de packaging n'a été construit.

## Contrôles exécutés

- Premier rendu : **FAIL explicite**, les médias n'étaient pas à la racine et les identifiants étaient absents ; l'outil a détecté le problème. Corrigé avant le rendu retenu.
- Second rendu : **PASS technique**, MP4 H.264/AAC stéréo, **16,166667 s**, **485 images**, décodage intégral FFmpeg réussi.
- SHA-256 du MP4 : `63edcabe56703bf163f1d0f1dd76a1eee3fc994bffaf4a5f9ec700cb250e5e29`.
- Une planche `contact-sheet-v4.png` de **16 images (1 image/s)** a été examinée. Les trois états sont présents ; le bandeau SYNC n'est pas visible sur ces échantillons. Les phrases incrustées sont affichées au moment des états correspondants sur les échantillons.
- `captions.srt`, `captions.vtt` et `transcript.txt` produits à partir des mêmes textes et repères. Cela prouve leur **cohérence de génération**, pas leur fidélité à ce qui est effectivement prononcé.

## Limites et décision

- **UNVERIFIED** : intelligibilité et prononciation réelles, écoute indépendante sans image, compréhension par un tiers, contrôle VoiceOver, synchronisation perceptive mot à mot, confidentialité et droits de diffusion exhaustifs.
- **UNVERIFIED** : absence d'artefacts entre les 16 images échantillonnées ; le bandeau de calibration demeure dans la capture source hors cadre.
- La V4 est un **prototype de 16,2 s**, non le livrable initial d'environ 30 s. L'allongement par ralentissement n'est pas une preuve de montage éditorial définitif.
- La composition et les sous-titres incrustés ont été modifiés ensemble ; aucun test de reprise après interruption ni de préservation de correction humaine n'a été réalisé.
- **Verdict : PASS technique ; recette FF-06 et FF-08 PARTIAL / NO-GO diffusion.** Faire écouter et voir le film exact, sans puis avec image, avant de décider d'une nouvelle correction. Aucune nouvelle architecture justifiée.
