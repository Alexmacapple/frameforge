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
