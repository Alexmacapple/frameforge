# FF-04 — Proposition de fiche de film (manifeste de provenance)

23 novembre 2026, MacBook Pro. **Statut : format validé par Alex, éprouvé sur deux films, et lu par le rendu gardé du formulaire.** Les sections ci-dessous sont dans l'ordre où le travail a été fait.

## Ce que c'est

Un fichier unique par film, `form-pilot-kokoro/provenance-manifest.json`, qui relie chaque scène à son geste, à son résultat observé, à sa phrase et à ses repères. Exemple fourni : le film du formulaire, trois scènes, trois gestes.

Au sens du glossaire, c'est un manifeste de provenance : il ne constitue pas une preuve. `check_manifest.py` le confronte aux fichiers qu'il cite.

## Ce que la fiche contient

- **Film** : identifiant, durée, composition, transcription, fichiers de sous-titres, film produit et son empreinte, statut d'approbation et document qui le porte, contrôles restés ouverts.
- **Source** : page filmée et son empreinte, autorisation, date de capture.
- **Capture** : vidéo capturée et journal des événements horodatés.
- **Scène** : identifiant, type de plan, gestes, résultat attendu et événement qui le montre, phrase de narration avec son clip et son créneau, sous-titre, statut de preuve.

Les empreintes des médias ne sont pas recopiées : la fiche renvoie au fichier d'empreintes du garde (`pins_ref`), et tout média cité doit y figurer.

## Ce que le contrôle vérifie

Treize contrôles, chacun PASS, FAIL ou UNVERIFIED :

- `schema` : aucun champ inconnu, aucun champ manquant. Un champ sans contrôle qui le lit est refusé.
- `source` : page présente, empreinte identique, autorisation renseignée, date valide.
- `pinned_media` : tout fichier cité est figé par le garde.
- `texts` : narration, transcription, SRT et VTT portent le même texte.
- `captions` : repères des sous-titres identiques dans la fiche et dans les fichiers.
- `composition` : clips, débuts et durées identiques à la composition HyperFrames.
- `timeline` : pas de chevauchement de narration, rien après la fin du film, chaque sous-titre encadre sa phrase.
- `gestures` : gestes présents dans la capture, dans l'ordre, et résultat affiché pendant le sous-titre qui l'annonce.
- `results` : résultat relu dans le DOM égal au résultat attendu.
- `statuses` : statuts connus ; un film REVIEWED ne contient que des scènes observées.
- `approval` : le document d'approbation nomme l'empreinte du film et le statut.
- `measured_audio` : durée réelle de chaque clip proche de son créneau ; UNVERIFIED si le clip est absent.
- `output_film` : empreinte du film local ; UNVERIFIED si le film est absent.

Les contrôles restés ouverts sont rapportés UNVERIFIED, jamais PASS. Code de sortie : 0 tout passe, 1 au moins un FAIL, 2 aucun FAIL mais des UNVERIFIED.

## Preuves exécutées

