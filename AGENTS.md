# AGENTS.md — FrameForge

## Mission
Construire le plus petit système permettant de produire une vidéo réelle, narrée et vérifiable. Préserver les objectifs et exclusions du brief.

## Avant de coder
1. Lire README, WHY, INTENT, SPEC, PLAN.
2. Identifier la fonction existante dans HyperFrames, agent-browser ou ShipGuard avant toute implémentation.
3. Vérifier les licences et fixer les versions/SHA.
4. Définir le résultat observable et le test qui échouerait si l'action était sautée.
5. Poser une question si deux interprétations changent matériellement le résultat.

## Pendant la production
- Séparer capture observée, média simulé et proposition éditoriale.
- Journaliser provenance, paramètres, versions et erreurs.
- Ne pas publier de vidéo, de données ou de modifications distantes sans approbation explicite.
- Ne jamais cacher un échec en sautant un geste, en raccourcissant une scène ou en modifiant le résultat attendu.
- Ne pas ajouter de framework, orchestrateur ou contrôle redondant sans preuve d'un manque.

## Vérification
- Vérifier le parcours normal et le cas d'échec.
- Mesurer la durée audio, les cues, le décodage vidéo et la concordance des sous-titres.
- Contrôler les informations sensibles sur l'ensemble des images, transitions et métadonnées.
- Produire un rapport texte distinguant `PASS`, `FAIL`, `UNVERIFIED`, `NOT_APPLICABLE`.
- Demander une revue humaine avant toute diffusion.

## ShipGuard
Pré-revue avant ajout, audit des invariants temporels, contrôle des diffs ; ne pas lui attribuer une validation audiovisuelle qu'il n'effectue pas.
