# FrameForge — essais locaux sur MacBook Pro (23 novembre 2026)

## Périmètre et limites

Essais réalisés sur macOS 26.5.2, Apple M2 Max, Node 24.22.1, FFmpeg/ffprobe 9.0.1, agent-browser 0.31.1 et HyperFrames 0.8.33. Application publique TodoMVC React avec données fictives, sans authentification. Tests sur le MacBook Pro, **pas** sur le Mac Studio. Les fichiers sources et les médias de ce dossier constituent des artefacts expérimentaux, pas une validation du MVP.

## Résultats observés

- **FF-01** : composition HTML simple de 5 s rendue par HyperFrames en MP4 H.264, 1920×1080, 30 images/s, 150 images. Décodage FFmpeg intégral réussi. Les premières et dernières images ont été extraites localement, sans validation éditoriale indépendante.
- **FF-02** : agent-browser a ajouté « FF02 first », ajouté « FF02 second » et coché le premier. Les états du DOM ont été interrogés après les gestes : deux éléments, premier `completed=true`. Vidéo native WebM VP8, 1280×634, 10 images/s, durée 3,6 s, décodage FFmpeg réussi. Les dates UTC relevées par le shell sont des repères approximatifs, **pas** des horodatages synchronisés image par image.
- **FF-03** : `hyperframes init --video` a importé le WebM muet, mais a également créé un élément `audio` pointant sur ce média sans piste audio. Le rendu a échoué avec « expected: audio ». Après retrait de cet élément dans le projet temporaire, MP4 de 3,6 s produit et décodé intégralement. Ce défaut n'est pas encore corrigé dans HyperFrames ni dans FrameForge.
- **Prototype narré** : synthèse française locale par `say -v Thomas -r 145`, durée mesurée 13,637914 s ; HyperFrames a rendu 15 s de MP4 H.264 + AAC, décodage intégral réussi. Il utilise les 3,6 s de capture puis une image fixe du résultat final. L'audio et l'image sont présents, mais l'alignement des trois gestes sur les phrases **n'a pas été vérifié**.

## Livrables

- `media/hyperframes-5s.mp4` : essai de rendu de base
- `media/three-actions.webm` : capture réelle
- `media/capture-integrated.mp4` : premier import vidéo réussi, muet
- `media/prototype-15s.mp4` : prototype narré, **non validé comme MVP**
- `media/narration.m4a`, `media/final.png`, `index.html`, `hyperframes.json`, `package.json` : sources du prototype
- `transcript.txt` : texte de narration
- `captions.srt` : **minutage éditorial approximatif, non synchronisé ni vérifié à l'écoute** ; non incrusté au MP4

## Reproduction indicative

Les médias d'entrée sont inclus. Dans ce dossier, utiliser HyperFrames 0.8.33 sur `index.html` après avoir placé les médias du sous-dossier `media/` à la racine du dossier de composition (ou ajusté les chemins). Le rendu a été effectué avec `npx --yes hyperframes@0.8.33 render -o prototype-15s.mp4`. L'exécution exacte peut nécessiter Chromium et des ressources réseau pour les polices et GSAP. La reproductibilité sur une seconde machine n'a pas été testée.

## Décision

**GO pour un test vertical plus complet**, mais pas de PASS pour le MVP 30 s. Prochaines preuves : capturer des gestes à une cadence lisible, obtenir les repères audio réels, synchroniser les événements, contrôler SRT/VTT, comparer avec une méthode directe et effectuer une revue de confidentialité et d'accessibilité. Aucun adaptateur général ni orchestrateur supplémentaire justifié.
