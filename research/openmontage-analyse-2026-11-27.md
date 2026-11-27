# OpenMontage : ce qui peut servir à FrameForge

Analyse du 27 novembre 2026, en lecture seule. Rien n'a été installé, cloné, exécuté ni copié dans un dépôt ; aucune issue publiée.

## Révisions figées

- OpenMontage : `2e003e65fa99a0f329478a2c1cdcf26bc481933a` (16 novembre 2026), AGPL-3.0, 2 285 fichiers.
- FrameForge : `dc8f8aa24fd5455c26df9a8e197f369a03c313f3`, licence MIT, arbre propre.

## Méthode et limites

Arborescence complète d'OpenMontage lue par l'API GitHub ; 41 fichiers lus en tout ou en partie (liste en fin de document), soit moins de 2 % du dépôt. Côté FrameForge : `INTENT.md`, `SPEC.md`, `WHY.md`, `PUBLICATION-POLICY.md`, `REPRISE.md`, `film-chain/README.md`.

Non vérifié : tout comportement à l'exécution, les 12 autres pipelines, les outils de recherche de rushes et de sélection de prises, les 103 fichiers de compétences de pipeline, les coûts annoncés, Backlot avec VoiceOver. Aucun `contraintes.md` n'existe dans FrameForge : les contraintes ci-dessous viennent de `INTENT.md`, `SPEC.md` et `film-chain/README.md`.

## Contraintes et hypothèses

- FrameForge est sous MIT. Du code AGPL-3.0 copié ou adapté ferait passer l'ensemble dérivé sous AGPL à la distribution. Reprendre une idée et la réécrire n'emporte pas cette obligation ; reprendre un fichier, si. Ce point reste une lecture personnelle de la licence, pas un avis juridique.
- Le rendu FrameForge est figé : HyperFrames 0.8.33, Node 24.22.1, sans réseau sous `sandbox-exec`, film refusé s'il ne redonne pas l'empreinte approuvée. OpenMontage appelle `npx hyperframes` sans version figée (`tools/video/hyperframes_compose.py`, résolution par `npm view`), et fixe Node 22.23.4 et Python 3.11.
- `SPEC.md` et `WHY.md` excluent un nouvel orchestrateur et une usine multi-agents au MVP. OpenMontage en est une : huit rôles « director » par pipeline.
- Voix : Kokoro 0.9.4 `ff_siwis` en local. OpenMontage n'a aucun fichier Kokoro ; son seul chemin local est Piper, voix par défaut `en_US-lessac-medium`. Qualité de Piper en français face à Kokoro : hypothèse à vérifier, non testée.

## Écarts entre la fiche et le dépôt

- Backlot ne valide rien. Son serveur n'expose que des routes GET (`backlot/server.py`) et son README le décrit comme un tableau en lecture seule. Les validations humaines passent par les points de contrôle des pipelines (`lib/checkpoint.py`), pas par Backlot.
- Accessibilité de Backlot, indices statiques seulement : dans `backlot/ui/board.js` (1 146 lignes), 14 `onclick`, aucun `<button`, aucun `role=`, aucun `tabindex`, 3 attributs `aria-`, 1 écoute clavier ; pages en `lang="en"`. Cela annonce des éléments cliquables hors d'atteinte au clavier ; ce n'est pas un test VoiceOver.
- La publication n'est pas automatique : `tools/publishers/export_bundle.py` ne fait qu'un dossier local, sans envoi. Compatible avec `PUBLICATION-POLICY.md`.
- Le pipeline `screen-demo` capture l'écran par FFmpeg (`avfoundation`) et demande, à l'étape de montage, de couper ou d'accélérer les temps morts. C'est contraire à l'invariant FrameForge (pas de coupe ni d'accélération silencieuse) et il n'y a pas de journal de gestes.

## Verdicts par composant

**Manifestes de pipeline** (`pipeline_defs/screen-demo.yaml`) : REJECT. Sept étapes et huit rôles pour un besoin que la fiche de film et le garde couvrent ; contraire au non-objectif « pas d'usine multi-agents ».

**Registre d'outils, suivi des coûts, routage de fournisseurs** (`tools/tool_registry.py`, `tools/base_tool.py`) : REJECT. FrameForge n'appelle aucun service payant.

**Points de contrôle et reprise** (`lib/checkpoint.py`) : REUSE_EXISTING. Empreintes, reçus de rendu, statuts `DRAFT / REVIEWED / APPROVED_FOR_RELEASE` et reprise ciblée (ff10) existent déjà, avec une garantie plus forte : le film approuvé est lié à une empreinte.

**Garde réseau** (`tests/test_network_guard.py`) : REUSE_EXISTING. Leur garde bloque les sockets Python pendant les tests ; `sandbox-exec` coupe aussi Chrome et Node.

