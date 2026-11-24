# film-chain — outils communs aux films produits depuis une fiche

Créé le 23 novembre 2026 en regroupant ce que deux films partageaient : le formulaire (`ff10-second-web-demo-transfer/form-pilot-kokoro/`) et la réservation de salle (`ff04-room-booking-film/`). Statut expérimental : aucun de ces outils n'est une chaîne de production validée, et aucun n'autorise une diffusion.

## Contenu

- `check_manifest.py` : confronte la fiche d'un film (`provenance-manifest.json`) aux fichiers qu'elle cite. Code de sortie 0, 1 (au moins un FAIL) ou 2 (des UNVERIFIED).
- `build_from_fiche.py` : génère depuis la fiche la composition, les sous-titres SRT et VTT et la transcription. L'habillage est en dur et dépend de `manifest_version` : la version 1 garde le bandeau d'origine, octet pour octet ; la version 2 demande deux champs de plus dans `film`, `title` (titre d'ouverture, affiché sans être dit, repris en tête de la transcription) et `capture_zoom` (de 1 à 1,5, capture agrandie depuis le haut, le reste est rogné), et met les sous-titres en cartouche.
- `film_guard.py` : garde de rendu. Précontrôle des entrées figées, contrôle de la fiche, validation du film avant dépôt.
- `repin.py` : refige les empreintes d'un film après un changement voulu. `--check` n'écrit rien.
- `capture_lib.cjs` : navigateur, pointeur visible, horloge, journal et conversion des captures.
- `test_repin.py` : tests de `repin.py`.
- `test_capture_lib.py` : le dépôt d'une capture n'écrase rien et n'écrit rien à travers un lien, avec un faux navigateur et le vrai ffmpeg.
- `test_guard_main.py` : verdict, code de sortie et reçu de rendu du garde, sans média.
- `test_interruption.py` : l'arrêt d'un rendu ne laisse aucun processus en vie.
- `test_review_findings.py` : un test par constat corrigé de la revue du 23 novembre, sur une copie du film de réservation.
- `test_codex_findings.py` : un test par constat de la revue indépendante de Codex du 24 novembre (générateur qui écrasait une entrée, nom contenant `&`, mutants illisibles).
- `test_film_guard.py` : films trafiqués, précontrôle et forme du film, joués sur chaque film.
- `test_fiche_checks.py` : chaque motif de refus du contrôle de fiche, joué sur chaque film.
- `test_habillage_v2.py` : la version 1 génère les fichiers d'avant ; ce que la version 2 ajoute, motif par motif.
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
7. `python3 render_guarded.py`, puis `python3 repin.py DOSSIER --record-output`, puis rendre de nouveau. Le garde écrit un reçu à côté du film (`…mp4.receipt.json`, non versionné) : `--record-output` refuse un film sans reçu, ou dont une entrée a changé depuis le rendu. Dès que la fiche porte l'empreinte d'un film, le garde refuse tout rendu qui ne redonne pas ce film, fichier entier. Pour rendre de nouveau, déplacer d'abord le film existant ailleurs : le garde ne l'écrase pas.
8. Faire regarder et écouter le film ; consigner l'approbation avec son empreinte.

## Limites connues

Ces outils rattrapent des erreurs de manipulation. Ils ne résistent pas à quelqu'un qui prépare délibérément le terrain sur la machine. Décision d'Alex du 24 novembre 2026, après la seconde revue indépendante (issue 15) : les cas suivants sont connus et ne sont pas corrigés.

- **Fichier modifié entre deux lectures.** Si le fichier d'empreintes change entre le relevé du garde et son précontrôle, le reçu peut décrire d'autres entrées que celles contrôlées.
- **Processus qui s'échappe.** Un descendant du rendu qui change de session et efface le jeton de son environnement survit à l'arrêt du rendu.
- **Dossier remplacé pendant l'écriture.** Un sous-dossier ordinaire au moment du contrôle, remplacé par un lien avant l'écriture, redirige la génération ou la capture.
- **Cible de génération qui est une entrée figée.** Les fichiers générés sont eux-mêmes figés par empreinte : une fiche qui nomme comme transcription un autre fichier figé le fait réécrire, sauf s'il s'agit de la fiche, du fichier d'empreintes, d'un média, de la source ou du document d'approbation.

Deux refus sont volontaires : le générateur n'accepte qu'un nom écrit sous sa forme simple (`sortie.txt`, pas `./sortie.txt`), et `repin.py` n'accepte que des noms écrits en clair dans l'appel qui construit `GUARD`.

## Installer la voix de synthèse

Les clips de narration sont produits par Kokoro 0.9.4, voix `ff_siwis`, sur ce Mac et sans service distant. L'environnement Python n'est pas versionné ; il se reconstruit depuis `voice-requirements.txt`, qui fige 94 paquets avec leurs empreintes. Depuis la racine du dépôt :

```bash
uv venv .venv-voice --python 3.12
uv pip install --python .venv-voice/bin/python --require-hashes -r experiments/2026-11-23-macbook-pro/film-chain/voice-requirements.txt
```

Puis, pour synthétiser les phrases d'un film qui a son `synthesize_kokoro.py` :

```bash
HF_HUB_OFFLINE=1 .venv-voice/bin/python CHEMIN_DU_FILM/synthesize_kokoro.py
```

- `.venv-voice/` pèse environ 900 Mo et n'est pas suivi par Git. Jusqu'au 24 novembre 2026, l'environnement était dans `/tmp`, que macOS vide.
- Le modèle (`hexgrad/Kokoro-82M`) est lu dans le cache local de Hugging Face. Sur une machine neuve, lancer une première fois sans `HF_HUB_OFFLINE=1` pour le télécharger.
- `voice-requirements.txt` est figé pour Python 3.12 sur macOS Apple Silicon (macOS 14 ou plus récent, exigence de `torch`).
- Vérifié le 24 novembre 2026 en resynthétisant hors film les trois phrases de la réservation : deux clips sur trois ressortent identiques à l'octet aux clips approuvés, le premier diffère, comme avant la réinstallation. Un clip approuvé ne se resynthétise donc pas : il se conserve.

## Pièges constatés

- **Les médias figés n'existent qu'en un exemplaire local.** Une capture, un clip ou un film n'est pas versionné : l'écraser, c'est perdre le film approuvé. `capture_lib.cjs` refuse d'écraser une capture existante ; pour un essai, définir `FF_CAPTURE_OUT`. Une copie des médias des trois films approuvés est conservée hors dépôt, sur le même Mac, dans `~/Claude-worktrees/frameforge-medias-approuves/`, avec ses empreintes ; elle est à refaire après chaque nouvelle approbation.
- **Refiger n'est pas approuver.** `repin.py` rend cohérentes des empreintes ; il ne dit pas que le changement est voulu. Relire ce qu'il affiche avant de commiter.
- **Une nouvelle synthèse de voix peut donner un autre son**, même avec une graine fixe. Elle demande une nouvelle écoute.
- **Un résultat qui se fait attendre se date avec `appear`, pas avec `locator.waitFor`.** L'attente de Playwright espace ses essais jusqu'à une demi-seconde : le journal datait le résultat de 0,3 à 0,5 s trop tard. `appear(sélecteur)`, fourni à `play`, relit la page à chaque image. Un résultat qui suit aussitôt un clic n'est pas concerné.
- **Un film approuvé sans journal de capture lisible est en échec.** Pour un brouillon, c'est un manque (UNVERIFIED) ; dès que la fiche dit `REVIEWED` ou `APPROVED_FOR_RELEASE`, c'est un FAIL du contrôle `statuses` : rien ne prouve ce que le film dit avoir observé. Décision du 24 novembre 2026 (issue 15). Le film V5 (`ff10-web-workflow-entrypoint/local`), approuvé à l'écoute avec un journal dans un autre format, est dans ce cas : sa fiche répond FAIL tant que sa capture n'est pas refaite avec `capture_lib.cjs`.
- **Le garde d'un film nomme ses fichiers en clair.** `repin.py` lit `pins_ref`, `reference_ref` et `output` dans l'appel qui construit `GUARD`, sans exécuter le fichier : un nom passé par une variable est refusé.
- **Rien n'est écrit à travers un lien symbolique.** Le générateur et la capture refusent un fichier ou un sous-dossier qui est un lien, et un nom qui sort du dossier du film.
- **Un film présent sans son reçu de rendu bloque le rendu suivant.** Cela arrive si le rendu est arrêté entre le dépôt du film et l'écriture du reçu. Le garde répond `…_output_without_receipt` : déplacer le film ailleurs, puis rendre de nouveau.
- **Aucun contrôle automatique ne voit un pointeur qui masque un résultat.** Regarder une planche d'images de la capture.
