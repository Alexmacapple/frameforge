# FF-10 — Correction ciblée des deux contre-exemples HyperFrames

23 novembre 2026. Référence avant correction : commit 3709673. **Verdict : PASS limité aux scénarios rejoués ; protection produit générale NON DÉMONTRÉE.**

## Correction

Un nouveau point d'entrée expérimental guarded_hyperframes_v2.py réutilise le contrôle HTML du premier pilote, puis copie les fichiers nécessaires à la composition dans un répertoire temporaire propre à l'exécution. HyperFrames 0.8.33 rend cette copie, et non le projet source. Les empreintes des entrées sont contrôlées avant le rendu et après copie.

Le sous-processus HyperFrames est lancé dans un groupe de processus distinct. À réception de SIGTERM/SIGINT par le contrôleur, celui-ci envoie SIGTERM au groupe du rendu, attend sa fin, puis supprime le répertoire temporaire. En cas de non-réponse, un SIGKILL du groupe est prévu après délai. Le MP4 n'est publié dans un chemin neuf que si le rendu a réussi, a été décodé par FFmpeg et que les sources sont restées inchangées à la vérification finale. Publication par lien physique exclusif.

## Rejeu des contre-exemples

### Interruption

- Arrêt du contrôleur pendant le rendu (après huit secondes) : code de sortie 2, raison guarded render interrupted.
- Aucun MP4 final immédiatement ni après cinq secondes supplémentaires.
- Aucun répertoire temporaire de ce pilote restant après l'arrêt.
- Relance complète sur les mêmes entrées : PASS ; MP4 16,166667 s, 485 images, 759 paquets audio ; SHA-256 07e8dd7d237877a5c80d8210f6c69a2cb1ac1ceb56c139e7da93dae149e20324.
- Ce n'est pas une reprise à partir d'un checkpoint.

### Mutation transitoire

- Le texte du sous-titre HTML 2 du projet d'origine a été modifié après démarrage du rendu, puis rétabli cinq secondes plus tard.
- HyperFrames utilisait une copie isolée créée avant cette modification.
- Le contrôleur a produit un MP4 avec la même empreinte SHA-256 que le rendu témoin : 07e8dd7d237877a5c80d8210f6c69a2cb1ac1ceb56c139e7da93dae149e20324.
- Résultat structuré : V2-RACE-RESULTS.json.

## Garanties et limites

| Garantie | Verdict |
| --- | --- |
| Interruption SIGTERM supervisée du chemin testé | PASS observé |
| Absence de MP4 final après interruption | PASS observé, y compris vérification différée de cinq secondes |
| Nettoyage temporaire après SIGTERM | PASS observé |
| Relance complète et décodage | PASS |
| Isolation du rendu contre une modification transitoire du projet source | PASS sur le cas testé |
| Préservation de l'élément protégé sur ce rendu | PASS par précontrôle et empreinte identique du MP4 |
| Arrêt brutal SIGKILL, panne machine, coupure d'alimentation | NOT TESTED |
| Résistance aux changements pendant la copie initiale, symlinks malveillants ou modifications de la copie par un acteur autorisé | NOT DEMONSTRATED |
| Détection de toutes les mutations transitoires de la source | NON : le résultat est isolé, mais une mutation puis restauration peut ne pas être signalée |
| Contrôle obligatoire dans tous les chemins FrameForge | NON : appel direct à HyperFrames toujours possible |
| Approbation humaine immuable et recette perceptive | NOT DEMONSTRATED |

## Décision

**REUSE_EXISTING + EXPERIMENT.** Les deux contre-exemples FF-10 sont corrigés sur le chemin expérimental isolé. Ne pas promouvoir ce script en garantie globale ni fermer FF-10 sans définir et tester le chemin de production effectivement obligatoire, l'approbation humaine et les limites de sécurité. Pas de moteur ou d'orchestrateur supplémentaire. Les MP4 restent locaux.
