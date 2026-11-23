# FrameForge — V2 : montage sans remplissage, synchronisation approximative

Date : 23 novembre 2026. Exécution sur MacBook Pro M2 Max, macOS 26.5.2. HyperFrames 0.8.33, agent-browser 0.31.1, FFmpeg 9.0.1. Vidéo expérimentale, **non validée pour diffusion**.

## Protocole

La capture originale de 19,2 s est réutilisée, sans nouvel acte sur le site. Les différences entre images extraites à 5 images/s et réduites à 640 px ont été mesurées par Pillow (moyenne absolue des différences RGB sur toute l'image). Les trois changements visuels dominants sont à environ 1,6 s, 7,4 s et 13,2 s. Ces repères ont une granularité de 0,2 s et sont des **indices de changement d'image**, pas des horodatages d'action émis par le navigateur ; l'identification de leur cause repose sur le scénario déjà vérifié par assertions DOM.

Les trois segments de voix française locale déjà générés ont été positionnés à 1,0 s, 6,8 s et 12,6 s, soit environ 0,6 s avant les trois changements visuels détectés. Durées audio mesurées : 1,820272 s, 2,366032 s et 2,505079 s. SRT et VTT ont été ajustés à ces débuts et durées ; leurs fins sont arrondies à la milliseconde.

## Résultats techniques

- MP4 H.264 + AAC, 1920×1080, 19,200 s, 615658 octets, SHA-256 `dbed2dea1570e814f4fc60c9ce9bd5ee29b302d48d5fd9352e46c968c8121c44`.
- HyperFrames annonce 20,5 s de rendu ; décodage intégral FFmpeg : PASS.
- Analyse `silencedetect=noise=-36dB:d=0.25` : voix détectée approximativement de 1,000 à 2,716 s, 6,800 à 9,053 s, 12,600 à 14,993 s. L'analyse du silence ne prouve pas l'exactitude des mots prononcés.
- La vidéo dure exactement autant que la capture source ; **aucune image finale ajoutée**.
- Trois phrases et alternatives SRT/VTT/transcription fournies.

## Écarts V1 → V2

| Point | V1 | V2 |
|---|---|---|
| Durée | 30 s | 19,2 s |
| Capture réelle | 19,2 s | 19,2 s |
| Image fixe de remplissage | 10,8 s | 0 s |
| Début des voix | 2 / 9 / 16 s | 1 / 6,8 / 12,6 s |
| Repères de gestes | Hypothèses éditoriales | Détection de différences d'images, approximative |
| Synchronisation événementielle exacte | Non démontrée | Non démontrée |
| Revue humaine indépendante | Non faite | Non faite |

## Statuts

- **PASS** : rendu, décodage, présence audio, suppression du remplissage, génération des alternatives.
- **UNVERIFIED** : identification indépendante des changements d'image, synchronisation action/parole exacte, qualité de la voix française à l'écoute, exactitude de la parole par rapport au texte, lisibilité et accessibilité du film, contrôle complet de confidentialité.
- **À corriger avant validation** : contrôle de chaque geste sur les images, repères d'événements émis pendant la capture, revue éditoriale indépendante et comparaison avec une réalisation directe ou manuelle de même périmètre.

## Décision

`REUSE_EXISTING` pour la composition. Les outils directs produisent le film sans adaptateur FrameForge. La valeur potentielle d'une couche FrameForge est la **preuve synchronisée, le contrôle qualité et la reproductibilité**, pas un moteur vidéo. Ne pas déclarer FF-06/FF-08 terminées.
