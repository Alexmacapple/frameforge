# FF-10 — Vérification d'une référence approuvée par empreinte

23 novembre 2026. Protocole préalable : APPROVAL-PIN-PROTOCOL.md, commit 9b87dce.

## Résultats

La référence HTML baseline de la fixture TodoMVC possède le SHA-256 suivant :
340fb7b0ffc17605d6f1bbcd9892928c24236b75e44c9a3821a79dac2c9abdb7.

Le nouveau point d'entrée expérimental guarded_hyperframes_v3.py exige l'empreinte attendue via --approved-sha256. Il refuse toute référence ne correspondant pas à cette valeur, puis délègue l'isolation et le rendu à guarded_hyperframes_v2.py.

- Cinq tests unitaires : PASS.
- Modification autorisée, baseline et empreinte intactes : rendu HyperFrames 0.8.33 PASS ; MP4 SHA-256 07e8dd7d237877a5c80d8210f6c69a2cb1ac1ceb56c139e7da93dae149e20324.
- Modification interdite du second sous-titre avec baseline intacte : rejet par précontrôle, test unitaire PASS.
- Substitution de la référence HTML par un fichier modifié : rejet avant rendu, raison approved_reference_digest_mismatch ; aucun MP4 adversarial.
- Le projet source et les médias ne sont pas modifiés ; MP4 de test local.

## Limite de confiance déterminante

L'empreinte attendue est fournie en argument de ligne de commande. **Elle n'est pas protégée par une autorité indépendante de l'agent.** Si l'agent peut choisir ou réécrire l'empreinte en même temps que la baseline, le contrôle peut être contourné. Le SHA-256 ne prouve pas qui a approuvé la version ; il vérifie seulement sa concordance avec une empreinte attendue. Aucun acte d'approbation humaine formel n'a été recueilli pour cette fixture.

## Décision

**PASS technique à périmètre limité ; NOT DEMONSTRATED pour l'authenticité de l'approbation et le non-contournement produit.** Conserver l'implémentation comme expérience. Ne pas promouvoir le point d'entrée en production ni clore FF-10. Prochaine décision : identifier le propriétaire et le stockage fiable de l'empreinte d'approbation et vérifier que les agents de rendu ne peuvent pas les modifier.

Aucun nouveau moteur ni orchestrateur. Aucun média publié.
