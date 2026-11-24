# GLOSSARY — FrameForge V1

Glossaire métier consolidé après les cinq tours de `grill-with-docs` (D1 à D16, 23 novembre 2026). Les définitions n'imposent aucun modèle de stockage ni API.

## Production et narration
- **Production** : ensemble des travaux destinés à réaliser une vidéo à partir d'un objectif et de sources autorisées.
- **Exploration** : recherche et observation des éléments nécessaires à une production.
- **Scène** : unité narrative présentant une action, une information ou un résultat cohérent.
- **Plan** : portion visuelle continue ou fixe d'une scène.
- **Geste** : interaction observable avec une interface.
- **Résultat observable** : état effectivement constaté à l'issue d'un geste.
- **Repère temporel** : position permettant de coordonner un événement, une image ou une parole.
- **Synchronisation** : alignement des éléments visuels et sonores sans altération silencieuse de leur sens.
- **Raccord honnête** : transition rendant explicite une discontinuité significative, notamment une attente raccourcie.

## Provenance et preuves
- **Preuve** : élément vérifiable soutenant une affirmation dans un contexte déterminé.
- **Preuve originale** : élément de référence conservé distinctement de ses transformations éditoriales.
- **Preuve actuelle** : preuve dont la pertinence pour le contexte examiné a été revérifiée.
- **Preuve historique** : preuve d'un état antérieur qui ne démontre pas à elle seule l'état actuel.
- **Manifeste de provenance** : inventaire reliant scènes, affirmations et éléments qui les justifient ; il ne constitue pas lui-même une preuve.
- **Statut de preuve** : qualification d'un élément comme observé, raisonné, prévu, non vérifié ou en échec.
- **Statut de validation** : qualification indépendante indiquant si les vérifications requises pour une scène ou un film ont été satisfaites.

## Validation et reprise
- **Brouillon** : production incomplète ou non encore validée.
- **Scène validée** : scène dont les éléments requis ont été vérifiés.
- **Film validé** : film dont les scènes et l'assemblage ont été vérifiés.
- **Version approuvée** : version déterminée d'un film ayant reçu une approbation humaine.
- **Diffusion autorisée** : état d'une version dont la publication a été explicitement approuvée.
- **Étape invalide** : étape dont le résultat manque, est incorrect ou ne satisfait plus les conditions attendues.
- **Dépendance affectée** : élément dont la validité peut être remise en cause par un changement ou un échec.
- **Reprise** : réexécution ciblée des étapes invalides et des vérifications affectées.
- **Contrôle affecté** : vérification à renouveler après un changement susceptible d'invalider son résultat.
- **Changement significatif** : modification susceptible d'affecter le sens, les preuves, la compréhension ou la confidentialité.
- **Réapprobation** : nouvelle approbation humaine d'une version significativement modifiée.
- **Repli technique** : utilisation d'un autre chemin de production lorsque le chemin principal échoue, sous réserve de garanties équivalentes.

## Chaîne de fabrication d'un film

Termes des outils de `experiments/2026-11-23-macbook-pro/film-chain/`, ajoutés le 24 novembre 2026. Ils nomment des fichiers et des gestes, pas des notions métier nouvelles.

- **Fiche** : le manifeste de provenance d'un film, fichier `provenance-manifest.json`.
- **Empreinte** : somme SHA-256 d'un fichier, qui dit si son contenu a changé.
- **Entrée figée** : fichier dont l'empreinte est consignée ; le rendu est refusé si elle ne correspond plus.
- **Garde de rendu** : `render_guarded.py` d'un film ; il contrôle les entrées figées et la fiche avant le rendu, puis le film obtenu avant son dépôt.
- **Refiger** : recalculer les empreintes après un changement voulu (`repin.py`). Refiger n'est pas approuver.
- **Reçu de rendu** : fichier écrit par le garde à côté du film, qui dit de quelles entrées ce film est sorti.
- **Journal de capture** : `capture-events.json`, les dates des gestes et les états relus dans la page pendant la capture.
- **Contrôle par mutation** : retirer chaque contrôle l'un après l'autre et vérifier qu'un test s'en aperçoit (`mutation_check.py`).

Une preuve observée ne vaut pas validation automatique d'une scène ; un film validé ne vaut pas autorisation de diffusion.
