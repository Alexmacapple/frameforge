# FF-04 — Proposition de fiche de film (manifeste de provenance)

23 novembre 2026, MacBook Pro. **Statut : proposition, en attente de validation du format par Alex. Rien n'en dépend encore : le rendu gardé ne lit pas la fiche.**

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

## Limites

- Le format est tiré d'un seul film. Il n'a pas été essayé sur le film V5 ni sur un montage de rushes.
- Les repères des gestes viennent de l'horloge du script de capture, pas d'une mesure sur l'image ; l'écart constaté sur cette prise est d'environ 0,01 s.
- L'autorisation est un texte libre : le contrôle vérifie qu'elle est renseignée, pas qu'elle est vraie.
- La fiche n'est lue par aucun autre outil. La brancher sur le rendu gardé ou générer la composition depuis elle sont des décisions à prendre après validation du format.
