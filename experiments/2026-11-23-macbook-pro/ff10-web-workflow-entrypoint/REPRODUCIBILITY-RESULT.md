# FF-10 — Reproductibilité depuis une archive propre

23 novembre 2026. Protocole préalable : REPRODUCIBILITY-PROTOCOL.md, commit 8838445. **Verdict : PASS technique sur MacBook Pro ; reproductibilité multi-OS UNVERIFIED.**

## Reproduction

- Archive propre créée à partir de main après ajout du script de reconstruction, SHA 445237e.
- Dossier de test isolé sous /tmp/ff10-clean-7WeAnN ; aucun accès aux fichiers locaux du premier pilote nécessaire.
- Exécution de prepare_fixture.py : PASS, neuf empreintes vérifiées, référence HTML SHA-256 de4a2b7c434d9e168f891999a4f82d782daaba76253a774dcbabbc1d72b8bfd1.
- Exécution de 16 tests : 14 PASS et 2 SKIP explicites, correspondant aux assertions sur le MP4 historique absent de l'archive.
- Rendu HyperFrames 0.8.33 réel dans la copie propre via npm run render : PASS. MP4 local SHA-256 9fbb7c316fb20ef94a0424f231881b5f0f24d86daf32418aadc1a92e94ae11ad, identique au premier rendu.
- Le validateur de sortie et le décodage complet sont exécutés avant le dépôt du MP4 final.

## Limites

Ce test a été effectué sur le même MacBook Pro, avec les outils et caches présents. Il ne prouve pas une installation fraîche des dépendances sur Linux, où la contre-revue a observé une erreur onnxruntime-node. Le MP4 historique reste volontairement non versionné ; la reconstruction génère un nouveau MP4. Les tests ne démontrent pas la recette perceptive humaine, l'autorité de l'approbation, ni le caractère obligatoire du chemin contrôlé dans les autres compositions.

**Décision : PASS pour le défaut de reproductibilité sur Mac, pas de promotion générale. FF-10 reste ouvert.** Aucun média diffusé.
