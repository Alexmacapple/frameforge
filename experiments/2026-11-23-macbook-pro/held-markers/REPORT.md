# FrameForge — marqueurs avant/après maintenus 450 ms

23 novembre 2026, MacBook Pro Apple M2 Max. agent-browser 0.31.1, TodoMVC React avec données fictives.

## Hypothèse et protocole

Le test précédent perdait deux marqueurs très courts. Cette variante maintient chaque marqueur au moins 450 ms avant de passer à la commande suivante. Le WebM natif est à 10 images/s (vérifié avec ffprobe), les images sont extraites sans rééchantillonnage avec `ffmpeg -fps_mode passthrough`, puis le pixel du bandeau est comparé aux six couleurs attendues.

## Résultats

| Marqueur | Première image détectée | Images détectées |
| --- | ---: | ---: |
| Avant geste 1, rouge | 0,5 s | 4 |
| Après assertion 1, vert | 0,9 s | 22 |
| Avant geste 2, bleu | 3,1 s | 5 |
| Après assertion 2, jaune | 3,6 s | 20 |
| Avant geste 3, magenta | 5,6 s | 6 |
| Après assertion 3, cyan | 6,2 s | 20 |

Les trois assertions DOM sont positives. Capture WebM de 8,2 s, 82 images extraites. **PASS** pour la présence des six marqueurs dans cet essai, contre **FAIL** dans le précédent.

## Limites

- Une seule prise réussie : **répétabilité non démontrée**.
- La précision est limitée à la cadence de 10 images/s et au délai de propagation entre la commande et l'image effectivement enregistrée.
- Le marqueur après assertion prouve la chronologie de la vérification, mais ne constitue pas à lui seul une preuve que le résultat est lisible dans le plan.
- Les marqueurs recouvrent une partie de l'interface. Ils sont des artefacts d'instrumentation et ne doivent pas être conservés dans la vidéo destinée au public.
- Aucune V4 propre ni revue audiovisuelle indépendante réalisée ici.

## Décision

**REUSE_EXISTING + TARGETED_INSTRUMENTATION**. Un maintien de 450 ms a permis d'obtenir les six marqueurs sans nouvelle dépendance. Prochaine étape : reproduire le test sur une seconde prise, obtenir les repères et résultats sans superposition visible dans la version publique, puis vérifier narration, sous-titres, confidentialité et accessibilité. Ne pas clôturer FF-06/FF-08.
