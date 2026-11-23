# FF-10 — Suivi de la seconde contre-revue

23 novembre 2026. Base d'examen d'AlexDot : bb6f840. Correction ciblée après son verdict FAIL production. Protocole figé avant correctif : FRAMERATE-PROTOCOL.md (2ed9522).

## Correction

Le validateur V5 contrôle maintenant la cadence moyenne vidéo fournie par ffprobe : 30 images/s avec une tolérance de 0,01 image/s. Une cadence absente, invalide ou différente est refusée avant de vérifier le nombre d'images et l'audio. Ce contrôle complète les vérifications de durée, dimensions, codecs, nombre d'images, piste AAC, empreinte PCM et décodage intégral.

## Preuves nouvelles

- 17/17 tests web PASS, dont rejet d'une vidéo 24 images/s.
- Un rendu V5 réel via npm run render après modification : PASS, 28,55 s sur MacBook Pro.
- Empreinte du nouveau MP4 local : 9fbb7c316fb20ef94a0424f231881b5f0f24d86daf32418aadc1a92e94ae11ad, identique au témoin précédent.

## Limites et décision

Le validateur vérifie une cadence moyenne déclarée par ffprobe ; il ne garantit pas une cadence constante sur chaque intervalle. Il ne prouve pas la présence perceptible des trois gestes, ni la qualité de l'audio, ni l'autorité de la référence. Le nouveau rendu a été exécuté sur Mac et non dans l'environnement Linux où une dépendance bloquait l'installation. Aucune nouvelle contre-revue indépendante du correctif de cadence n'a été exécutée.

**Verdict : PASS ciblé sur la cadence ; FF-10 reste FAIL pour promotion en production, recette humaine V5 UNVERIFIED.** Aucun média publié.
