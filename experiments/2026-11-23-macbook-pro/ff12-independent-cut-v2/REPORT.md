# FF-12 — Rendu local des coupes proposées par AlexDot

Date : 23 novembre 2026. **Verdict : PASS technique ; PARTIAL éditorial ; accessibilité UNVERIFIED.**

## Origine de la décision

La sélection indépendante d'AlexDot a été fournie par l'utilisateur, avec un gel antérieur à la confrontation. La proposition retenue ici utilise uniquement la vidéo NASA B « What Spacecraft Saw During the 2017 Solar Eclipse » (ID GSFC_20170830_MultiSpacecraft_m12698_eclipse).

- Plan 1 : B [9,500 ; 17,500[ (8 s), images du Soleil observées par SDO.
- Plan 2 : B [36,000 ; 41,500[ (5,5 s), images de la Terre observées par DSCOVR.
- La sélection primaire FF-12 B [10 ; 16[ puis B [34 ; 42[ est préservée dans ../ff12-plausible-distractor/SELECTION-PRIMARY.md. Les nouvelles coupes évitent de terminer sur Terra.

## Vérification pré-rendu

Les six images de chaque intervalle sont extraites avec FFmpeg à la borne initiale, +0,1 s, +0,5 s, milieu, fin -0,5 s et dernière image approximative. Résultats et réserves : PREFLIGHT-AND-SELECTION.md. Images locales dans local/evidence/. Le premier plan change de cadrage en cours de séquence ; le second comporte des variations de la zone sombre et ne constitue pas une prise continue en temps réel.

## Rendu et QA

- HyperFrames 0.8.33, montage local local/ff12-independent-cuts-13s5-DRAFT.mp4.
- FFprobe : **13,500 secondes, H.264, 405 images**, aucune piste audio.
- FFmpeg : décodage complet sans erreur.
- Images post-rendu échantillonnées aux secondes 0,5 ; 4 ; 7,5 ; 8,1 ; 10 ; 13,2. À 10 s, Terre avec bandeau DSCOVR. Ces images ne prouvent pas le rythme perçu ou la compréhension.
- SHA-256 MP4 : 4f7dc65a33c40f97b1e77f0534dbccf9a32e317aadf785fc6577df743ae50205.
- Médias NASA et MP4 restent sur le MacBook Pro, hors Git.

## Statuts

| Dimension | Verdict |
| --- | --- |
| Décision indépendante préalable | PASS documentaire, rapport transmis par l'utilisateur |
| Contrôle des bornes | PASS limité aux échantillons |
| Correction du mélange d'instruments dans le plan terrestre | PASS limité aux échantillons |
| MP4 13,5 s décodable | PASS |
| Rythme, continuité et intelligibilité de l'ombre | UNVERIFIED : pas de visionnage humain à vitesse réelle |
| Compréhension sans image | FAIL pour cette version muette |
| Narration et sous-titres | NOT DONE |
| Droits de diffusion | UNVERIFIED |
| Autonomie éditoriale générale | NOT DEMONSTRATED |

## Décision

**REUSE_EXISTING.** Aucune nouvelle architecture. Conserver ce film comme témoin technique des coupes d'AlexDot. Faire une recette humaine de continuité visuelle avant de décider d'une narration française. Ne pas clôturer FF-12, ne pas publier les médias.
