# FF-10 — Correctif après FAIL indépendant : contrôle du film final

23 novembre 2026. Contre-revue indépendante reçue sur la version 922536d. Verdict initial : FAIL pour la promotion en production. Protocole figé dans OUTPUT-QA-PROTOCOL.md, commit 2bc88c6.

## Défaut confirmé

Le wrapper ne vérifiait que le décodage intégral du MP4. Un moteur de test pouvait retourner un film valide de 0,5 seconde, 64×64 pixels, sans audio, et obtenir PASS. Il n'exigeait ni durée ni piste sonore. Le défaut est distinct de l'intégrité des entrées.

## Correction minimale

Le wrapper V2 accepte un validateur de sortie optionnel, appelé sur le MP4 temporaire **avant** son dépôt sous le nom final. Le pilote V5 fournit un validateur spécifique : durée 16,10–16,23 s ; vidéo H.264 1920×1080, au moins 480 images ; audio AAC d'au moins 16 s ; empreinte du PCM stéréo 48 kHz identique à la V5 témoin. Les autres expériences ne reçoivent pas automatiquement ce validateur : ne pas prétendre qu'elles sont protégées.

## Tests exécutés sur MacBook Pro

- 16/16 tests du point d'entrée web PASS.
- Un MP4 synthétique de 0,5 s sans audio est rejeté (output_duration_invalid).
- Un MP4 synthétique 1920×1080 de durée attendue mais sans audio est rejeté (output_audio_missing_or_short).
- Le MP4 V5 témoin est accepté.
- Un rendu réel complet via npm run render, avec validation avant dépôt, est PASS. Empreinte SHA-256 : 9fbb7c316fb20ef94a0424f231881b5f0f24d86daf32418aadc1a92e94ae11ad, identique au rendu antérieur.
- Le wrapper conserve le décodage FFmpeg intégral et le refus d'écrasement d'une sortie existante.

## Ce que ce PASS ne démontre pas

Les seuils sont propres à cette V5. Ils ne prouvent pas que les trois gestes et résultats sont effectivement visibles, que les sous-titres sont lisibles, ni que la voix est intelligible. Le test PCM protège l'identité de la narration par rapport au témoin, pas son adéquation éditoriale. La fixture locale et le MP4 historique ne sont pas encore reproductibles depuis un checkout neuf sans reconstruction. L'autorité d'approbation et les chemins de rendu directs ne sont pas verrouillés. Une nouvelle contre-revue indépendante du correctif n'a pas été exécutée.

**Verdict : PASS technique ciblé pour la lacune de contrôle final, FAIL/UNVERIFIED maintenu pour promotion générale. FF-10 reste ouvert.** Aucun média publié.
