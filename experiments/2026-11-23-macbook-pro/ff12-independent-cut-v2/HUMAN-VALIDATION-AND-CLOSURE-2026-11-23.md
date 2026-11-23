# FF-12 — Recette humaine rapportée et clôture du pilote expérimental

Date : 23 novembre 2026. **Verdict : PASS à périmètre limité ; autonomie éditoriale générale NON DÉMONTRÉE.**

## Périmètre

FF-12 teste un corpus NASA de trois sources astronomiques proches, dont un transit lunaire et un tutoriel d'éclipse lunaire. Après une contre-revue indépendante AlexDot, le rendu local a conservé les coupes de la vidéo NASA B : SDO [9,500 ; 17,500[ et DSCOVR [36,000 ; 41,500[. Le film final expérimental local, non diffusé, est ff12-narrated-fr-subtitled-DRAFT.mp4 (13,5 secondes). La sélection primaire initiale reste archivée, sans correction rétrospective.

## Preuves techniques existantes

- Contrôles de bornes et justification des coupes : PREFLIGHT-AND-SELECTION.md.
- Rendu muet de 13,5 s et 405 images : REPORT.md.
- Ajout de la voix française Kokoro et d'une piste de sous-titres français : NARRATION-QA-2026-11-23.md.
- SHA-256 du MP4 narré : 26d5242151aa1b4288f8f64e377d7acd443e5d3a4646f7c249085fd3b5917b66.
- Média NASA et film local uniquement ; pas de publication de la vidéo.

## Retours humains déclarés dans la conversation

1. Après le visionnage du montage muet, l'utilisateur confirme qu'une autre personne a compris l'enchaînement Lune devant le Soleil puis ombre sur la Terre (« oui »). **PASS rapporté**, sans verbatim détaillé ni contrôle indépendant du contexte de visionnage.
2. Après écoute de la version française narrée, l'utilisateur répond « oui ca va » à une question sur la clarté de la voix, les sigles et la compréhension sans image. **Retour positif rapporté**, sans évaluation séparée de chaque dimension.
3. Après activation des sous-titres dans QuickTime, l'utilisateur répond « oui » à la question sur l'affichage au bon moment et la correspondance à la narration. **PASS humain rapporté** pour l'affichage et la synchronisation, non mesuré image par image.

Ces déclarations ne constituent pas une étude d'utilisabilité ni une preuve de fidélité exhaustive des sous-titres.

## Matrice de clôture

| Dimension | Statut |
| --- | --- |
| Choix des sources et contre-revue indépendante | PASS limité ; écarts documentés |
| Détection des changements de scène et correction des coupes | PASS sur les échantillons contrôlés |
| Rendu H.264/AAC, 13,5 s, 405 images | PASS technique |
| Narration française et compréhension sans image | PASS rapporté par l'utilisateur, sans verbatim |
| Sous-titres français sélectionnables et synchronisés | PASS rapporté dans QuickTime |
| Qualité perceptive à plus grande échelle | UNVERIFIED |
| Droits de diffusion et crédits définitifs | UNVERIFIED ; diffusion non autorisée par cette clôture |
| Sélection autonome généralisable | NOT DEMONSTRATED |

## Décision

**Clôturer le pilote FF-12 comme expérimentation locale terminée à périmètre limité.** Cette décision ne ferme pas automatiquement une issue GitHub : son identifiant et son périmètre doivent être vérifiés avant toute clôture d'issue. Conserver les contre-exemples, les sources et les gels de sélection. Aucun nouvel outil ni moteur de montage n'est justifié.

Suite produit séparée : tester la sélection de rushes réellement inconnus, la continuité du récit, et la préservation des corrections humaines après interruption/reprise. Ne pas multiplier les pilotes NASA sans nouvelle question discriminante.
