# FF-10 — Contre-exemples du point d'entrée web et correction ciblée

23 novembre 2026. SHA initial 273d3b9. **Revue contradictoire interne, non indépendante.**

## Défaut découvert

Le précontrôle initial examinait la composition HTML mais pas les fichiers annexes. Un SRT pouvait être modifié tout en laissant l'HTML accepté. Reproduction exécutée : changement du texte de captions.srt et acceptation du précontrôle HTML inchangé. Cela crée un risque de divergence entre sous-titres incrustés et sous-titres livrés. Verdict initial : FAIL pour intégrité des assets annexes.

## Correction ciblée

Le point d'entrée expérimental V5 vérifie désormais les SHA-256 épinglés de captions.srt, captions.vtt, transcript.txt, capture.webm, des trois pistes de voix, de hyperframes.json et de package.json. L'empreinte du manifeste est également fixée dans le point d'entrée. Le wrapper V2 invoque un précontrôle incluant les assets **avant et après copie isolée**, pour rejeter une altération entre contrôle et snapshot.

Les tests adversariaux nouveaux couvrent le SRT modifié, la voix modifiée et le manifeste falsifié. Le rendu npm après la première correction a produit un MP4 décodable, identique bit à bit au précédent (SHA-256 9fbb7c316fb20ef94a0424f231881b5f0f24d86daf32418aadc1a92e94ae11ad). Le renforcement supplémentaire du contrôle du manifeste au niveau du snapshot a été vérifié par tests unitaires, sans troisième rendu complet.

## Résultats

- 13/13 tests web PASS après correction.
- 4/4 tests deux rushes et 5/5 tests de référence épinglée PASS dans la passe précédente.
- Aucune modification du projet V5 original.
- Aucun média diffusé.

## Limites

Le point d'entrée, le manifeste et ses empreintes peuvent être modifiés ensemble par un agent disposant de droits d'écriture : ce mécanisme **n'est pas une autorité d'approbation humaine indépendante**. Les appels directs à HyperFrames restent possibles. Le périmètre de ressources est explicitement limité à la V5. Aucune revue humaine du film ni vérification exhaustive des droits.

**Verdict : PASS ciblé pour l'intégrité des ressources déclarées sur le pilote, PARTIAL PASS pour FF-10 global.** Conserver FF-10 ouvert. Pour une véritable contre-revue indépendante, confier ce dossier à un évaluateur séparé, sans lui communiquer la conclusion avant ses propres tests.
