# FF-11 — Précontrôle éditorial avant rendu, variante V2

Date : 23 novembre 2026. Comparaison avec le FAIL archivé dans ../ff11-editorial-autonomy-pilot/REPORT.md. Ce document est figé AVANT le nouveau rendu.

## Garantie expérimentée

Une justification de plan portant sur un sujet **visible** doit être vérifiée par des images échantillonnées dans **l'intervalle exact** proposé, avant de déclencher le rendu. L'audio présent ne prouve pas qu'une personne est visible.

Protocole : extraction FFmpeg à +0,5, +1,5, +2,5, +3,5, +4,5, +5,5 secondes dans chaque plage, soit six images par intervalle. Inspection des planches de contact par le modèle. Il ne s'agit pas d'un détecteur automatique, d'un examen de chaque image, ni d'une validation humaine.

## Résultats avant rendu

| Proposition | Images | Verdict |
| --- | --- | --- |
| ISS 105–111 s : montrer la Terre et des éléments de l'ISS | evidence/iss-sheet.jpg : Terre et matériel de station visibles sur plusieurs images | PASS sur 6 échantillons |
| NISAR 158–165 s : montrer une intervenante scientifique | evidence/nisar-failed-sheet.jpg : public et groupe, puis fusée ; pas d'intervenante en entretien | **FAIL** |
| NISAR 60–67 s : montrer une application d'observation puis une intervenante scientifique | evidence/nisar-candidate-sheet.jpg : agriculture, carte du littoral, puis intervenante à partir d'environ 63,5 s | PASS sur 6 échantillons, avec précision temporelle |

## Décision éditoriale V2

Conserver ISS 105–111 s ; **remplacer NISAR 158–165 s par NISAR 60–67 s**. Le plan 2 ne doit PAS être décrit comme sept secondes d'intervention face caméra : il contient d'abord des images d'application, puis la personne qui parle. La parole source reste à contrôler, et les SRT existants ne sont pas repris automatiquement.

Critère de décision : le nouveau plan 2 contient visuellement une intervenante dans plusieurs images du passage et des applications d'observation de la Terre au début. Cela corrige l'écart de correspondance image/justification, sans prouver la qualité narrative ni la fidélité des paroles.

**Limites :** corpus déjà connu, sélection et inspection par le même modèle, images espacées d'une seconde, pas d'évaluation indépendante ni de contrôle juridique. Aucune nouvelle architecture.