**Contrôles de livraison** (`tools/analysis/visual_qa.py`, `composition_validator.py`, `frame_sampler.py`) : REUSE_EXISTING. Sonde ffprobe, images échantillonnées, niveaux audio : `film_guard.py`, `contact_sheet.py` et `av-qa-v3/qa.py` les couvrent. Leur contrôle d'occultation compare un visage et la zone de sous-titres ; il ne répond pas au pointeur qui masque un résultat.

**Revue finale** (`schemas/artifacts/final_review.schema.json`) : EXTRACT_ONLY, idées seulement. Deux champs utiles :
- `transcript_comparison` (film retranscrit, comparé au texte, taux de mots exacts) : c'est le contrôle que demandent les tickets 36 et 61. Leur schéma confirme la forme du résultat, pas la faisabilité en français.
- `subtitle_check` distingue « sous-titres attendus » de « sous-titres présents » et mesure la couverture. Rien n'y exige un SRT séparé : l'exigence FrameForge reste plus stricte.

**Promesse de livraison** (`lib/delivery_promise.py`, champs `runtime_swap_detected` et `silent_downgrade_detected`) : EXTRACT_ONLY, idée seulement. Le principe « ce qui a été promis à la proposition est comparé à ce qui a tourné » rejoint la règle de repli de `SPEC.md`. Le garde le fait déjà pour la version d'HyperFrames ; rien à ajouter tant qu'il n'y a qu'un moteur.

**Provenance des médias** (`schemas/artifacts/asset_manifest.schema.json`) : EXTRACT_ONLY, idée seulement. Champs `license`, `original_url`, `provider` par média, en texte libre et non vérifiés. À reprendre le jour où un film utilisera un média tiers ; inutile pour les films actuels, entièrement capturés et synthétisés sur place.

**Choix du moteur** (`skills/meta/animation-runtime-selector.md`) : REJECT. Arbitre Remotion, HyperFrames et FFmpeg ; FrameForge a tranché (`research/comparaison-claude-remotion-hyperframes.md`).

**Sous-titres** (`tools/subtitle/subtitle_gen.py`) : REUSE_EXISTING. Coupe à 8 mots ou 42 caractères, sans égard pour la ponctuation : c'est le défaut corrigé par la fiche v3.

**Alignement narration et étapes** (`lib/verify_scene_pacing.py`) : REUSE_EXISTING. Propre à leur scène de terminal Remotion ; `place_cues.py` et les contrôles de gestes font ce travail.

**Voix** (`tools/audio/piper_tts.py`, `tts_selector.py`) : REJECT. Pas de Kokoro ; une nouvelle voix imposerait de nouvelles écoutes.

**Backlot** : REJECT en l'état. Lecture seule, lié à leur format de projet, accessibilité douteuse sur indices statiques.

**Compétences HyperFrames embarquées** (`.agents/skills/hyperframes-*`, environ 250 fichiers, `website-to-video`) : EXPERIMENT, lecture seule. Elles peuvent aider les inserts animés (ticket 59). Leur origine et leur licence propre ne sont pas établies (aucun fichier de licence dans ces dossiers) : chercher d'abord la source chez l'éditeur d'HyperFrames.

**`hyperframes check`** (cité dans `hyperframes_compose.py` comme contrôle unifié : lint, exécution, mise en page, mouvement, contraste) : EXPERIMENT. C'est une commande d'HyperFrames, pas d'OpenMontage. Aucune occurrence de `hyperframes lint`, `check`, `validate` ou `doctor` dans FrameForge. Essai fait le même jour : voir « Essai de `hyperframes check` » plus bas.

**Recherche de rushes et sélection de prises** : non lu. Hors MVP (le montage de rushes est une extension future) ; à rouvrir avec ff11 et ff12 le moment venu.

## Synthèse

Pas d'adoption, ni globale ni par composant. Aucune lacune démontrée de FrameForge n'est comblée par du code OpenMontage. L'apport se réduit à trois idées à réécrire (comparaison transcription et texte, sous-titres attendus contre présents, licence par média) et à deux pistes qui relèvent d'HyperFrames lui-même.

Rien de ce qu'OpenMontage contient ne répond au ticket 67 (écart de rendu entre macOS 27.0 et 26.5.2) : aucun rendu en conteneur n'a été vu dans les fichiers lus.

## Essai de `hyperframes check` (27 novembre 2026)

