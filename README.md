# FrameForge

Studio de production vidéo pilotable par agents, fondé sur HyperFrames, agent-browser et une recette audiovisuelle vérifiable.

## Statut
Expérimental, au 24 novembre 2026. Aucune chaîne de production n'est validée et aucune diffusion n'est autorisée.

- Trois films de démonstration web de quinze à seize secondes sont relus et approuvés en local. Les médias ne sont pas versionnés.
- Leurs outils communs sont dans `experiments/2026-11-23-macbook-pro/film-chain/` : contrôle de la fiche d'un film, générateur, garde de rendu, capture. Le mode d'emploi et les pièges constatés sont dans son `README.md`.
- L'état réel des expériences, ce qui reste ouvert et l'ordre de travail sont à la fin de `PLAN.md`.

## Objectif
Produire des démonstrations web narrées, puis étendre aux rushes et vidéos pédagogiques, avec traçabilité des sources, des captures et des validations.

## Principes
- Réutiliser HyperFrames pour la composition et le rendu.
- Employer agent-browser comme pilote privilégié, avec adaptateur interchangeable.
- Intégrer une narration audio-first, des voix locales avec cache et lexique, des sous-titres synchronisés et des contrôles qualité audiovisuels.
- Utiliser ShipGuard pour contrôler le code et les changements, pas comme moteur audiovisuel.
- Distinguer preuve observée, inférence, simulation et élément non vérifié.
- CLI et rapports textuels utilisables avec lecteur d'écran.

Voir WHY.md, INTENT.md, SPEC.md, PLAN.md et AGENTS.md.

## Licence

FrameForge est distribué sous licence [MIT](LICENSE). Copyright © 2026 Alexandra Guiderdoni.

## Brouillons et publication

Les agents peuvent produire des brouillons vidéo locaux. La diffusion exige un accord humain explicite sur la version et la destination ; un PASS technique ou éditorial ne vaut pas autorisation. Voir [PUBLICATION-POLICY.md](PUBLICATION-POLICY.md).
