# FrameForge — V5, narration Kokoro Siwis

**Date :** 23 novembre 2026. **Statut :** prototype technique, pas de validation de diffusion.

## Objectif

Reprendre la V4 avec la voix féminine française **Kokoro `ff_siwis`**, acceptée provisoirement à l'écoute d'un échantillon, sans modifier la capture source ni ajouter un moteur à l'architecture FrameForge.

## Chaîne exécutée

- Source vidéo : `../vertical-v4-results-narration/media/capture.webm` (capture V3 instrumentée, ralentie 1,7× dans V4 ; recadrage 180 % conservé). **Aucune nouvelle capture propre.**
- Synthèse **locale** de trois segments par `hexgrad/Kokoro-82M`, `KPipeline(lang_code='f')`, voix `ff_siwis`, vitesse `1.0`, dans le venv temporaire du pilote. Poids téléchargés antérieurement depuis Hugging Face ; aucune API TTS distante sollicitée pour générer le texte.
- Trois segments : `2,700`, `3,750` et `4,375` secondes ; départs `2,550`, `6,650`, `11,200` secondes. Les sous-titres incrustés et fichiers SRT/VTT sont dérivés des mêmes textes et repères.
- HyperFrames **0.8.33** rend le film. Pour reproduire, copier `media/capture.webm` et `media/voice{1,2,3}.m4a` dans le répertoire contenant `index.html`, puis exécuter `npx --yes hyperframes@0.8.33 render -o media/prototype-v5.mp4`. Les liens symboliques utilisés localement pour le rendu ne sont pas versionnés.
- `timings.json` conserve les repères et durées ; `captions.srt`, `captions.vtt` et `transcript.txt` constituent les alternatives textuelles.

## Contrôles exécutés

- **PASS technique :** MP4 H.264 et AAC, durée **16,433333 s**, **493 images** ; rendu HyperFrames terminé et décodage intégral FFmpeg réussi.
- SHA-256 : `99792213f5706e7764bb970e776de875eb65f35a6d10528f91ff7a9018caebd1`.
- Planche `contact-sheet-v5.png` : **16 images à 1 image/s** examinées ; tâche 1 visible à 2 s, tâche 2 à 6 s, tâche 1 cochée et barrée à 11 s. Les sous-titres des trois résultats sont visibles sur les images correspondantes. Les instants sont des **échantillons**, pas des horodatages précis des gestes.
- Les trois phrases restent celles de V4 : résultat 1 visible, deux tâches visibles, première cochée/barrée et seconde encore à faire.
- Aucune grande bannière « SYNC » visible sur la planche ; la source conserve toutefois le marqueur hors cadre.

## Limites et décision

- **UNVERIFIED :** écoute de la **V5 exacte**, naturel de la voix dans le montage, intelligibilité sans image par un tiers, synchronisation perceptive, concordance parole réelle/SRT, lecture externe des sous-titres, tests VoiceOver, contrôle exhaustif de confidentialité et droits.
- La voix Siwis est **provisoire**, non figée comme dépendance du studio ; l'utilisateur pourra la remplacer sans recapturer les gestes.
- La vidéo est **16,4 s**, pas le livrable initial d'environ 30 s. La source est ralentie et le cadrage masque un artefact de capture ; ce n'est pas une prise finale propre.
- **FF-06 : PARTIAL** (repères audio et textes construits, synchronisation perçue non testée). **FF-08 : PARTIAL** (décodage et inspection d'échantillons PASS ; revue humaine finale NOT RUN). **NO-GO diffusion**.

**Suite :** ouvrir la V5 exacte dans un lecteur, l'écouter sans image puis l'examiner avec image, relever les résultats et les défauts. Ensuite seulement tester la reprise ciblée (#10) et deux rushes hors navigateur (#11).
