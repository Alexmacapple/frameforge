# FF-11 — Deux rushes hétérogènes sans navigateur

Date : 23 novembre 2026. MacBook Pro, macOS 26.5.2. HyperFrames 0.8.33, FFmpeg 9.0.1.

## Objectif et sources

Tester l'assemblage de deux vidéos sans navigateur et sans nouvel éditeur. **Sources synthétiques** créées localement par les filtres FFmpeg : ce ne sont pas de véritables prises de vues.

- Rush A : mire animée testsrc2, 640 × 360, 24 images/s, 4,5 s, muet. SHA-256 : 92ab13c536eb6004cb0f34ec735134ba0abac4ef9ca52bcd1a595d16b2b68fad.
- Rush B : mire SMPTE, 854 × 480, 30 images/s, 4,508 s, avec son synthétique 440 Hz. SHA-256 : 7ee9764740d9520758440c3f70eaa8fe5cd90545ce994883f9e4bd64dd03f456.

Les sources ont été générées par FFmpeg : filtre testsrc2 pour A, filtres smptebars et sine pour B. Elles ne contiennent ni rushes personnels ni médias tiers.

## Composition et livraison

- Deux vidéos natives HyperFrames, de 0 à 4,5 s et de 4,5 à 9 s.
- Transition noire de 0,2 s autour de la coupe, **pas un fondu enchaîné**.
- Deux légendes incrustées ; fichiers captions.srt, captions.vtt, transcript.txt et provenance dans ce rapport.
- **Pas de narration vocale** : la transcription est celle des légendes, pas de paroles réellement prononcées. Le son du rush B est une tonalité de contrôle.
- Pour reproduire, copier les deux rushes de media/ à côté de index.html et lancer : npx --yes hyperframes@0.8.33 render -o media/ff11-native-two-rushes.mp4.

## Résultats

| Vérification | Résultat |
| --- | --- |
| Deux vidéos aux résolutions et cadences différentes, sans navigateur | PASS |
| Coupe et transition noire visibles sur images à 4,45 et 4,55 s | PASS sur échantillons |
| MP4 H.264/AAC, 1280 × 720, 9 s, 270 images décodées | PASS |
| Audio du rush B conservé | PASS technique : 0–3 s -91 dB, 5–8 s -21,1 dB (max -18 dB) |
| SRT, VTT, transcription des légendes | PASS fichiers ; pas de voix à transcrire |
| Provenance des deux sources | PASS documentaire, SHA-256 et génération locale |
| Compréhension humaine et accessibilité | UNVERIFIED |
| Sélection de vraies prises utiles, VFR, rotation, parole, droits tiers | NOT TESTED |

SHA-256 du MP4 : f0d10e92c2a2f4146cf6113baf25fdf5ef31d55a7b121e6b9400a69ccf125563.

## Décision

**REUSE_EXISTING pour ce cas, EXPERIMENT pour la généralisation.** HyperFrames suffit à assembler ces deux rushes et à conserver le son témoin, sans adaptateur ni éditeur maison. **FF-11 reste ouvert** : il faut encore tester des rushes réels autorisés, une sélection de passages pertinents et une voix réellement transcrite. Ne pas confondre une mire synthétique et une preuve de montage éditorial. Aucune validation de diffusion.
