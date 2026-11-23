# Film d'essai de l'habillage version 2

23 novembre 2026, MacBook Pro. HyperFrames 0.8.33, FFmpeg 9.0.1. Relevé établi par un agent ; aucun visionnage humain du film rendu par le garde.

## Origine

Critique d'habillage du film de réservation, faite avec le skill Impeccable 4.8.0 (regard de designer sur sept images, détecteur automatique sur la page). Cinq défauts relevés ; Alex a demandé un nouvel habillage pour les prochains films seulement, puis a validé un essai fait à la main.

Défauts traités ici : action et sous-titres trop éloignés, bandeau noir collé au bord, film sans ouverture ni fin. Défauts laissés : pointeur posé sur les coins des cibles (enregistré dans la capture), message de confirmation peu visible (page filmée), police Arial.

## Ce film

Même capture et mêmes voix que le film de réservation approuvé, copiées sans changement. Seule la fiche diffère : `manifest_version` 2, `title`, `capture_zoom` 1,2, dernier sous-titre tenu jusqu'à 14,8 s.

- Film rendu par le garde : `media/room-booking-v2.mp4`, SHA-256 `5056a8bd55c6d61041a3c4b0bc00a178a8f883dc1539c75ac147dc3b85f849a5`, DRAFT.
- Fiche : 13 PASS, 4 UNVERIFIED, 0 FAIL.
- Deux rendus gardés successifs identiques à l'octet.
- Son identique à l'échantillon près à celui du film approuvé.
- Planche de six images regardée par l'agent : titre à 0,8 s, cartouche sous la carte, aucun sous-titre sur la page, carte entière dans le cadre.

## Films approuvés

Refaits avec l'outil modifié, par la vraie commande : réservation `9c834228…f543` et formulaire `ab040730…7125`, identiques à l'octet.

## Non vérifié

- Le film en mouvement, par une personne.
- Le rognage : à 1,2, seuls les 83 % du haut et du centre de la capture restent visibles. Ici la carte tient dedans, constaté à l'œil sur six images ; rien ne le mesure.
- Un titre contenant `&` ou `<` : la composition l'échappe, le contrôle compare le texte brut et refuserait.
- Lisibilité du cartouche sur une page filmée sombre : l'habillage suppose une page claire.
