# Évaluation du projet au 24 novembre 2026

Évaluation demandée par Alex en fin de session et rédigée par un agent, à la révision 290f8d7. Les chiffres sont relevés dans le dépôt et sur GitHub ; les notes et le verdict sont un jugement de l'agent qui a fait une grande partie du travail évalué, pas une revue indépendante. La notation est volontairement sévère : un point bloquant existe, aucun film utile n'est encore sorti de la chaîne.

## Les chiffres

- **Durée du projet** : deux jours (23 et 24 novembre 2026), 191 commits, 23 PR fusionnées.
- **Films produits** : trois, pour 47 secondes au total (15, 16 et 16 secondes). Tous sur des pages de démonstration, aucun diffusé.
- **Code** : environ 2 000 lignes d'outils dans `film-chain`, 2 700 lignes de tests pour les protéger ; 7 900 lignes de Python au total dans le dépôt, dont 4 000 de tests.
- **Documents** : 132 fichiers Markdown, 4 500 lignes, soit plus du double du code des outils.
- **Essais** : 45 dossiers sous `experiments/2026-11-23-macbook-pro/`.
- **Critères du plan d'origine prouvés** : 16 sur 66 (issues 5 à 10, relevé du ticket 49).
- **Issues** : 20 ouvertes, 12 fermées.
- **Intégration continue** : aucune. Tout tourne sur un seul Mac.

## Notes par critère, sur 5

- **Utilité livrée : 1.** Aucun film ne répond à un besoin réel.
- **Solidité du garde : 4.** 194 tests, 95 contrôles surveillés un à un, deux relectures indépendantes, une vingtaine de défauts corrigés. Un point retiré : les dernières corrections n'ont pas été relues par un tiers.
- **Qualité audiovisuelle prouvée : 2.** Beaucoup de mesures automatiques, presque aucune vérification par une personne qui découvre le film.
- **Reproductibilité : 2.** Un seul Mac, médias en un seul exemplaire, voix qui varie d'une synthèse à l'autre.
- **Coût et vitesse : 1.** Le temps nécessaire pour fabriquer un film n'a jamais été mesuré.
- **Traçabilité : 4.** Tout est écrit et retrouvable, au prix d'un volume de documents élevé.
- **Droits et confidentialité : 2.** Données fictives, mais licence de la voix non confirmée.

**Moyenne : environ 2,3 sur 5.** Un prototype techniquement sérieux dont l'utilité n'est pas démontrée.

## Forces

- La chaîne fonctionne de bout en bout : fiche, capture, voix, sous-titres, rendu.
- Un film fautif est refusé au lieu de sortir en silence, ce que l'outil de rendu seul ne fait pas.
- Tout tourne en local, sans service payant ni donnée envoyée ailleurs.
- Les sous-titres et la transcription sortent du même texte que la voix.

## Faiblesses

- L'effort est allé au contrôle, pas à la fabrication. Le garde est plus solide que ce que le risque réel demande.
- Chaque film demande encore d'écrire à la main ses gestes et son calage sur la voix.
- Personne d'autre que son auteur ne peut utiliser la chaîne aujourd'hui.
- La recette par une personne manque presque partout.

## Opportunités

- **Refaire un film quand la page change.** C'est là que la chaîne pourrait battre une capture d'écran faite à la main. Hypothèse à vérifier : elle n'a pas été testée.
- Produire des démonstrations accessibles : sous-titres et transcription sont déjà là.
- Servir de base aux vidéos pédagogiques, si le premier vrai film est concluant.

## Menaces

- Continuer à perfectionner l'outil sans jamais s'en servir.
- La dépendance à HyperFrames, à Kokoro et à Playwright, qui évoluent vite.
- La licence de la voix, qui peut interdire la diffusion.
- Un outil du commerce qui ferait la même chose plus simplement. Aucune comparaison n'a été faite.

## Verdict

- **Comme outil de production, aujourd'hui : non, pas encore utile.** Rien de ce qui est sorti ne sert un besoin.
- **Comme apprentissage et comme socle : oui.** On sait que la chaîne tient, ce qu'elle coûte à protéger, et où elle demande un humain.

## Ce qui tranchera

Le ticket 47 : un vrai film de 30 à 60 secondes, avec le temps passé et les interventions humaines mesurés.

- Si le film demande plus d'une demi-journée et ne sera jamais refait, la chaîne ne se justifie pas.
- S'il doit être refait à chaque évolution de la page, elle peut devenir rentable dès la deuxième fois.

Recommandation : ne plus rien construire avant d'avoir ce chiffre.

## Limites de cette évaluation

- Le seuil d'une demi-journée est une estimation de l'agent, pas une mesure.
- Les notes ne viennent d'aucune grille externe ; un autre évaluateur pourrait peser les critères autrement.
- Aucun film n'a été rouvert pour cette évaluation, aucun test rejoué : les chiffres de tests sont ceux du dernier passage de la journée.