Conditions : Mac Studio (`mac-studio-alex`, macOS 27.0), HyperFrames 0.8.33 lu dans le cache npm (`npx --offline hyperframes@0.8.33`), télémétrie coupée, sous `sandbox-exec` avec le profil sans réseau du garde. Le film 47 (`ff47-film-fenetres-modales`, `index.html` d'empreinte `ca9bec8348fa81da…`) a été copié hors du dépôt ; le dépôt et le garde n'ont pas été touchés. Aucun rendu n'a été lancé.

Trois passages, commande `check --json` :

1. Copie telle quelle : code de sortie 1. Erreur de lint `multiple_root_compositions` (`baseline.html` et `index.html` déclarent tous deux une composition à la racine). Les passes de mise en page et de contraste n'ont alors rien mesuré (0 échantillon, 0 élément contrôlé) tout en répondant `ok: true`.
2. Copie sans `baseline.html` : code de sortie 0. Mise en page : 9 instants sur 54 s, 0 débordement. Contraste : 4 éléments de texte contrôlés sur 5 instants, 4 conformes. Un avertissement de lint (`timeline_track_too_dense`, 7 éléments sur la piste 6).
3. Test négatif, sous-titres passés de `#fff` à `#333` sur fond sombre : 4 éléments contrôlés, 0 conforme, contrastes mesurés de 1,18 à 1,28 pour 3 exigé. Mais ce sont des avertissements : code de sortie 0 et `ok: true`. Seule l'option `--strict`, non essayée, promet un code de sortie non nul.

Ce que l'essai établit : la commande existe en 0.8.33, tourne sans réseau en moins d'une minute et voit un sous-titre illisible. Ce qu'il n'établit pas :

- le contraste ne porte que sur le texte de la composition (titre, sous-titres), pas sur l'interface filmée dans la capture ;
- le seuil annoncé est 3 pour 1, celui des grands textes ; l'exigence pour un sous-titre reste à fixer ;
- un seul film, sur le Mac dont le rendu diffère du film approuvé (ticket 67) ;
- sans `--strict`, un défaut de contraste passe ; avec une erreur de lint, les passes suivantes sont vides et vertes.

Complément du même jour :

- `check --strict` sort en code 1 sur la copie aux sous-titres illisibles, mais aussi sur la copie saine : l'avertissement de lint `timeline_track_too_dense`, dû à la forme que produit `build_from_fiche.py`, suffit. Le code de sortie ne distingue pas les deux cas.
- `baseline.html` n'entre pas dans le rendu gardé : `guarded_hyperframes_v2.py` rend depuis une copie `project/` et range `baseline.html` à côté, pour le seul précontrôle. Mesure sur le film approuvé `d10c50b8…` : la fenêtre de la voix 1 donne -23,3 dB en moyenne et -5,1 dB en crête, comme `voice1.wav` seul ; pas de son joué deux fois.

Verdict : EXPERIMENT concluant comme contrôle d'appoint avant le brouillon témoin, lancé sur la copie isolée du garde, sans `--strict`, en lisant les compteurs (`contrast.checked`, `contrast.passed`, `layout.samples`) et non `ok` ni le code de sortie. L'intégrer à la chaîne est une décision à part (issue 70). Restent non faits : un passage sur le MacBook Pro et un cas de débordement de texte.

Découverte annexe : HyperFrames 0.8.33 a aussi une commande `transcribe` (horodatage mot à mot), à regarder pour le ticket 61 avant tout autre outil. Non essayée.

## Fichiers OpenMontage lus

`pipeline_defs/screen-demo.yaml`, `lib/delivery_promise.py`, `lib/checkpoint.py`, `lib/source_media_review.py`, `lib/verify_scene_pacing.py`, `lib/slideshow_risk.py`, `tools/subtitle/subtitle_gen.py`, `tools/publishers/export_bundle.py`, `tools/analysis/{visual_qa,composition_validator,frame_sampler,audio_probe}.py`, `tools/audio/{piper_tts,tts_selector}.py`, `tools/capture/{screen_recorder,cap_recorder}.py`, `tools/video/hyperframes_compose.py`, `tools/tool_registry.py`, `tools/base_tool.py`, `tests/test_network_guard.py`, `backlot/README.md`, `backlot/server.py`, `backlot/ui/{index.html,board.html,board.js}`, `schemas/artifacts/{final_review,asset_manifest,render_report,decision_log}.schema.json`, `skills/meta/{animation-runtime-selector,reviewer}.md`, `skills/core/subtitle-sync.md`, `skills/pipelines/screen-demo/compose-director.md`, `docs/{ARCHITECTURE,apple-silicon-mps}.md`, `PROJECT_CONTEXT.md`, `requirements.txt`, `config.yaml`, `.node-version`, `.python-version`, `.claude/launch.json`, `.github/workflows/ci.yml`.

Plusieurs n'ont été lus que par leur en-tête ou par recherche de motifs : `lib/checkpoint.py`, `lib/source_media_review.py`, `lib/slideshow_risk.py`, `tools/tool_registry.py`, `tools/base_tool.py`, `tools/capture/cap_recorder.py`, `docs/ARCHITECTURE.md`, `skills/meta/reviewer.md`, `compose-director.md`, `ci.yml`, `config.yaml`, `subtitle-sync.md`, `render_report` et `decision_log`.
