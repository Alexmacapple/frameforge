# SPEC — Architecture candidate, non validée

## Chaîne
Brief -> storyboard/provenance -> capture agent-browser -> médias et événements horodatés -> narration TTS -> synchronisation audio-first -> composition HyperFrames -> MP4/SRT/transcription -> QA -> validation humaine.

## Frontières
- `capture-adapter` : pilote le navigateur et retourne des médias, événements et observations. Ne présume pas qu'un journal d'actions suffit à reconstruire une vidéo.
- `narration-adapter` : voix locale, lexique, cache, segments et durées mesurées.
- `timeline-adapter` : transforme repères de voix et événements en éléments de composition ; gère pauses et débordements.
- `render-adapter` : utilise HyperFrames ; consigne version, commande, sorties et erreurs. FFmpeg en repli seulement après preuve d'équivalence fonctionnelle.
- `qa` : décodage, durée, audio, sous-titres, premières/dernières images, données sensibles et conformité au scénario ; distingue mesures automatiques et revue humaine.

## Contrat minimal d'une scène (conceptuel)
`scene_id`, `purpose`, `claims`, `source_refs`, `capture_refs`, `narration_text`, `audio_ref`, `cue_points`, `media_refs`, `expected_visual_result`, `verification_status`.

## Statuts de preuve
`observed`, `reasoned`, `planned`, `unverified`, `failed` ; horodatage, environnement et provenance associés.

## Dépendances et risques à vérifier
- API/version/licence d'HyperFrames et comportement du rendu CLI sur macOS.
- Capacités exactes d'enregistrement d'agent-browser et synchronisation des horodatages.
- Licences et compatibilité des éventuels composants tiers réutilisés ; privilégier une implémentation indépendante et minimale.
- Compatibilité TTS local, codecs et dépendances système.
- Absence de fuite de données dans captures, sous-titres, métadonnées et logs.

## ShipGuard
Utiliser `sg-pre-review` avant tout ajout, `sg-logic-audit` pour les invariants temporels et `sg-ship` pour les changements du code. La validation audiovisuelle reste propre à FrameForge.

## Précisions conceptuelles validées — D1 à D16
- **Manifeste minimal** : relier chaque scène et affirmation à des références de preuves originales, au geste, au résultat observé, à la version/source, à la date et au contexte de capture. Le manifeste n'est pas lui-même une preuve. Ne pas figer son format de sérialisation avant FF-04.
- **Statuts indépendants** : conserver `observed`, `reasoned`, `planned`, `unverified`, `failed` pour les éléments de preuve ; gérer séparément la validation de la scène, du film et l'autorisation humaine de diffusion. `observed` ne signifie pas `validated`.
- **Actualité** : vérifier la pertinence des captures historiques pour le contexte et la version visés, sans imposer une recapture automatique.
- **Reprise ciblée** : conserver les scènes réussies en brouillon après échec ; réexécuter les étapes invalides et revérifier les dépendances affectées. Ne pas figer d'architecture de cache ou de graphe avant FF-10.
- **Temps et montage** : respecter les durées observées des gestes et des phrases ; signaler les raccords qui raccourcissent une attente et montrer le résultat réel.
- **Repli** : documenter l'échec du chemin principal, la méthode de repli et ses différences ; vérifier les mêmes garanties de décodage, audio, sous-titres, temporalité et fidélité avant d'en conclure l'équivalence.
- **Livraison et approbation** : MP4, sous-titres, transcription, provenance et rapport de recette constituent le lot MVP ; validation des scènes puis du film, suivie d'une approbation humaine portant sur une version précise. Toute modification significative entraîne les revérifications affectées et une réapprobation.

Ces règles sont fonctionnelles, pas des implémentations démontrées. Aucun nouvel orchestrateur ni ADR n'est retenu à ce stade. Voir [GLOSSARY.md](GLOSSARY.md).
