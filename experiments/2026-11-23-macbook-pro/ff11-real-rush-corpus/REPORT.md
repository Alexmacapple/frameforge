# FF-11 — Corpus de trois rushes réels : étude et montage local

Date : 23 novembre 2026. Statut : expérience locale PARTIAL ; aucun média tiers publié dans Git. FF-11 reste ouvert.

## Objectif

Éprouver FrameForge sur des vidéos préexistantes, sans navigateur, en choisissant deux sources pertinentes parmi trois, dont une avec parole humaine, puis en livrant MP4, sous-titres, transcription de travail, provenance et recette.

## Corpus et provenance

Sources téléchargées depuis la NASA Image and Video Library (API officielle). Métadonnées, liens exacts et SHA-256 dans provenance.json. Les originaux (46 Mo) sont conservés uniquement en local dans sources/. Les extraits de travail sont dans clips/.

1. RETENU : Earth Views from the International Space Station, extrait 45–51 s, 6 s, images de la Terre depuis l'espace. Audio supprimé volontairement : la source contient notamment un texte attribuable à un tiers ; sa réutilisation audio n'est pas autorisée par la seule présence dans la bibliothèque NASA.
2. RETENU : NISAR: Tracking Earth’s Changes From Space (Mission Overview), extrait 60–67 s, 7 s. Images d'observation puis entretien avec une scientifique ; parole humaine originale conservée.
3. ÉCARTÉ : Perseverance Rover’s Descent and Touchdown on Mars, extrait 60–65 s, 5 s. Sujet Mars, hors du brief « observation de la Terre ». L'exclusion est une décision éditoriale explicite, pas une incapacité technique.

Droits : les contenus NASA sont généralement réutilisables sous conditions, mais il existe des droits tiers, des règles de crédit et de non-approbation. Aucune vérification juridique source par source exhaustive n'a été faite. Voir https://www.nasa.gov/nasa-brand-center/images-and-media/ . Le présent corpus n'est pas autorisé à la diffusion ; le rapport et les métadonnées peuvent être conservés sans redistribuer les médias.

## Montage exécuté

- Découpage local avec FFmpeg, normalisation en VP9 640 × 360 à 30 i/s, sans altérer les originaux.
- HyperFrames 0.8.33 : 2 plans de 6 et 7 secondes, MP4 13 s, 390 images, H.264/AAC, décodage intégral FFmpeg PASS.
- Les deux sources sont des vidéos préexistantes, à la différence du premier pilote de mires synthétiques.
- Premier plan muet ; deuxième plan avec audio source conservé. Niveaux mesurés : 0–3 s ≈ -91 dB (silence), 7–10 s ≈ -23 dB moyen, -5,8 dB maximum.
- Les légendes incrustées sont des descriptions visuelles, pas des sous-titres de la parole humaine.
- ASR local avec faster-whisper modèle tiny.en sur le deuxième rush. Résultat dans asr-draft.json, sous-titres captions-speech-ASR-UNVERIFIED.srt. Transcription non corrigée humainement, et la piste SRT n'a pas encore été chargée dans le lecteur cible. Un premier essai ASR sur fichier a échoué en raison d'une incompatibilité de PyAV ; un passage par PCM décodé avec FFmpeg a permis la transcription. Aucun moteur de production nouveau.
- captions.srt, captions.vtt : légendes descriptives de la composition ; ne doivent pas être présentées comme sous-titres fidèles de l'audio.
- SHA-256 MP4 local : 6d7f1f3758cc9c48b2507e2a6c73a95b4a1ecc89b65b44fbad7787fc29a86204.

## Verdict et limites

| Garantie | Résultat |
| --- | --- |
| Trois sources réelles, deux retenues et une écartée avec raison | PASS documentaire |
| Découpage de plages et montage sans navigateur | PASS technique |
| Conservation de la parole humaine dans la deuxième source | PASS piste audio ; écoute indépendante UNVERIFIED |
| MP4 13 s décodable | PASS |
| Sous-titres et transcription exacts de la parole | UNVERIFIED : ASR brouillon, non relu |
| Concordance des descriptions avec les plans | PARTIAL : contrôle visuel ponctuel |
| Droits de diffusion de chaque source | UNVERIFIED |
| Accessibilité du film et du lecteur | UNVERIFIED |
| Montage entièrement automatisé depuis un brief | NOT TESTED : plages choisies manuellement |
| Généralisation à des rushes hétérogènes en orientation/cadence | NOT TESTED ici : extraits normalisés |

Décision : REUSE_EXISTING + EXPERIMENT. La composition native suffit à ces rushes, mais la recette éditoriale, la transcription exacte et les droits doivent être résolus avant de déclarer FF-11 terminé. Ne pas construire un nouvel éditeur, orchestrateur ou index de rushes sur la base de ce seul test.

Les médias et les fichiers de travail restent locaux. Les sources peuvent être retrouvées via les URLs et SHA-256 de provenance.json, sans inclure 46 Mo de contenus tiers dans Git.
