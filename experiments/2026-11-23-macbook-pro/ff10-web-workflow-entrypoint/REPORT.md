# FF-10 — Chemin npm contrôlé sur une démonstration web narrée

23 novembre 2026. Protocole préalable : PROTOCOL.md, commit 8b77b0d. **Verdict : PASS du chemin npm de cette copie ; non-contournement produit UNVERIFIED.**

## Expérience

Composition V5 Kokoro (16,166 s, trois phrases de narration et capture d'interface). Copie indépendante de l'original. Le package.json de la copie remplace npm run render par un appel à render_guarded.py ; npm run publish refuse explicitement. L'original n'est pas modifié.

Le script appelle le précontrôle existant, vérifie la référence de fixture par SHA-256 de4a2b7c434d9e168f891999a4f82d782daaba76253a774dcbabbc1d72b8bfd1, puis utilise le wrapper HyperFrames V2 pour isoler les médias, rendre et décoder intégralement le MP4.

Modification autorisée : fond du premier sous-titre #111 vers #222. Le second et le troisième sous-titres restent inchangés.

## Résultats exécutés

- Modification du sous-titre 2 : rejet protected_caption2_changed.
- Référence substituée : rejet approved_fixture_digest_mismatch.
- npm run publish : refus explicite (code non nul), aucun média diffusé.
- npm run render : PASS ; MP4 local produit.
- SHA-256 MP4 : 9fbb7c316fb20ef94a0424f231881b5f0f24d86daf32418aadc1a92e94ae11ad.
- Durée, pistes et nombre d'images : ffprobe.json.
- Décodage complet FFmpeg : PASS par le wrapper.

## Réserves

La référence est une fixture de test, pas une approbation humaine du film V5. La commande npm publish est neutralisée **uniquement dans cette copie** ; les autres projets et appels directs à HyperFrames restent accessibles. Ce test ne vérifie ni la perception du film par un humain, ni le verrouillage des identifiants de publication, ni toutes les ressources possibles d'un projet général. La présence de l'audio et son décodage ne prouvent pas sa qualité.

## Décision

**REUSE_EXISTING + EXPERIMENT.** Le chemin npm nominal contrôlé est viable sur la démonstration web. Ne pas généraliser automatiquement le wrapper aux 22 compositions expérimentales, ne pas fermer FF-10, et ne pas publier le média. La prochaine décision nécessite une recette humaine du film et le choix d'un chemin produit officiel.
