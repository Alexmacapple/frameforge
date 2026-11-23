# FrameForge — essai de repères vidéo explicites

23 novembre 2026, MacBook Pro Apple M2 Max, agent-browser 0.31.1, TodoMVC React public, données fictives.

## Question

Les horloges du journal des commandes et de la capture vidéo peuvent-elles être rapprochées sans déduire les gestes de changements d'images ambigus ?

## Protocole

Après `record start`, injecter un bandeau fixe en haut de la page, changer sa couleur avant les trois actions, puis enregistrer pour chaque marqueur le temps monotone de demande et de retour. Exécuter trois gestes et assertions DOM. Extraire la vidéo à 10 images/s et lire le pixel au centre du bandeau ; détecter les transitions entre six couleurs connues.

## Observations

| Événement | Monotone depuis demande record (s) | Vidéo (s) |
| --- | ---: | ---: |
| Rouge, calibration | 1,977 | 0,8 |
| Vert, début parcours | 2,734 | 1,2 |
| Bleu, avant action 1 | 3,397 | 1,5 |
| Jaune, avant action 2 | 5,602 | 3,4 |
| Magenta, avant action 3 | 7,779 | 5,0 |
| Cyan, fin parcours | 10,053 | 6,5 |

Le WebM VP8 dure **7,2 secondes**. Les trois assertions DOM ont réussi (une tâche, deux tâches, première terminée). Le journal contient les temps monotones de commande, retour et vérification.

## Interprétation et limites

- Les marqueurs **visibles et étiquetés** fournissent des repères dans le média lui-même. Ils sont moins ambigus que les seules différences visuelles de TodoMVC.
- Les écarts journal → vidéo varient : les temps de marqueur ne sont **pas** reliés par un offset constant. L'enregistrement de la vidéo et l'horloge du shell ne doivent pas être confondus.
- Granularité de mesure vidéo : **0,1 seconde**. Les instants relevés sont les premières images échantillonnées où la couleur apparaît ; ils ne prouvent pas une précision à la frame d'origine.
- Un marqueur posé **avant** le geste situe le début de la séquence, **pas** l'apparition du résultat métier. Le résultat reste démontré séparément par l'assertion DOM. Une future prise peut utiliser deux marqueurs par geste (début et résultat vérifié).
- Les bandeaux colorés sont une instrumentation d'essai et **ne doivent pas être conservés tels quels dans une vidéo destinée au public**.
- Pas de démonstration que cette instrumentation est native à agent-browser ; c'est un script expérimental minimal. Pas de nouvelle dépendance ni de skill.

## Décision

**REUSE_EXISTING + TARGETED_INSTRUMENTATION** : les outils existants suffisent pour filmer et rendre ; le besoin résiduel est de relier les observations métier aux images avec des marqueurs explicitement identifiables. Ne pas construire d'orchestrateur ni d'adaptateur générique. Pour FF-06, tester les marqueurs *avant action* et *après assertion*, puis vérifier leur suppression ou masquage dans la version finale. FF-08 reste non validée (écoute, lisibilité, confidentialité, contre-revue humaine).
