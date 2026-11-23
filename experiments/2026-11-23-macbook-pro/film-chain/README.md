# film-chain — outils communs aux films produits depuis une fiche

Créé le 23 novembre 2026 en regroupant ce que deux films partageaient : le formulaire (`ff10-second-web-demo-transfer/form-pilot-kokoro/`) et la réservation de salle (`ff04-room-booking-film/`). Statut expérimental : aucun de ces outils n'est une chaîne de production validée, et aucun n'autorise une diffusion.

## Contenu

- `check_manifest.py` : confronte la fiche d'un film (`provenance-manifest.json`) aux fichiers qu'elle cite. Code de sortie 0, 1 (au moins un FAIL) ou 2 (des UNVERIFIED).
- `build_from_fiche.py` : génère depuis la fiche la composition, les sous-titres SRT et VTT et la transcription. L'habillage est en dur, commun aux deux films.
- `film_guard.py` : garde de rendu. Précontrôle des entrées figées, contrôle de la fiche, validation du film avant dépôt.
- `repin.py` : refige les empreintes d'un film après un changement voulu. `--check` n'écrit rien.
- `capture_lib.cjs` : navigateur, pointeur visible, horloge, journal et conversion des captures.
- `test_repin.py` : tests de `repin.py`.
- `test_film_guard.py` : films trafiqués, précontrôle et forme du film, joués sur chaque film.
- `test_fiche_checks.py` : chaque motif de refus du contrôle de fiche, joué sur chaque film.
- `mutation_check.py` : supprime chaque contrôle l'un après l'autre et signale ceux dont aucun test ne s'aperçoit. À relancer après tout ajout de contrôle ; il dure quelques minutes et ne modifie rien dans le dépôt.

Les tests propres à un film (gestes, fichiers générés) restent dans son dossier.

## Ce qui reste propre à chaque film

Sa fiche, sa page filmée, ses gestes (`capture.cjs`), ses clips de voix, son fichier d'empreintes, son `render_guarded.py` réduit à ses paramètres, et ses tests.

## Fabriquer un film neuf, dans l'ordre

1. Écrire la fiche avec les phrases, statut `DRAFT`, sans empreinte de film.
2. Produire les clips de narration et mesurer leurs durées.
3. Poser les repères dans la fiche, puis `python3 build_from_fiche.py CHEMIN_DE_LA_FICHE`.
4. Écrire `capture.cjs` et capturer.
5. Écrire le fichier d'empreintes et le `render_guarded.py` du film, puis `python3 repin.py DOSSIER`.
6. Rendre un brouillon témoin, le qualifier, écrire la référence de sortie, refiger.
7. `python3 render_guarded.py`, puis `python3 repin.py DOSSIER --record-output`, puis rendre de nouveau. Dès que la fiche porte l'empreinte d'un film, le garde refuse tout rendu qui ne redonne pas ce film, fichier entier. Pour rendre de nouveau, déplacer d'abord le film existant ailleurs : le garde ne l'écrase pas.
8. Faire regarder et écouter le film ; consigner l'approbation avec son empreinte.

## Pièges constatés

- **Les médias figés n'existent qu'en un exemplaire local.** Une capture, un clip ou un film n'est pas versionné : l'écraser, c'est perdre le film approuvé. `capture_lib.cjs` refuse d'écraser une capture existante ; pour un essai, définir `FF_CAPTURE_OUT`. Une copie des médias des trois films approuvés est conservée hors dépôt, sur le même Mac, dans `~/Claude-worktrees/frameforge-medias-approuves/`, avec ses empreintes ; elle est à refaire après chaque nouvelle approbation.
- **Refiger n'est pas approuver.** `repin.py` rend cohérentes des empreintes ; il ne dit pas que le changement est voulu. Relire ce qu'il affiche avant de commiter.
- **Une nouvelle synthèse de voix peut donner un autre son**, même avec une graine fixe. Elle demande une nouvelle écoute.
- **Aucun contrôle automatique ne voit un pointeur qui masque un résultat.** Regarder une planche d'images de la capture.
