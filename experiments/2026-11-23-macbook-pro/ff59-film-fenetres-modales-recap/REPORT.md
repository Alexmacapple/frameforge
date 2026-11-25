# Film des fenêtres modales avec récapitulatif animé (suite du ticket 59)

25 novembre 2026, MacBook Pro, branche `feature/insert-dans-le-film`. Même film que le 47, avec le schéma animé du ticket 59 en récapitulatif final. Le film 47 approuvé n'est pas modifié : les deux versions restent côte à côte, décision d'Alex du 25 novembre 2026.

## Verdict

- **Reproductible : PASS.** Deux rendus gardés donnent le même film, octet pour octet : `3720625a99a418023dce88720e4163f0f4bc776a8c3399ae251f32bf1ec71af6`.
- **Fiche : PASS** sur les quatorze contrôles ; restent les cinq points ouverts déclarés (écoutes humaines, lecteur d'écran).
- **Approbation : REVIEWED**, le 25 novembre 2026 à 17 h 29 (« oui il me convient »), consignée dans `EDITORIAL-APPROVAL.md` avec l'empreinte du film. Aucune autorisation de diffusion.

## Ce qui change par rapport au film 47

- Fiche en version 4 : sous-titres découpés (version 3) et une scène `recapitulatif` de type insert, après les sept scènes filmées. La capture s'arrête à 52,875 s ; l'insert occupe la fin, jusqu'à 66 s.
- Voix de l'insert : les trois clips de l'essai (`ff59-insert-anime`), séparés par 0,4 s de silence (`build_recap.py voice`, 10,825 s).
- Animation : `compositions/recapitulatif.html`, sous-composition générée par `build_recap.py insert` depuis la fiche.
- Les sept scènes filmées, la capture, son journal et les voix 1 à 7 sont ceux du film 47, aux mêmes instants.

## Mesures

- Brouillon témoin : 69 s de rendu ; rendus gardés : 70 s chacun.
- Premier essai du témoin bloqué par le disque plein (99 %) : HyperFrames estimait 16,4 Go de stockage temporaire pour 15,6 Go libres. Résolu en libérant de la place (cache npm, corbeille, `~/Claude.zip`), sans changer les options du garde.
- Deux contraintes de HyperFrames découvertes en chemin : une sous-composition se range dans `compositions/` (sinon elle passe pour une seconde entrée) ; chaque élément qui porte `data-composition-id` sans `data-no-timeline` doit inscrire sa timeline, sinon le rendu attend 45 s puis échoue.

## Limites

- Récapitulatif non écouté sans l'image ni comparé à ses sous-titres (#35, #36).
- Sous-titres de l'insert minutés au prorata des caractères, silences compris : léger décalage possible avec la voix.
- Reproductibilité mesurée sur ce Mac seulement.
