# FF-10 — Intégration ciblée au rendu HyperFrames réel

Date : 23 novembre 2026. Référence du dépôt au départ : c2d83bc. Verdict : **PASS technique sur un chemin HyperFrames contrôlé ; protection générale NON DÉMONTRÉE.**

## Périmètre

Copie locale du projet FF-10 TodoMVC, 16,166 s. Rendu via HyperFrames 0.8.33, sans modification du projet source. Les médias sont réutilisés sans changement (empreintes dans input-qa.json). Les sous-titres HTML 2 et 3 sont protégés par comparaison exacte à la version témoin. Le sous-titre 1 n'autorise que le changement du fond #111 vers #222 ; mots, horaires et autres éléments restent identiques.

## Chemin exécuté

Le pilote guarded_hyperframes.py vérifie les blocs HTML et l'absence de changements hors périmètre **avant** d'invoquer la commande HyperFrames. Il contrôle les empreintes des médias et fichiers HTML avant/après, puis décode intégralement le MP4 produit.

- Adversarial : altération du texte du second sous-titre. Refus protected_caption2_changed avant le rendu, aucun MP4 adversarial.
- Autorisé : seul le fond du premier sous-titre change. Le contrôle accepte et lance réellement HyperFrames.
- HyperFrames : 485 images capturées, rendu de 16,2 secondes, exécution de 35,4 secondes. MP4 produit.
- ffprobe : voir ffprobe.json ; décodage FFmpeg intégral sans erreur.
- SHA-256 MP4 autorisé : 07e8dd7d237877a5c80d8210f6c69a2cb1ac1ceb56c139e7da93dae149e20324.
- Les quatre médias d'entrée sont inchangés par empreintes.

## Limites

1. Protection de la source HTML, pas preuve perceptive exhaustive : pas de comparaison de toutes les images ni recette humaine du nouveau MP4.
2. Pas de verrou humain formalisé : la composition témoin n'a pas été approuvée par l'utilisateur comme version finale verrouillée ; test d'un bloc protégé par protocole.
3. Contournement possible : appel direct à HyperFrames ; ce pilote ne rend pas le contrôle obligatoire dans tous les workflows.
4. Concurrence : l'empreinte avant/après détecte les modifications persistantes, mais le moteur lit les fichiers du projet ; une modification concurrente puis annulée pourrait échapper au contrôle.
5. Interruption et relance de ce chemin HyperFrames : non testées ici ; les tests antérieurs concernent un remux FFmpeg.
6. Droits et diffusion : média expérimental local ; aucune autorisation de diffusion inférée.

## Décision

**REUSE_EXISTING + EXPERIMENT.** Le chemin HyperFrames contrôlé fonctionne sur un projet réel, avec rejet avant rendu et MP4 vérifié techniquement. Ne pas clôturer FF-10 comme garantie générale. Prochain test discriminant : absence de contournement dans un workflow déclaré officiel et comportement sous interruption/concurrence, sans ajouter d'orchestrateur.
