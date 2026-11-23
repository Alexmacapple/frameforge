# FF-11 — Deux sources vidéo sans navigateur, test de composition synthétique

**Date :** 23 novembre 2026. **Statut : PASS technique sur fixtures synthétiques ; FF-11 reste ouvert pour de vrais rushes.**

## Question

HyperFrames et FFmpeg peuvent-ils assembler deux fichiers vidéo autonomes sans navigateur, avec caractéristiques différentes et conservation du son, et produire un dossier de livraison comportant MP4, sous-titres, transcription descriptive, provenance et recette ?

## Protocole exécuté

- Deux **fixtures synthétiques distinctes**, produites localement par FFmpeg, sans caméra, sans navigateur et sans données personnelles :
  - A : mire animée **1280 × 720, 24 fps**, piste de test **440 Hz**, 4 s.
  - B : mire animée **720 × 1280, 30 fps**, piste de test **660 Hz**, 4 s.
- Sélection de **0 à 3,5 s** pour chaque fichier, puis coupe à **3,5 s** et composition de **7 s** via **HyperFrames 0.8.33**. Mise à l'échelle avec `object-fit:contain` pour éviter de rogner le plan portrait.
- Audio des deux fichiers explicitement placé sur la timeline comme éléments audio, avec volume 0,3. Ce ne sont pas des dialogues, et **aucune narration n'a été créée**.
- Titre visuel différent pour chaque plan. Les fichiers `captions.srt`, `captions.vtt` et `transcript.txt` décrivent les sons et plans ; ce sont des alternatives textuelles **descriptives**, pas une transcription de paroles inexistantes.
- `provenance.json` référence les sources, durées, fréquences, plages sélectionnées et SHA-256. **Aucune sélection éditoriale de prises réelles n'a été testée.**

## Preuves

- Rendu HyperFrames **PASS**, MP4 **7,000 s**, **1920 × 1080**, H.264 + AAC, **210 images**, décodage intégral FFmpeg réussi.
- SHA-256 rendu : `ab33b7712b97976db9fbbdf68e02ba1ad608e4b97ed3ce5bb192f3c8583c321c`.
- Inspection des images extraites à **1,5 s** et **5 s** : captures `frame-a.png` et `frame-b.png` ; revue visuelle à confirmer.
- Contrôle spectral simple sur une fenêtre de 0,5 s à **0,8 s** et **4,2 s** : première fenêtre dominée par **440 Hz** (énergie corrélée 611,62 contre 0,03 à 660 Hz), seconde dominée par **660 Hz** (615,96 contre 0,02 à 440 Hz). RMS normalisé ≈ **0,0264 / 0,0266**. **PASS :** les deux sons sont effectivement présents dans le rendu aux plages attendues.
- Les sources sont artificielles : elles ne démontrent ni gestion de rushes humains réels, ni compréhension et sélection de prises, ni normalisation audio avancée.

## Décision

**REUSE_EXISTING.** Aucun navigateur, moteur temporel, nouvel éditeur ou orchestrateur n'a été nécessaire pour le cas synthétique testé. Les outils actuels ont assemblé deux formats et deux cadences différents et préservé leurs sons.

**FF-11 non clos.** La vraie expérience suivante doit utiliser **deux rushes autorisés réels**, idéalement l'un vertical et l'autre horizontal, comportant des contenus utiles à sélectionner et un son à conserver. Tester le choix des passages, les droits, le rendu, les sous-titres et la compréhension humaine. Si cet essai échoue, localiser d'abord la limite précise dans HyperFrames ou FFmpeg.

**Aucune autorisation de diffusion publique n'est déduite de ce test.**

### Reproduction

Recréer les deux fixtures avec les commandes FFmpeg correspondant aux sources indiquées dans `provenance.json`, puis placer les fichiers `media/rush-a-landscape-with-audio.mp4` et `media/rush-b-portrait-with-audio.mp4` à la racine de la composition, ou créer des liens symboliques locaux, et exécuter `npx --yes hyperframes@0.8.33 render -o media/ff11-composition.mp4`.
