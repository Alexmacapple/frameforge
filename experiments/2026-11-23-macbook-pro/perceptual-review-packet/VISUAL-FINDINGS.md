# FrameForge V3 — première contre-revue visuelle sur images extraites

Date : 23 novembre 2026. Source : `../vertical-v3/media/prototype-v3.mp4`. Support examiné : `contact-sheet.png` (8 images à 0,5, 1,6, 2,9, 3,8, 5,5, 6,5, 8,6 et 9,2 s). **Ce n'est pas une revue image par image de tout le film ni une écoute.**

## Constatations directement observées

| Point | Verdict | Preuve et limite |
| --- | --- | --- |
| Bandeau de calibration supprimé | **FAIL** | À 0,5 s, un grand bandeau rouge « SYNC » reste visible en haut de l'image. Il s'agit d'un marqueur technique inadapté à une vidéo publique. |
| Résultat 1 visible | **PASS ponctuel** | À 1,6 et 2,9 s, « Première tâche » figure dans la liste TodoMVC. |
| Résultat 2 visible | **PASS ponctuel** | À 3,8 et 5,5 s, « Première tâche » et « Deuxième tâche » figurent dans la liste. |
| Résultat 3 visible | **PASS ponctuel** | À 6,5, 8,6 et 9,2 s, « Première tâche » apparaît cochée et barrée ; « Deuxième tâche » reste non cochée. |
| Lisibilité des gestes | **À améliorer / UNVERIFIED** | La démonstration occupe une petite zone centrale dans une page comportant des colonnes et du contenu périphérique. Les états sont identifiables sur les images, mais la lisibilité à taille mobile et la compréhension du mouvement n'ont pas été testées. |
| Sous-titres incrustés | **Présence constatée** | Textes visibles dans la bande noire inférieure à 1,6, 3,8, 5,5 et 6,5 s. Les images tardives montrent une bande noire vide, ce qui correspond à la fin des sous-titres. |
| Confidentialité exhaustive | **UNVERIFIED** | Les images montrent une page de démonstration et des tâches fictives, sans secret évident sur ces échantillons ; toutes les images n'ont pas été contrôlées. |
| Narration, synchronisation perceptive, lecteur d'écran | **NOT RUN** | Aucun examen auditif indépendant ni test avec technologie d'assistance. |

## Décision

**FAIL de propreté visuelle de la V3** : retirer « SYNC » de la version de présentation. **NO-GO diffusion** en l'état.

Le prochain montage doit soit partir d'une capture sans marqueur, soit recadrer de façon à ne pas laisser le bandeau dans l'image. Un cadrage plus serré sur la zone TodoMVC est recommandé à titre d'hypothèse, avec contrôle que les trois actions et résultats restent visibles. Ne pas inventer des temps exacts de gestes en transférant les marqueurs d'une prise à une autre.

FF-06 et FF-08 restent ouverts. Ce document est une revue visuelle **partielle et traçable**, pas une validation audiovisuelle indépendante complète.
