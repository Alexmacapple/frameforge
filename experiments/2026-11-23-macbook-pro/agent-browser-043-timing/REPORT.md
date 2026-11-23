# FrameForge — agent-browser 0.43.0, repères à 30 images/s

Date : 23 novembre 2026. MacBook Pro M2 Max. Version 0.43.0 exécutée via `npx --package` sans remplacer l'installation globale 0.31.1. TodoMVC React public, données fictives.

## Protocole

Enregistrer à 30 fps avec `--contact-sheet`, placer un bandeau de couleur avant chaque action et après son assertion DOM, journaliser les instants monotones des commandes, puis décoder **toutes** les images natives du WebM sans rééchantillonnage. Les six couleurs sont détectées par lecture d'un pixel au centre du bandeau.

## Résultats

WebM de **7,600 s**, **228 images à 30 fps**, 232695 octets. Feuille de contact native de neuf images. Trois actions et trois assertions DOM réussies.

| Repère | Première image vidéo (s) | Retour commande depuis demande de record (s) |
| --- | ---: | ---: |
| Avant 1 | 0,933 | 1,341 |
| Après assertion 1 | 2,467 | 2,843 |
| Avant 2 | 3,500 | 3,768 |
| Après assertion 2 | 4,833 | 5,236 |
| Avant 3 | 5,700 | 6,061 |
| Après assertion 3 | 6,800 | 7,177 |

Les six couleurs sont détectées sur respectivement 46, 31, 40, 26, 33 et 24 images. Les décalages entre retour de commande et première image varient : **un offset constant n'est pas démontré**. Le début de l'action et le résultat métier sont encadrés par les marqueurs, mais ces marqueurs ne prouvent pas l'instant exact où le résultat devient visible.

## Critère de précision à arbitrer

La cadence de 30 fps donne un pas d'échantillonnage d'environ 33 ms ; **ce n'est pas une précision d'alignement garantie**. Une tolérance éditoriale de l'ordre de 200 à 250 ms pourrait être évaluée sur des scènes explicatives, mais elle n'est pas un critère validé. Pour prouver une tolérance, il faut une référence temporelle indépendante et des mesures répétées.

## Comparaison

- agent-browser 0.31.1 : captures d'écran toutes les 100 ms et pipe FFmpeg à 10 fps, sans horodatages de capture transmis à l'encodeur.
- agent-browser 0.43.0 : capture screencast 30 fps, feuille de contact, gestion des frames améliorée, mais **aucun export natif de correspondance image ↔ événement DOM démontré**.
- La version 0.43.0 améliore la granularité et la visibilité des marqueurs, sans lever seule la question de synchronisation.

## Décision

**REUSE_EXISTING / EXP** : préférer tester le mécanisme 0.43.0 avant toute couche propre. **BUILD_MINIMAL non justifié à ce stade**. Ne pas ajouter de skill ni d'orchestrateur. Pour FF-06 : déterminer un seuil métier de synchronisation et une méthode de vérification indépendante. Pour FF-08 : revoir réellement le film, la narration, les alternatives, la confidentialité et l'accessibilité. Aucun de ces deux tickets ne doit être clôturé à ce stade.
