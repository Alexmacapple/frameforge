# FF-11 — Précontrôle avant rendu : correction de l'erreur éditoriale

Date : 23 novembre 2026. **Verdict : PASS limité sur la correspondance images/justification ; autonomie non démontrée.**

## Méthode et références

Le FAIL du premier essai reste conservé dans ../ff11-editorial-autonomy-pilot/REPORT.md. La décision V2 a été figée **avant rendu**, commit 4ebf59c, dans PREFLIGHT-DECISION.md.

Trois intervalles ont été contrôlés par six images FFmpeg espacées d'une seconde, à +0,5, +1,5, +2,5, +3,5, +4,5, +5,5 s : ISS 105–111 s, NISAR 158–165 s (contre-exemple), NISAR 60–67 s (correction). Planches de preuve dans le sous-dossier local evidence/.

- ISS 105–111 s : Terre et éléments de la station visibles ; PASS sur échantillons.
- NISAR 158–165 s : public, groupe, fusée, sans entretien face caméra ; FAIL sur l'exigence initiale.
- NISAR 60–67 s : agriculture et changements du littoral, puis intervenante visible dans les dernières secondes ; PASS sur échantillons. **La personne n'est pas visible pendant les sept secondes entières**.

## Nouveau rendu

La composition V2 réutilise les extraits déjà découpés localement, sans navigateur ni nouvelle architecture. Rendu HyperFrames 0.8.33 : clips/ff11-preflight-v2.mp4.

- 13,000 secondes, 390 images, H.264/AAC ; décodage intégral FFmpeg PASS.
- Image de contrôle à 11 secondes : intervenante visible ; PASS sur échantillon.
- SHA-256 MP4 local : ed9f145189fc813df23ee68a9d3bc38e345112f5fef5916eb8a3f6276bbb43fd.
- Aucun sous-titre anglais/français validé n'a été réutilisé automatiquement. Les droits NASA et la qualité perceptive restent UNVERIFIED.

## Garanties et limites

| Contrôle | Verdict |
| --- | --- |
| Détection de l'ancien intervalle inadapté AVANT rendu | PASS pour cet intervalle et cette inspection |
| Justification visuelle du nouveau plan | PASS sur six images pré-rendu et une image post-rendu |
| Rendu de la correction | PASS technique |
| Validation exhaustive de toutes les images et de la parole | UNVERIFIED |
| Choix autonome à partir de rushes inconnus | NOT DEMONSTRATED : corpus déjà connu |
| Recette humaine et droits de diffusion | UNVERIFIED |

**Décision : REUSE_EXISTING.** Les outils FFmpeg et HyperFrames suffisent à réaliser ce précontrôle expérimental. Ne pas construire de détecteur, d'index ou d'orchestrateur. Pour valider une garantie produit, tester ensuite un brief et des rushes non vus, avec un évaluateur indépendant et des critères préenregistrés. FF-11 reste ouvert.

Les rushes et le MP4 restent sur le MacBook Pro ; seuls les rapports et les sources de composition sont publiés sur GitHub.
