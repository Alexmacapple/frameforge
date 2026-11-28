# film-chain — outils communs aux films produits depuis une fiche

Créé le 23 novembre 2026 en regroupant ce que deux films partageaient : le formulaire (`ff10-second-web-demo-transfer/form-pilot-kokoro/`) et la réservation de salle (`ff04-room-booking-film/`). Statut expérimental : aucun de ces outils n'est une chaîne de production validée, et aucun n'autorise une diffusion.

## Contenu

- `check_manifest.py` : confronte la fiche d'un film (`provenance-manifest.json`) aux fichiers qu'elle cite. Code de sortie 0, 1 (au moins un FAIL) ou 2 (des UNVERIFIED).
- `build_from_fiche.py` : génère depuis la fiche la composition, les sous-titres SRT et VTT et la transcription. L'habillage est en dur et dépend de `manifest_version` : la version 1 garde le bandeau d'origine, octet pour octet ; la version 2 demande deux champs de plus dans `film`, `title` (titre d'ouverture, affiché sans être dit, repris en tête de la transcription) et `capture_zoom` (de 1 à 1,5, capture agrandie depuis le haut, le reste est rogné), et met les sous-titres en cartouche. La version 3 garde les champs et l'habillage de la version 2 et découpe chaque phrase en sous-titres de 2 lignes de 42 caractères au plus : coupure aux fins de phrase, puis aux virgules, entre deux mots en dernier recours ; la fenêtre de la phrase est partagée au prorata des caractères. Le débit de lecture ne change pas (16 à 18 caractères par seconde pour le film 47) : il dépend de la voix. La version 4 garde la version 3 et accepte une scène `insert` en fin de film : au plus une, après toutes les scènes filmées, sans geste ni résultat, statut `reasoned`, champ `insert_ref` vers une sous-composition HyperFrames rangée dans `compositions/` et qui déclare `data-composition-id="insert"` et sa timeline. La capture s'arrête quand l'insert commence ; le fichier de l'insert est figé et compté parmi les médias du garde.
- `contact_sheet.py` : planche de 12 images d'un film rendu, à regarder avant l'approbation, écrite à côté de la vidéo (`<film>-planche.png`). Sans légende, faute de `drawtext` dans le ffmpeg local : les instants des images sont rendus dans la sortie JSON, rangée par rangée. N'écrase pas une planche existante.
- `test_soustitres_v3.py` : découpage et minutage des sous-titres en version 3, sur la fiche du film 47 ; films déjà rendus inchangés ; planche sur une vidéo de synthèse.
- `test_rendu_hors_ligne.py` : le rendu gardé et le brouillon témoin tournent sous `sandbox-exec`, sans connexion sortante hors de la machine (HyperFrames demande sinon la police Inter à Google Fonts, sans effet sur l'image : ticket 65) ; sans `sandbox-exec`, le rendu est refusé.
- `test_inserts_v4.py` : insert de fin de film en version 4, sur la fiche du film 47 ; chaque motif de refus, et l'insert compté parmi les médias du garde.
- `film_guard.py` : garde de rendu. Précontrôle des entrées figées, contrôle de la fiche, validation du film avant dépôt.
- `repin.py` : refige les empreintes d'un film après un changement voulu. `--check` n'écrit rien.
- `place_cues.py` : pose les repères de la fiche (phrases, sous-titres, durée du film) depuis les durées des clips mesurées par ffprobe. Refuse la fiche d'un film déjà rendu.
- `witness_reference.py` : rend le brouillon témoin (HyperFrames 0.8.33, mêmes options que le garde, télémétrie coupée) et écrit `output-reference.json` ; `--from` part d'un témoin déjà rendu. Refuse la fiche d'un film déjà rendu et n'écrase pas un témoin.
- `composition_check.py` : contrôle la composition sans la rendre, par `hyperframes check` 0.8.33 dans le bac à sable sans réseau, sur une copie des seules entrées du garde. Refuse une erreur de lint ou d'exécution, un texte qui déborde, un texte illisible, et toute mesure absente. `witness_reference.py` le lance avant de rendre le témoin ; il se lance aussi seul sur le dossier d'un film (code 0, 1 ou 2). Le verdict vient des compteurs du rapport : HyperFrames répond « ok » et sort en code 0 avec des sous-titres illisibles (mesure du 27 novembre 2026, issue 70). Environ 80 secondes par film.
- `test_composition_check.py` : chaque motif de refus sur des rapports construits ; le témoin n'est pas rendu si la composition est refusée ; le vrai HyperFrames sur des copies du film 47 (saine, sous-titres illisibles, seconde composition à la racine).
  Le contrôle par mutation ne couvre ni `composition_check.py` ni `witness_reference.py` : leurs refus ne sont pas mutés et cette suite n'y est pas rejouée (ses trois tests avec le vrai HyperFrames durent près de quatre minutes).
- `content_check.py` : contrôle le contenu du brouillon témoin avant qu'il devienne la référence, par trois filtres de FFmpeg et sa mesure de niveau, sans rien modifier. Refuse un son muet, une phrase de la fiche dont le créneau est silencieux, un écran noir sur la moitié du film, une seule image tenue sur 90 % du film (ticket 78). `test_content_check.py` : chaque refus sur des mesures construites, puis sur des témoins fabriqués par FFmpeg ; un témoin refusé n'écrit pas de référence ; les témoins de la chaîne sont acceptés. Comme pour le contrôle de composition, ses refus ne sont pas mutés par `mutation_check.py`.
- `test_outils_fiche.py` : les deux outils redonnent les valeurs posées à la main pour le film 47, et leurs refus ; un fichier d'empreintes absent donne un FAIL du contrôle de fiche.
- `capture_lib.cjs` : navigateur, pointeur visible, horloge, journal et conversion des captures.
- `test_repin.py` : tests de `repin.py`.
- `test_capture_lib.py` : le dépôt d'une capture n'écrase rien et n'écrit rien à travers un lien, avec un faux navigateur et le vrai ffmpeg.
- `test_guard_main.py` : verdict, code de sortie et reçu de rendu du garde, sans média.
- `test_interruption.py` : l'arrêt d'un rendu ne laisse aucun processus en vie.
- `test_review_findings.py` : un test par constat corrigé de la revue du 23 novembre, sur une copie du film de réservation.
- `test_codex_findings.py` : un test par constat des deux revues indépendantes de Codex du 24 novembre (générateur qui écrasait une entrée ou la fiche, composition mal adressée, journal de capture absent ou vide, mutants illisibles).
- `test_film_guard.py` : films trafiqués, précontrôle et forme du film, joués sur chaque film.
- `test_fiche_checks.py` : chaque motif de refus du contrôle de fiche, joué sur chaque film.
- `test_habillage_v2.py` : la version 1 génère les fichiers d'avant ; ce que la version 2 ajoute, motif par motif.
- `mutation_check.py` : supprime chaque contrôle l'un après l'autre et signale ceux dont aucun test ne s'aperçoit. Il rejoue toutes les suites pour chacun des 106 contrôles : 66 minutes sur le MacBook Pro au 27 novembre 2026. À lancer en arrière-plan, une fois après une série de changements du garde plutôt qu'à chaque PR ; il ne modifie rien dans le dépôt. Ne rien modifier dans `film-chain` pendant sa première minute, le temps qu'il copie les fichiers.
- `synthesize_libra.py`, `libra-requirements.txt` : seconde voix de synthèse, Libra-TTS, pour un film neuf (voir « Installer la seconde voix »). `test_synthesize_libra.py` : ses refus, testés sans le modèle, et une vraie synthèse sans réseau, sautée si Libra-TTS n'est pas installé sur le Mac.

Les tests propres à un film (gestes, fichiers générés) restent dans son dossier.

## Ce qui reste propre à chaque film

Sa fiche, sa page filmée, ses gestes (`capture.cjs`), ses clips de voix, son fichier d'empreintes, son `render_guarded.py` réduit à ses paramètres, et ses tests.

## Deux gardes antérieurs, hors de cette chaîne

Deux dossiers gardent leur propre garde, écrit avant `film-chain` : ils ne sont pas migrés, et les contrôles de ce dossier ne s'y appliquent pas.

- `ff10-second-web-demo-transfer/form-pilot/` : premier pilote du formulaire, avec l'ancienne voix. Il n'a pas de fiche. Il est remplacé par `form-pilot-kokoro/`, qui reprend sa page et sa capture comme sources : ne pas modifier ni supprimer `form.html` et ses médias. Ses neuf tests passent (relevé du 24 novembre 2026). Décision du même jour : le laisser tel quel, comme trace d'essai ; lui écrire une fiche reviendrait à documenter un film que personne ne rendra de nouveau.
- `ff10-web-workflow-entrypoint/local/` : film V5, filmé sur un site public. Sa fiche répond FAIL depuis qu'un film approuvé doit avoir un journal de capture lisible. Le remettre sur cette chaîne demande une nouvelle capture du site, donc un nouveau film et une nouvelle approbation : décision en attente (ticket 46).

## Fabriquer un film neuf, dans l'ordre

1. Écrire la fiche avec les phrases, statut `DRAFT`, sans empreinte de film, en version 3 (version 4 si le film finit par un insert animé).
2. Produire les clips de narration et mesurer leurs durées.
3. `python3 place_cues.py CHEMIN_DE_LA_FICHE` (écarts réglables : `--first`, `--gap`, `--pad`, `--tail`), puis `python3 build_from_fiche.py CHEMIN_DE_LA_FICHE`.
4. Écrire `capture.cjs` et capturer.
5. Écrire le fichier d'empreintes et le `render_guarded.py` du film, puis `python3 repin.py DOSSIER`.
6. `python3 witness_reference.py DOSSIER` contrôle la composition (refus sans rendu si un texte est illisible ou déborde), rend le brouillon témoin, contrôle son contenu (refus sans référence s'il est muet, noir, figé ou s'il manque une voix) et écrit la référence de sortie ; regarder le témoin (`python3 contact_sheet.py VIDEO`), puis refiger.
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

## Installer la seconde voix, Libra-TTS

Seconde voix possible pour un film neuf, décidée par Alex le 28 novembre 2026 après écoute (ticket 75, essai dans `research/libra-tts-essai-2026-11-28.md`). Les films approuvés restent en Kokoro : leurs clips sont figés et ne se resynthétisent pas. Le garde et la fiche ne distinguent pas les deux voix ; la fiche ne cite que des clips.

Tout est figé : le code de `ekambrar100/Libra-TTS` au commit `2642632…7a09`, ses 23 paquets par empreintes dans `libra-requirements.txt`, et le modèle `Ekam/Libra-TTS` à la révision `a29b9e64…8c92`, dont `synthesize_libra.py` contrôle les sept fichiers par empreinte avant de le charger. Depuis la racine du dépôt :

```bash
uv venv .venv-libra --python 3.12
uv pip install --python .venv-libra/bin/python --require-hashes -r experiments/2026-11-23-macbook-pro/film-chain/libra-requirements.txt
.venv-libra/bin/hf download Ekam/Libra-TTS config.json tokenizer.json model.safetensors codec.safetensors \
  frontend/en_acronyms.txt frontend/en_lexicon.tsv frontend/zh_rare_tokens.json \
  --revision a29b9e64155bffd08966f180502ca412cb358c92 \
  --local-dir ~/.cache/frameforge/libra-tts/a29b9e64155bffd08966f180502ca412cb358c92
```

Puis, pour synthétiser les phrases de la fiche d'un film neuf :

```bash
.venv-libra/bin/python experiments/2026-11-23-macbook-pro/film-chain/synthesize_libra.py CHEMIN_DU_FILM --voice nina
```

- Huit voix : `nina` (par défaut), `sofia`, `aliya`, `maya`, `omar`, `jon`, `bob`, `sam`. Écoute d'Alex du 28 novembre 2026 sur une phrase : `nina` et `sam` « très bien », `aliya` et `bob` à écarter (détail dans `research/libra-tts-essai-2026-11-28.md`). Langue `fr`, graine 0, moteur MLX ; les styles de lecture du modèle ne sont pas exposés.
- `.venv-libra/` pèse environ 300 Mo et le modèle 950 Mo ; ni l'un ni l'autre n'est suivi par Git. Le téléchargement est la seule étape qui demande le réseau.
- Le script refuse d'écraser un clip ou un `narration-synthesis.json` déjà présent : pour recommencer, déplacer d'abord les clips. Il ne peut donc pas remplacer la voix d'un film approuvé.
- **Le niveau de chaque clip est ramené à −23 LUFS**, celui des clips Kokoro des films approuvés, par un réglage de volume seul : même gain sur tout le clip, ni compression ni filtre. Mesuré le 28 novembre 2026, Libra-TTS sortait environ 6 LU plus fort que Kokoro, avec 3,8 LU d'écart d'une phrase à l'autre et des crêtes à 0 dBTP. Le gain ne monte jamais au point de porter la crête au-dessus de −1 dBTP ; un clip muet est refusé. Le rapport note pour chaque clip le niveau d'origine, le gain et le niveau obtenu. Le niveau est mesuré par FFmpeg (`loudnorm`), sur des clips courts : précis à quelques dixièmes de LU.
- Libra-TTS n'a pas de réglage de vitesse : les durées des clips diffèrent de celles de Kokoro (réglé à 1,2), et les instants de la fiche sont à reposer.
- Vérifié le 28 novembre 2026 sur le Mac Studio (macOS 27.0), réseau coupé par `sandbox-exec` : les trois phrases de la réservation ressortent identiques à l'octet d'un passage à l'autre, et identiques aux clips de l'essai, produits par un autre environnement installé séparément. Non vérifié : sur le MacBook Pro, et après une mise à jour de macOS.
- Projet publié le 19 novembre 2026, un seul auteur, aucune version publiée : rien ne garantit son suivi. Tant que les empreintes ci-dessus tiennent, la synthèse ne dépend pas de lui.

## Pièges constatés

- **Les médias figés n'existent qu'en un exemplaire local.** Une capture, un clip ou un film n'est pas versionné : l'écraser, c'est perdre le film approuvé. `capture_lib.cjs` refuse d'écraser une capture existante ; pour un essai, définir `FF_CAPTURE_OUT`. Une copie des médias des trois films approuvés est conservée hors dépôt, sur le même Mac, dans `~/Claude-worktrees/frameforge-medias-approuves/`, avec ses empreintes ; elle est à refaire après chaque nouvelle approbation.
- **Refiger n'est pas approuver.** `repin.py` rend cohérentes des empreintes ; il ne dit pas que le changement est voulu. Relire ce qu'il affiche avant de commiter.
- **Une nouvelle synthèse de voix peut donner un autre son**, même avec une graine fixe. Elle demande une nouvelle écoute.
- **Un résultat qui se fait attendre se date avec `appear`, pas avec `locator.waitFor`.** L'attente de Playwright espace ses essais jusqu'à une demi-seconde : le journal datait le résultat de 0,3 à 0,5 s trop tard. `appear(sélecteur)`, fourni à `play`, relit la page à chaque image. Un résultat qui suit aussitôt un clic n'est pas concerné.
- **Un film approuvé sans journal de capture lisible est en échec.** Pour un brouillon, c'est un manque (UNVERIFIED) ; dès que la fiche dit `REVIEWED` ou `APPROVED_FOR_RELEASE`, c'est un FAIL du contrôle `statuses` : rien ne prouve ce que le film dit avoir observé. Décision du 24 novembre 2026 (issue 15). Le film V5 (`ff10-web-workflow-entrypoint/local`), approuvé à l'écoute avec un journal dans un autre format, est dans ce cas : sa fiche répond FAIL tant que sa capture n'est pas refaite avec `capture_lib.cjs`.
- **Le garde d'un film nomme ses fichiers en clair.** `repin.py` lit `pins_ref`, `reference_ref` et `output` dans l'appel qui construit `GUARD`, sans exécuter le fichier : un nom passé par une variable est refusé.
- **Rien n'est écrit à travers un lien symbolique.** Le générateur et la capture refusent un fichier ou un sous-dossier qui est un lien, et un nom qui sort du dossier du film.
- **Un film présent sans son reçu de rendu bloque le rendu suivant.** Cela arrive si le rendu est arrêté entre le dépôt du film et l'écriture du reçu. Le garde répond `…_output_without_receipt` : déplacer le film ailleurs, puis rendre de nouveau.
- **Le contrôle de composition ne mesure que le texte de la composition.** Titre et sous-titres, relevés à quelques instants du film, au seuil de HyperFrames (3 pour 1) ; l'interface filmée dans la capture n'est pas mesurée. Il se lance sur la copie isolée, jamais sur le dossier du film : `baseline.html` à côté d'`index.html` y fait deux compositions à la racine, et HyperFrames ne mesure alors plus rien.
- **Le contrôle de contenu voit un film vide ou amputé, pas un film faux.** Une voix qui dit autre chose, une image qui montre la mauvaise page ou un son trop fort passent. Nos films sont immobiles 88 à 96 % du temps (mesuré le 28 novembre 2026 sur six témoins) : seule une image unique sur presque tout le film est refusée, pas un plan fixe de plusieurs secondes.
- **FFmpeg fait partie de l'environnement de rendu et n'est pas figé.** Relire un film existant ne dépend plus de sa version : l'empreinte des paquets écarte la ligne `#software` (ticket 73). Mais HyperFrames écrit le film avec le FFmpeg de la machine, et le film porte sa version (`encoder` dans `expected_format_tags`) : un rendu fait après une mise à jour de FFmpeg ne redonnera pas le film approuvé. Les films approuvés au 27 novembre 2026 sortent de FFmpeg 9.0.1.
- **Aucun contrôle automatique ne voit un pointeur qui masque un résultat.** Regarder une planche d'images de la capture.
