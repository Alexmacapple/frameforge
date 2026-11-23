# FF-10 — Arbitrage du point d'entrée de production

23 novembre 2026. Révision examinée : 0102447. Décision proposée après vérification des preuves FF-10 et de PUBLICATION-POLICY.md, PLAN.md et research/ff10-production-workflow-decision-2026-11-23.md.

## Décision

**REUSE_EXISTING + REFERENCE_PATH_ONLY + NO-GO_GLOBAL_PRODUCTION.**

Pour le cas *démonstration web narrée V5*, désigner le script npm render du pilote, qui appelle render_guarded.py puis guarded_hyperframes_v2.py, comme **chemin de référence documenté**. Le contrôle des entrées, la copie isolée, le rendu HyperFrames et la validation du MP4 avant dépôt sont réutilisés. Ne pas développer de nouveau moteur, orchestrateur ou service d'approbation.

Cette désignation est documentaire : elle ne rend pas techniquement le chemin obligatoire. Ne pas la présenter comme une promotion globale en production.

## Preuves favorables

- Reconstruction des ressources versionnées depuis une archive propre, avec 14 PASS et 2 SKIP sur les tests du checkout neuf, puis rendu réel PASS sur Mac.
- Contrôle des fichiers sources, du MP4 final et de la cadence moyenne : tests positifs et négatifs, contre-revues indépendantes ciblées.
- MP4 V5 de 16,166667 s, SHA-256 9fbb7c316fb20ef94a0424f231881b5f0f24d86daf32418aadc1a92e94ae11ad.
- Validation éditoriale humaine explicite de ce MP4 exact, enregistrée dans HUMAN-EDITORIAL-APPROVAL-V5.md ; **aucune autorisation de diffusion**.

## Limites maintenues

- Autres scripts HyperFrames directs encore disponibles ; pas de contrôle global des permissions.
- Empreintes de référence modifiables par un acteur ayant les droits d'écriture au code.
- Contrôle de cadence moyenne ≠ cadence constante.
- Différences de pixels entre fenêtres ≠ preuve que les trois gestes sont visibles et compréhensibles.
- Aucun test séparé documenté de compréhension de la narration sans image.
- Échec de l'installation HyperFrames dans l'environnement Linux de la contre-revue ; preuve de reproductibilité sur Mac uniquement.
- Le pilote conserve des seuils spécifiques à la V5 ; ne pas les imposer à d'autres vidéos.

## Contrat recommandé pour les prochains films de démonstration web

1. Identifier les sources autorisées, le scénario, la référence éditoriale et les droits d'utilisation.
2. Reconstruire les entrées depuis des ressources versionnées ou autorisées, puis épingler les empreintes.
3. Rendre uniquement un brouillon local par le point d'entrée contrôlé adapté à ce projet.
4. Refuser tout film ne satisfaisant pas au contrat de sortie propre au projet.
5. Vérifier les gestes réellement visibles, les sous-titres et la compréhension sans image ; consigner les preuves, sans confondre mesures et appréciation humaine.
6. Associer toute validation éditoriale à une empreinte exacte.
7. Garder le média non diffusable tant qu'une autorisation distincte n'identifie pas sa version et sa destination.

## Conditions avant promotion générale

- Définir le périmètre précis du produit : démonstration web uniquement ou toutes compositions.
- Choisir un point d'entrée obligatoire si la garantie de non-contournement est réellement exigée, et démontrer sa couverture.
- Définir qui peut approuver et modifier les références éditoriales.
- Réaliser une recette de trois gestes avec observations horodatées, distincte de la seule comparaison de pixels.
- Évaluer la nécessité d'une cadence constante au lieu de la seule moyenne.
- Maintenir une autorité de publication séparée des agents de rendu.

## Décision opérationnelle

**GO pour utiliser le chemin contrôlé comme référence de nouveaux brouillons web expérimentaux. NO-GO pour le déclarer obligatoire ou prêt pour une production générale.** FF-10 reste ouvert. Aucun média transmis ni publié. Toute décision de promotion exige un arbitrage humain explicite.
