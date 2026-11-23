# FF-10 — Remontage successif après approbation humaine du texte

23 novembre 2026. Protocole figé dans SUCCESSIVE-EDIT-PROTOCOL.md, commit 0c391da.

**Verdict : PASS technique sur un remontage successif de deux rushes de test ; recette perceptive humaine du film UNVERIFIED.**

## Décision et modification

Texte approuvé par l'utilisateur : « Rush B : barres de couleur, audio témoin. ». La décision porte uniquement sur ce libellé, pas sur l'ensemble du film.

Nouvelle modification éditoriale distincte : augmenter la taille du texte du cartouche A de 30px à 32px, en conservant le fond #222222 et sans toucher au cartouche B ni à la transition.

## Preuves

- Le contrôle compare le bloc B et la transition à la référence de fixture dont l'empreinte SHA-256 est fixée ; il refuse les changements hors du bloc A.
- Scénario adversarial, changement du texte B : rejet protected_label-b_changed.
- Scénario adversarial, substitution de la référence : rejet approval_fixture_digest_mismatch.
- Rendu HyperFrames 0.8.33 sur copie isolée : PASS ; MP4 local de 9 secondes, SHA-256 2170ca70fa9f976dc4918d6cc5823c6cd98ea8b9d5e3f4c91c9967bbb266fa68.
- Décodage intégral du MP4 : PASS, effectué par le wrapper.
- Comparaison framemd5 FFmpeg des images décodées : 76 images du premier passage examinées, séquence différente ; 106 images du passage B examinées, séquence strictement identique au rendu précédent.
- Résultats structurés dans successive-qa.json et successive-ffprobe.json.

## Contre-revue statique ciblée

La comparaison visuelle par empreintes d'images établit que la modification ciblée a changé des pixels du premier passage et que les images sélectionnées du passage B sont inchangées. Elle ne prouve pas la lisibilité humaine des textes ni la qualité de la transition, qui restent à examiner. Le contrôle d'empreinte de référence reste dépendant d'une autorité externe fiable ; un agent capable de modifier la référence et l'empreinte peut contourner ce mécanisme.

Les deux rushes sont des mires expérimentales, pas des rushes éditoriaux réels. Le script reste expérimental et les autres chemins de rendu peuvent contourner le précontrôle. La validation du texte ne constitue pas une autorisation de diffusion.

## Décision

**PASS technique FF-10 pour la conservation d'une correction textuelle humaine au cours d'un remontage successif ciblé.** Ne pas clore FF-10 comme garantie produit générale ; il manque une recette perceptive humaine du film, une adoption explicite du chemin de rendu contrôlé et une preuve d'application aux rushes éditoriaux. Aucun média diffusé.