- Fiche du formulaire : 13 PASS, 2 UNVERIFIED (compréhension sans l'image, conformité de la voix au texte), code de sortie 2.
- 14 tests sur 14 dans `test_manifest.py`. Avant l'ajout des champs de références à la fiche, 13 échouaient.
- Chaque contrôle a un test qui le fait échouer : champ inconnu, texte modifié, début de narration décalé, repère de sous-titre modifié, résultat affiché avant son annonce (le défaut de l'ancien film), résultat attendu faux, média non figé, scène non vérifiée dans un film approuvé, empreinte de film non approuvée, narrations qui se chevauchent, source modifiée.
- Sans les médias locaux, le contrôle répond UNVERIFIED et non PASS (testé sur une copie sans clips ni film).

## Critères de l'issue FF-04

- **Schéma minimal et exemple à trois gestes** : proposés.
- **Validation des références, durées et états non vérifiés** : couverte par le contrôle.
- **Aucun champ sans consommateur** : imposé par le contrôle `schema`.
- **Types de plans** (`fixed`, `continuous_action`, `title_card`, `honest_cut`, `result`) : la liste est acceptée, mais seul `continuous_action` est exercé par l'exemple. Les règles propres aux autres types ne sont pas écrites.
- **Fraîcheur, version du produit, rôle et session** : date de capture, empreinte de la page et autorisation en texte libre. Pas de notion de rôle ni de session : la fixture n'en a pas.

## Essai sur un second film

Format validé par Alex le 23 novembre 2026, puis éprouvé sur le film V5 (TodoMVC, `9fbb7c31…11ad`) : fiche dans `ff10-web-workflow-entrypoint/local/provenance-manifest.json`.

Le film V5 ne rentrait pas tel quel. Trois écarts réels, et la réponse retenue :

- **Source publique sans empreinte.** La page filmée est un site en ligne, pas un fichier du dépôt. `sha256` peut valoir `null` ; le contrôle `source` répond alors UNVERIFIED.
- **Aucun repère de geste aligné sur le film.** La capture a été ralentie d'un facteur 1,7 et son journal (`vertical-v3/events.json`) est dans un autre format, sur une autre horloge. `events_ref` et l'événement de résultat peuvent valoir `null` ; `gestures` et `results` répondent UNVERIFIED.
- **Composition et approbation.** Le fichier d'empreintes de V5 ne couvre pas la composition, et son document d'approbation ne contient pas le mot `REVIEWED`. Le contrôle n'exige plus que la composition soit figée (son contenu reste confronté à la fiche) et n'exige le statut en toutes lettres que pour une autorisation de diffusion.

Règle supprimée : « une action continue sans geste est un échec ». Une scène sans repère mesuré est désormais rapportée UNVERIFIED.

Résultat sur V5 : 10 PASS, 3 UNVERIFIED de contrôle (`source`, `gestures`, `results`) et 4 contrôles ouverts, code de sortie 2. Résultat inchangé sur le formulaire : 13 PASS, 2 UNVERIFIED. 17 tests sur 17 dans `test_manifest.py` ; les 17 tests du pilote V5 passent toujours.

Ce que l'essai montre : le film V5, approuvé à l'écoute, a des preuves plus faibles que le film du formulaire. Ses trois résultats sont bien consignés dans le DOM de la capture d'origine, mais rien ne mesure quand ils apparaissent dans le film. La fiche le rend visible au lieu de le masquer.

## Branchement sur le rendu gardé du formulaire

Décidé par Alex le 23 novembre 2026. Le précontrôle de `form-pilot-kokoro/render_guarded.py` lance le contrôle de la fiche et refuse le rendu si un contrôle est en échec (`kokoro_fiche_incoherent`). Les UNVERIFIED déclarés ne bloquent pas. La fiche et le journal de capture sont ajoutés aux fichiers figés par empreinte.

- **Refus sur le chemin réel** : fiche modifiée (troisième phrase avancée à 9 s) avec des empreintes remises à jour, puis `python3 render_guarded.py` : `kokoro_fiche_incoherent:composition,timeline`, code 2, aucun film déposé. État restauré ensuite.
- **Cas nominal** : rendu gardé PASS, même empreinte `ab040730…7125` que le film approuvé.
- **Tests** : 13 dans `test_kokoro_guard.py`, 32 avec la fiche et les gestes. Le refus neutralisé fait échouer `test_incoherent_fiche_blocks_preflight`.

Portée : ce pilote seulement. Le pilote V5 a une fiche mais son rendu ne la lit pas. La fiche est relue dans le projet d'origine même quand le précontrôle est rejoué sur la copie isolée, parce qu'elle renvoie à des documents voisins ; les empreintes garantissent que la copie porte la même fiche.

## La fiche comme seule source des fichiers texte

Décidé par Alex le 23 novembre 2026, sur plan soumis. `form-pilot-kokoro/build_from_fiche.py` génère depuis la fiche la composition `index.html`, `captions.srt`, `captions.vtt` et `transcript.txt`. Le précontrôle du rendu refuse si un de ces fichiers n'est pas celui que la fiche génère (`kokoro_files_not_generated_from_fiche`).

- **Rien ne change pour le film approuvé** : les quatre fichiers générés ont exactement les empreintes relevées avant l'écriture du générateur (`4fd5bd62…`, `9124ff26…`, `8e78df3d…`, `9d60690f…`). Le rendu gardé redonne le film `ab040730…7125`.
- **Une modification de la fiche se propage** : phrase changée dans une copie de la fiche, les quatre fichiers générés portent la nouvelle phrase ; repère changé, SRT, VTT et composition suivent.
- **Refus sur le chemin réel** : taille du texte des sous-titres retouchée à la main dans `index.html`, empreintes remises à jour, puis `python3 render_guarded.py` : `kokoro_files_not_generated_from_fiche:index.html`, code 2, aucun film déposé. État restauré ensuite. Le contrôle de cohérence seul ne voyait pas cette retouche, qui ne touche ni texte ni repère.
- **Tests** : 6 dans `test_build_from_fiche.py`, 38 avec le garde, les gestes et la fiche. Le refus neutralisé fait échouer un test.

Hors de cette étape : le plan de capture (instants des clics) reste écrit à la main dans `capture.cjs` ; l'habillage du film reste dans le générateur, propre à ce film ; le pilote V5 n'est pas concerné.

## Limites

- Le format est tiré de deux démonstrations web. Il n'a pas été essayé sur un montage de rushes.
- Les statuts de preuve des scènes V5 sont déclarés `observed` d'après le journal d'origine, que le contrôle ne relit pas.
- Les repères des gestes viennent de l'horloge du script de capture, pas d'une mesure sur l'image ; l'écart constaté sur cette prise est d'environ 0,01 s.
- L'autorisation est un texte libre : le contrôle vérifie qu'elle est renseignée, pas qu'elle est vraie.
- La fiche génère les fichiers texte du film du formulaire, pas sa capture : les instants des gestes restent écrits à la main dans `capture.cjs`, et la fiche ne les contient pas.
- Le générateur n'a été essayé que sur ce film. Son habillage est en dur ; un second film demanderait de le dupliquer ou de le paramétrer, ce qui n'est pas décidé.
