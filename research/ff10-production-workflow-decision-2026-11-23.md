# FF-10 — Décision sur le chemin de production

Date : 23 novembre 2026. SHA initial : 21e1087. **Verdict : REUSE_EXISTING + NEEDS_INTEGRATION, pas de promotion générale.**

## Preuves réexaminées

- Tests unitaires FF-10 deux rushes rejoués : 4/4 PASS.
- Tests de référence approuvée FF-10 rejoués : 5/5 PASS.
- Le pilote de remontage successif (SUCCESSIVE-EDIT-REPORT.md) a démontré une modification du premier passage et 106 images identiques du second ; résultat historique, pas un nouveau rendu pendant cette revue.
- Les scripts HyperFrames des projets expérimentaux invoquent directement HyperFrames 0.8.33 render. Le package.json au niveau experiments/2026-11-23-macbook-pro contient aussi un script publish invoquant directement HyperFrames publish.
- Le contrôleur expérimental est invoqué explicitement par les scripts de test. Aucun point d'entrée de production unique obligatoire n'a été établi.
- README décrit encore un cadrage V0.3 ; INTENT/PLAN séparent le MVP démonstration web de l'extension au montage de rushes.

## Décision technique

Ne pas annoncer une chaîne de production verrouillée. Ne pas fusionner les versions FF-10 en une API générale avant de définir le cas produit exact et ses assets. Réutiliser le wrapper V2 paramétrable pour les projets expérimentaux qui en ont besoin, et maintenir le contrôle de l'approbation comme une responsabilité séparée.

Chemin recommandé : sélectionner une composition concrète, identifier toutes ses ressources, définir une correction réellement approuvée, effectuer le rendu isolé avec précontrôle et QA, puis présenter le brouillon local à la revue humaine. Pour la publication, suivre PUBLICATION-POLICY.md ; la validation technique ne vaut pas autorisation.

## Risque de publication

La présence d'un script npm publish ne prouve ni diffusion ni exécution. Elle montre qu'un chemin direct existe. Une garantie technique de non-publication exigerait un contrôle des identifiants et droits, non implémenté ici.

## Conditions de promotion

1. Un workflow nominal choisi et documenté, sans chemins alternatifs non déclarés pour ce workflow.
2. Des tests adversariaux exécutés depuis le point d'entrée réellement utilisé.
3. Une référence de correction issue d'une validation humaine et une autorité de référence définie.
4. Une recette perceptive humaine d'un film représentatif, séparée des tests automatiques.
5. Une règle de publication applicable au canal utilisé, avec accord explicite sur version et destination.

## Décision FF-10

**PARTIAL PASS.** Les tests de préservation sont probants sur les fixtures et sur le remontage ciblé. Le non-contournement produit, la recette humaine du film complet et l'application à un projet représentatif restent UNVERIFIED. Garder FF-10 ouvert. Aucun média publié.
