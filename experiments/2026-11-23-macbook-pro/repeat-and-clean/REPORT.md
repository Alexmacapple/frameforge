# FrameForge — deuxième prise instrumentée et prise propre

Date : 23 novembre 2026. MacBook Pro Apple M2 Max, agent-browser 0.31.1, TodoMVC React, données fictives.

## Test A — répétabilité des marqueurs

Une seconde prise avec maintien de 450 ms a produit un WebM de 8,0 s à 10 images/s. Les trois gestes et assertions DOM ont réussi.

| Marqueur | Prise A (s) | Prise B (s) |
| --- | ---: | ---: |
| Avant 1 | 0,5 | 0,5 |
| Après 1 | 0,9 | 0,8 |
| Avant 2 | 3,1 | 2,9 |
| Après 2 | 3,6 | 3,3 |
| Avant 3 | 5,6 | 5,4 |
| Après 3 | 6,2 | 5,6 |

Les six marqueurs de la prise B ont été détectés sur les images natives : 3, 21, 4, 21, 2 et 24 images respectivement. **PASS de présence sur deux prises**, mais la variation des durées et le faible nombre d'images pour certains marqueurs ne justifient pas une précision universelle.

## Test B — capture propre sans marqueurs

Nouvelle session TodoMVC et données fictives. Trois gestes et assertions DOM réussis. WebM muet de **5,7 s**, 57 images à 10 images/s, sans bandeaux injectés. Les changements visuels dominants de la capture propre apparaissent approximativement à **0,7 s**, **2,4 s** et **4,0 s**, avec une variation à **5,5 s** qui n'a pas été qualifiée. Ces différences d'images ne prouvent pas seules l'identité du geste.

**Point de méthode :** les marqueurs de la prise instrumentée et les images de la prise propre appartiennent à des exécutions différentes. Leurs temps ne sont **pas transférables** l'un à l'autre. Les assertions DOM de la prise propre sont des preuves de résultat, pas des horodatages vidéo exacts.

## Décision

- **PASS** : répétabilité limitée à deux prises instrumentées, six marqueurs visibles, trois résultats DOM observés sur la prise propre.
- **UNVERIFIED** : alignement précis des événements avec la capture propre, qualité audiovisuelle d'une version narrée propre, contrôle de confidentialité image par image et revue indépendante.
- **NO-GO** pour déclarer FF-06/FF-08 terminées ou publier un film comme validé.
- **REUSE_EXISTING** pour le moteur ; la prochaine décision porte sur une instrumentation *non intrusive* de la prise finale ou sur une méthode de calibration démontrée, pas sur un nouveau skill.
