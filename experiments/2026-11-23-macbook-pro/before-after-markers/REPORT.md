# FrameForge — contre-exemple : marqueurs avant/après trop rapides

23 novembre 2026, MacBook Pro M2 Max, agent-browser 0.31.1, TodoMVC React avec données fictives.

## Objectif

Poser un marqueur visuel distinct **avant chaque geste** et **après vérification du résultat**, pour obtenir six repères et les relier à trois assertions DOM.

## Exécution

Les trois gestes ont réussi : ajout de deux tâches puis achèvement de la première. Le journal `events.json` conserve les temps monotones des appels et les états DOM observés. Capture WebM décodable de **4,3 secondes**.

Les marqueurs ont été détectés par lecture du pixel au centre du bandeau, sur une extraction de la vidéo à **10 images/s**.

| Marqueur | Résultat dans les images extraites |
| --- | --- |
| Avant geste 1, rouge | **ABSENT** |
| Après assertion 1, vert | Visible vers 0,5 s |
| Avant geste 2, bleu | **ABSENT** |
| Après assertion 2, jaune | Visible vers 1,6 s |
| Avant geste 3, magenta | Visible vers 2,9 s |
| Après assertion 3, cyan | Visible vers 3,0 s |

Le journal indique pourtant que les six commandes de marqueur ont retourné un succès. Les deux marqueurs absents ont été remplacés trop rapidement pour apparaître dans les images extraites. La cadence native du WebM n'a pas été contrôlée indépendamment dans cet essai ; on ne peut donc pas attribuer avec certitude l'absence au seul échantillonnage à 10 Hz.

## Verdict

**FAIL pour la garantie six marqueurs visibles** ; **PASS pour les trois actions et assertions DOM**. Ne pas considérer une commande d'instrumentation réussie comme la preuve que son marqueur est enregistré.

## Suite discriminante

Tester soit une durée minimale de maintien du marqueur validée sur le média, soit une capture native des événements associée à une synchronisation explicite des images. Vérifier le résultat à la cadence native et éviter que les marqueurs cachent l'interface. Ensuite seulement réaliser un montage propre et une revue audiovisuelle indépendante. Aucun skill ni orchestrateur justifié.
