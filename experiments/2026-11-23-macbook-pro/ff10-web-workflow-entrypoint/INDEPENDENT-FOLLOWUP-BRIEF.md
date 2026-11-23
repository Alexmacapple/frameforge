# FF-10 — Contre-revue indépendante du correctif (mission de reprise)

23 novembre 2026. Révision à examiner : bb6f840. Mission à confier à un évaluateur distinct de l'auteur des correctifs.

## Question centrale

Les deux défauts bloquants relevés dans la première contre-revue sont-ils réellement corrigés ?
1. Un MP4 décodable mais trop court et dépourvu de narration peut-il encore recevoir PASS et un nom final ?
2. Le pilote et ses tests sont-ils rejouables depuis un checkout neuf sans médias locaux non versionnés ni résultat historique ?

## Méthode aveugle

1. Fixer le SHA de lecture, examiner le code, les entrées versionnées et les tests avant de consulter les rapports de correction.
2. Reconstituer le pilote depuis une copie propre avec prepare_fixture.py, puis lancer la suite ; distinguer PASS, FAIL, SKIP.
3. Tester des faux MP4 : 0,5 s sans audio ; 16,17 s sans audio ; bonne durée et pistes mais audio différent ; vidéo avec résolution ou cadence incorrecte ; contenu visuel sans les trois gestes. Vérifier si chaque sortie invalide est refusée avant le dépôt final.
4. Exécuter un vrai rendu HyperFrames si l'environnement le permet ; documenter précisément tout échec d'installation.
5. Vérifier les liens symboliques, la concurrence, les changements pendant la copie et l'interruption, en distinguant observations nouvelles et preuves historiques.
6. Vérifier si les empreintes sont une autorité indépendante, si les autres points d'entrée sont contournables et si la V5 bénéficie d'une approbation perceptive humaine.
7. Geler les verdicts avant de consulter OUTPUT-QA-FOLLOWUP.md, REPRODUCIBILITY-RESULT.md et les anciens rapports.

## Verdicts attendus

Pour chaque garantie : PASS, FAIL ou UNVERIFIED avec commande reproductible, sortie et périmètre. Distinguer garantie du pilote et promotion en production. Un rendu réel PASS ne prouve pas la présence des trois actions visuelles, ni l'intelligibilité de la narration.

## Restrictions

Lecture et tests sur copies isolées uniquement ; pas de modification du produit, pas de fermeture de FF-10, pas de publication de média, pas d'approbation éditoriale attribuée à l'utilisateur.
