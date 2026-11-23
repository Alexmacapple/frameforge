# FrameForge — V5 Kokoro : remplacement de la voix, images conservées

**Date :** 23 novembre 2026  
**État :** expérimentation vocale, **NO-GO diffusion**.  
**Témoin :** `../vertical-v4-results-narration/media/prototype-v4.mp4` (Thomas, 16,1667 s).

## Hypothèse

Le modèle neuronal local Kokoro, voix française `ff_siwis`, peut remplacer Thomas sans refaire la capture ni perdre les trois résultats visuels. L'utilisateur avait jugé Kokoro « pas mal. Perfectible mais mieux » sur un échantillon continu. **Cela ne constitue pas une validation humaine de cette V5 montée.**

## Construction

- Réutilisation du **même média de capture ralenti** que V4, copié dans `media/capture.webm` ; même recadrage 180 %, même texte de narration et même composition HyperFrames 0.8.33.
- Trois phrases synthétisées **séparément** par Kokoro 0.9.x, modèle `hexgrad/Kokoro-82M`, voix `ff_siwis`, vitesse 1.0, phonétisation française eSpeak NG 1.52.0, calcul local sur MacBook Pro. Le modèle et la voix ont été obtenus via Hugging Face ; pas de service de synthèse payant.
- Départs de segments inchangés : **2,55 / 6,65 / 11,20 s**. Durées mesurées : **2,700 / 3,750 / 4,375 s** ; tous les segments se terminent avant le suivant et avant la fin de la vidéo.
- `captions.srt`, `captions.vtt`, `transcript.txt` et les sous-titres incrustés sont issus des mêmes textes et des durées Kokoro. Les pistes voix sont conservées séparément.
- Pour reproduire le rendu, placer `media/capture.webm` et `media/voice{1,2,3}.m4a` à la racine de ce dossier, puis exécuter `npx --yes hyperframes@0.8.33 render -o media/prototype-v5.mp4`. Le modèle vocal n'est pas nécessaire pour relire ou réassembler ces médias déjà générés.

## Recette exécutée

- **PASS technique** : rendu HyperFrames terminé ; décodage FFmpeg intégral ; MP4 H.264 + AAC stéréo, **16,166667 s, 485 images**.
- SHA-256 du MP4 : `779cadcd5e53be7cd85bca7a38b526a0b0653f312cb236599cf46c80b2526cc3`.
- **PASS sur échantillons** : `contact-sheet-v5.png` (16 images, 1 image/s) examinée ; tâche 1 visible à 2 s, deux tâches à 6 s, première tâche cochée/barrée à 11 s ; les sous-titres sont affichés pendant les états correspondants.
- **PASS structurel** : les segments de voix et sous-titres ne se chevauchent pas selon leurs durées déclarées ; les fichiers SRT/VTT/transcription existent.
- **UNVERIFIED** : fidélité de l'audio réellement prononcé aux textes, naturel et prononciation dans le film monté, absence d'artefact entre les échantillons, perception du rythme, accessibilité dans le lecteur cible, droits et confidentialité exhaustifs.
- La capture reste une source instrumentée, **ralentie** et **recadrée**, pas une nouvelle prise propre. Le film reste plus court que la cible initiale d'environ 30 s.

## Décision

**Kokoro est un candidat pour V5, pas un moteur adopté définitivement.** Comparer à l'écoute la V4 et la V5 entières, vérifier sans image les trois résultats, puis contrôler avec image les timings et sous-titres. Consigner la décision humaine avant toute autre modification. **FF-06/FF-08 restent ouverts ; aucune diffusion autorisée.**
