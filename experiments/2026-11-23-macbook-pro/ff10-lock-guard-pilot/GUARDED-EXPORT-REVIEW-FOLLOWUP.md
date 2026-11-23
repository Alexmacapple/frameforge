# FF-10 — Correctifs après contre-revue

Date : 23 novembre 2026. SHA initial examiné : ef9e3f6fd4c08baa52424c97830add7237a87576.

## Correctifs réalisés

- Entrées figées : copie locale de la vidéo, de la référence SRT et du SRT candidat dans un répertoire temporaire, avec contrôle SHA-256. FFmpeg lit ces copies.
- Validation du MP4 : extraction de la piste SRT depuis le MP4, comparaison des deux blocs avec le candidat, puis décodage FFmpeg complet avant publication.
- Sortie non écrasable : création exclusive par lien physique dans le même système de fichiers (os.link) ; fichiers temporaires nettoyés.
- Tests supplémentaires : refus d'une sortie déjà existante et d'un SRT malformé.

## Preuves d'exécution

- 7 tests unitaires : PASS.
- Export autorisé depuis FF-12 local : PASS, SHA-256 73c84ea720beabb588a4ac1e421871847eb55fa8d9ec6875b63e252595693597.
- Modification interdite du second sous-titre : BLOCKED avant export ; aucun fichier adversarial produit.
- L'export autorisé a la même empreinte que l'essai précédent.

## Limites explicites

- Non-contournement global : NOT DEMONSTRATED. Les autres scripts peuvent appeler directement FFmpeg ou HyperFrames.
- Mutation concurrente : PARTIAL. Les copies isolent le rendu d'une mutation ultérieure, mais une modification coordonnée pendant la copie ou le remplacement de la référence par un acteur autorisé ne sont pas exclus.
- Approbation humaine : PARTIAL. Le second sous-titre est un témoin évalué positivement, sans signature ou approbation immuable.
- Reprise après interruption sur ce nouveau point d'entrée : NOT TESTED.
- Tests d'intégration automatisés complets : NOT DEMONSTRATED. Les sept tests sont unitaires ; les deux scénarios CLI ont été exécutés manuellement.
- Portabilité : os.link nécessite le même système de fichiers ; le répertoire temporaire est placé dans le dossier de sortie.
- Diffusion : droits NASA non vérifiés ; aucun média publié.

## Décision

REUSE_EXISTING + BUILD_MINIMAL limité au prototype FF-10. Ne pas déclarer le verrou obligatoire pour toute l'usine vidéo et ne pas fermer FF-10. La prochaine décision porte sur la définition d'un chemin de production officiel, pas sur un nouveau moteur ou orchestrateur.
