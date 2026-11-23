# FF-08 — Revue ciblée du film V3 recadré (version fixée)

**Date :** 23 novembre 2026  
**Source exacte :** `../vertical-v3-reframed/media/reframed.mp4`  
**SHA-256 :** `8f9d069313b3973cd8e48b54f2e5fabd764e08335d9f47c84434ce21cb5b5075`  
**Statut :** PARTIAL — NO-GO diffusion, revue humaine à compléter.

## Objectif de compréhension

1. Une première tâche est ajoutée et visible.
2. Une deuxième tâche est ajoutée et les deux tâches sont visibles.
3. La première tâche est terminée, cochée et barrée, tandis que la seconde reste active.

## Contrôles exécutés

- FFprobe : MP4 **9,500 s**, **1920 × 1080**, **30 fps**, piste **AAC stéréo**.
- FFmpeg : décodage de **285 images**. Le script `inspect_frames.py` examine chaque image redimensionnée (480 × 270) à la recherche d'une grande zone rouge dans les 80 % supérieurs et d'une image totalement noire : **aucune occurrence**. **Limite :** détection heuristique de grandes zones, pas inspection humaine de tous les pixels.
- Une planche de **29 images échantillonnées à 3 images/s** (`overview-3fps.png`) a été examinée visuellement.
- Images échantillonnées : premier résultat visible vers **1,33 s** ; deuxième résultat vers **3,67 s** ; première tâche cochée/barrée vers **6,33 s**. Ces instants sont des bornes d'échantillonnage, **pas** les timestamps exacts d'événements.
- La planche ne montre pas le grand bandeau rouge « SYNC » et présente les trois états attendus. Le cadrage coupe des éléments périphériques de la page ; il faut juger sa lisibilité au format de diffusion cible.
- Les sous-titres incrustés sont visibles pendant les phrases sur la planche. Le fichier SRT distinct est disponible dans `../vertical-v3-reframed/captions.srt`. La comparaison antérieure a relevé des fins de sous-titres incrustés légèrement différentes du SRT : la concordance perceptive doit être vérifiée dans le lecteur cible.

## Examen sans image : ce qui est démontré et ce qui ne l'est pas

La transcription fournie contient exactement :

1. « Nous ajoutons une première tâche. »
2. « Nous ajoutons ensuite une deuxième tâche. »
3. « Enfin, nous terminons la première tâche. »

**Analyse du texte, pas de l'écoute :** le scénario verbal donne la séquence des actions, mais ne dit pas explicitement « la première tâche apparaît dans la liste », « deux tâches sont maintenant visibles » ou « la première tâche est cochée et barrée ». Pour une personne sans vision, l'état final et la confirmation du résultat restent donc insuffisamment explicites **dans le texte**. Il s'agit d'une **lacune éditoriale potentielle**, pas d'un résultat de test utilisateur.

**NOT RUN :** écoute humaine indépendante de l'audio, comparaison mot à mot de la voix effectivement prononcée avec le SRT, compréhension par une personne qui ne connaît pas le scénario, essai avec VoiceOver dans le lecteur cible, inspection exhaustive des données sensibles dans audio/vidéo/métadonnées, vérification des droits de diffusion.

## Verdict par objectif

| Objectif | Statut | Justification |
| --- | --- | --- |
| MP4 décodable, pistes présentes | PASS technique | 285 images, métadonnées et contrôles antérieurs |
| Trois résultats présents visuellement | PASS sur échantillons | États visibles dans la planche à 3 fps |
| Absence du grand bandeau rouge | PASS au détecteur + échantillons | Heuristique sur 285 images, inspection de 29 |
| Compréhension des trois résultats sans vision | UNVERIFIED / risque éditorial | Texte décrit les actions, pas les confirmations d'état |
| Concordance voix prononcée / SRT | UNVERIFIED | Aucune écoute ni ASR validée |
| Compréhension visuelle par tiers | UNVERIFIED | Aucune revue indépendante du film en lecture réelle |
| Accessibilité du lecteur et du film | UNVERIFIED | Aucun test VoiceOver exécuté |
| Confidentialité et droits exhaustifs | UNVERIFIED | Aucun contrôle complet de diffusion |
| Respect de la cible initiale ~30 s | NOT MET pour cette variante | Le candidat dure 9,5 s ; il reste un prototype court |

## Décision et prochain test

**NO-GO diffusion / FF-08 reste ouvert.** Ne pas inventer un PASS de revue perceptive. La prochaine étape sans nouveau code est une **séance indépendante sur le MP4 identifié par son SHA** :

1. **Sans image** : écouter le film une fois, puis demander à la personne de restituer les trois actions **et leurs résultats** sans lui donner le transcript.
2. **Avec image** : regarder le film entier au format de destination ; relever tout geste ou résultat illisible et les instants problématiques.
3. **Sous-titres** : lire le SRT externe dans le lecteur cible ; comparer chaque mot et les sons pertinents à l'audio.
4. **Confidentialité et droits** : examiner le lot de livraison complet, y compris les métadonnées et les médias originaux.
5. Consigner chaque observation comme PASS, FAIL ou UNVERIFIED avec son horodatage. Corriger le texte ou le cadrage avant de construire un nouveau composant.

Aucune nouvelle capture, aucun nouveau moteur, aucun seuil ±250 ms déclaré atteint.
