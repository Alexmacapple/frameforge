# FF-10 — Rejeu après épinglage du manifeste

23 novembre 2026. SHA de départ 922536d. Revue exécutée par l'auteur du pilote, **non indépendante**.

## Vérifications exécutées

1. Altération locale de captions.srt, appel à npm run render : refus avec ValueError: protected_asset_changed:captions.srt, code de sortie 1. Fichier restauré après essai.
2. Altération locale de asset-pins.json, appel à npm run render : refus avec ValueError: asset_manifest_changed, code de sortie 1. Fichier restauré après essai.
3. Un test de modification de voice2.m4a par ce même script a été volontairement ignoré : c'est un lien symbolique vers une ressource partagée. Le test unitaire correspondant utilise une copie temporaire, pas le média original.
4. Rendu complet via npm run render après le dernier durcissement du précontrôle du snapshot : PASS. MP4 local SHA-256 9fbb7c316fb20ef94a0424f231881b5f0f24d86daf32418aadc1a92e94ae11ad, identique à la version précédente. Le wrapper a effectué un décodage FFmpeg intégral.

## Conclusion

**PASS technique limité** pour les deux scénarios adversariaux au point d'entrée npm et le rendu complet après durcissement. Les résultats n'établissent ni l'autorité humaine sur les empreintes, ni le non-contournement des autres chemins, ni une recette perceptive. Le film reste DRAFT et FF-10 ouvert.

La mission d'une contre-revue réellement indépendante est définie dans INDEPENDENT-REVIEW-BRIEF.md ; **elle n'a pas encore été exécutée**. Aucun média diffusé.
