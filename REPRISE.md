# REPRISE — FrameForge

Dernière mise à jour : 28 novembre 2026, session sur le Mac Studio. Studio à `b6c1b17` avant cette mise à jour ; le MacBook Pro, injoignable en SSH à la clôture, est resté sur la branche `fix/empreinte-paquets-sans-version-ffmpeg` à `89f6760` : le remettre sur `main` (`git switch main`, puis `git pull --ff-only`). Vérifier HEAD et la synchronisation au démarrage.

## Prochaine action
Faire l'écoute [#35](https://github.com/Alexmacapple/frameforge/issues/35) du film de réservation par une personne qui n'a jamais vu le film (la partie B, [#36](https://github.com/Alexmacapple/frameforge/issues/36), est déclarée conforme depuis le 28 novembre), avec `experiments/2026-11-23-macbook-pro/ff04-room-booking-film/LISTENING-SHEET.md` et `media/room-booking-son-seul.m4a`. Même feuille prête pour les fenêtres modales (`ff59-film-fenetres-modales-recap/LISTENING-SHEET.md`) ; sa partie B y est déclarée conforme par Alex le 25 novembre, sa partie A reste à faire. [#61](https://github.com/Alexmacapple/frameforge/issues/61) (prononciation par transcription française) attend ces écoutes.

## Fait le 28 novembre 2026
- Libra-TTS est une seconde voix possible pour un film neuf (PR #76, ticket [#75](https://github.com/Alexmacapple/frameforge/issues/75) laissé ouvert) : `film-chain/synthesize_libra.py`, paquets et modèle figés par empreintes, installés sur le Mac Studio seulement (`.venv-libra`, modèle dans `~/.cache/frameforge/libra-tts/`). Décision d'Alex après écoute de la voix `nina`. Kokoro reste la voix par défaut et celle des films approuvés. Pour demander cette voix : dire « voix Libra » (ou « voix Nina ») en commandant le film. Essai : `research/libra-tts-essai-2026-11-28.md`.
- PR #77 : chaque clip Libra-TTS est ramené à −23 LUFS, le niveau de Kokoro, par un réglage de volume seul ; Libra-TTS sortait environ 6 LU plus fort, avec 3,8 LU d'écart d'une phrase à l'autre. Écoute d'Alex après réglage : « parfait ». Voix préférées : `nina` et `sam`.
- #47 relu : ses cinq critères sont satisfaits, preuves dans le ticket ; fermé à la demande d'Alex.
- #68 : ffmpeg-skill évalué au commit `53b1be1` (`v4.26.0`), à ne pas installer ; trois idées à reprendre avec notre FFmpeg (`research/ffmpeg-skill-analyse-2026-11-28.md`), aucun ticket ouvert, contre-revue indépendante non faite.
- Hors dépôt : Impeccable passé en 4.11.1 (moteur 0.1.31) sur le Mac Studio, télémétrie coupée ; le MacBook Pro reste en 4.8.0.
- #36 : partie B de l'écoute du film de réservation déclarée conforme par Alex (`ff04-room-booking-film/LISTENING-2026-11-28.md`) ; fermé à la demande d'Alex.
- Veille rea-video : aucune intégration (`research/rea-video-analyse-2026-11-28.md`).

## Fait le 27 novembre 2026
- #69 fermé : veille OpenMontage (AGPL-3.0, SHA `2e003e65`), aucun composant adopté ; rapport `research/openmontage-analyse-2026-11-27.md`.
- #70 fermé : `composition_check.py` lance `hyperframes check` 0.8.33 avant le brouillon témoin et refuse un texte illisible ou qui déborde, sans rendre (PR #71). Verdict lu dans les compteurs du rapport : HyperFrames répond « ok » et sort en code 0 avec des sous-titres illisibles. Les quatre films de la chaîne sont acceptés.
- PR #72 : la suite de ce contrôle est retirée du contrôle par mutation, qu'elle aurait fait durer plus de 7 heures. Contrôle par mutation rejoué sur le MacBook Pro : 106 mutants, aucun survivant, 66 minutes.
- #61 commenté : forme de résultat à viser, et commande `transcribe` de HyperFrames 0.8.33 à regarder d'abord (non essayée).
- #73 fermé (PR #74, fusionnée le 28 novembre) : les 11 tests en échec sur le Mac Studio venaient de FFmpeg (9.0.2 sur le Studio, 9.0.1 sur le MacBook), dont la version entrait dans l'empreinte des paquets. La ligne `#software` est écartée du calcul ; `expected_packets_sha256` recalculée dans huit références et refigée par `repin.py`. Suites vertes sur les deux Mac (235, 45 et 9 tests) ; contrôle par mutation sur le MacBook Pro : 106 mutants, aucun survivant, 63 minutes.

## Fait le 25 novembre 2026
- #47 : film des fenêtres modales produit et approuvé (PR #57, `d10c50b8…0845`). Ticket fermé le 28 novembre.
- #56 fermé (verdict COMPOSE) ; ses manques 1, 2, 4 (PR #58), 5 et 6 (PR #62 : fiche v3 à sous-titres découpés, `contact_sheet.py`) traités.
- #59 : insert animé jugé utile (PR #63), intégré en fin de film par la fiche v4 (PR #64) ; film `ff59-film-fenetres-modales-recap` approuvé (`3720625a…1af6`), à côté du film 47 inchangé.
- #65 : le rendu gardé et le brouillon témoin tournent sous `sandbox-exec`, sans réseau sortant (PR #66). La police Inter que HyperFrames demandait à Google n'entrait pas dans l'image.
- Essai du prompt de motion design rangé dans `ff59-essai-motion-design/` ; note de source `research/comparaison-claude-remotion-hyperframes.md`.
- Télémétrie HyperFrames coupée sur le MacBook Pro.

## Points à surveiller
- Libra-TTS : le réglage de niveau dépend d'une mesure faite par FFmpeg, dont la version diffère entre les deux Mac ; rien ne dit que les clips ressortent identiques à l'octet sur le MacBook Pro.
- Libra-TTS : non installé ni vérifié sur le MacBook Pro (procédure dans le README de film-chain) ; on ne sait pas si les clips y ressortent identiques à ceux du Studio. Aucun film n'a encore été produit avec cette voix ; elle n'a pas de réglage de vitesse, les instants de la fiche sont à reposer. Seule `nina` a été écoutée, sur huit voix.
- Mac Studio, équipé le 26 novembre 2026 : dépôt cloné au même chemin, médias non versionnés copiés (742 fichiers, empreintes identiques), HyperFrames 0.8.33 installé, télémétrie coupée (`config`), mêmes octets que le MacBook pour Node 24.22.1 (`~/.local/bin`) et chrome-headless-shell 152.0.7977.30. `.venv-voice` non copié : à recréer avant toute synthèse de voix.
- [#67](https://github.com/Alexmacapple/frameforge/issues/67) : un film rendu sur le Mac Studio (macOS 27.0) n'est pas le film approuvé sur le MacBook (macOS 26.5.2) ; même son, images différentes là où il y a du texte. Seul le MacBook reproduit les films approuvés ; le garde refuse tout autre résultat. Décision à prendre (même macOS ou rendu en conteneur).
- `sandbox-exec` est marqué obsolète par Apple : vérifier qu'il fonctionne après chaque mise à jour de macOS (`test_rendu_hors_ligne.py`).
- Disque du MacBook Pro plein à 99 % le 25 novembre, ramené à 89 % : un rendu de 66 s demande environ 16 Go temporaires.
- FFmpeg n'est pas figé : HyperFrames écrit le film avec le FFmpeg de la machine et le film porte sa version. Les films approuvés sortent de FFmpeg 9.0.1 ; ne pas mettre FFmpeg à jour sur le MacBook Pro (Homebrew propose la 9.1) avant la décision #67, où ce point est commenté. Non vérifié : si le rendu en conteneur fige aussi FFmpeg.
- Contrôle par mutation : dernier passage complet le 27 novembre 2026 sur la PR #74 (106/106, 63 minutes) ; à relancer après la prochaine série de changements du garde. Il ne couvre pas `composition_check.py` ni `witness_reference.py` : leurs refus ne sont pas mutés.
- Contrôle de composition : aucun cas réel de débordement de texte n'a été produit ; les textes ne sont relevés qu'à quelques instants du film ; l'interface filmée n'est pas mesurée ; environ 80 secondes de plus avant chaque témoin.
- Le MacBook Pro accepte la clé SSH du Mac Studio depuis le 27 novembre 2026 (`ssh macbook-pro`, autorisation ajoutée par Alex).
- #40/#41, #44, #46, thèmes #5–#12/#15 : consulter leur état courant.

## Règles
GitHub (issues et preuves) reste la source de vérité du suivi. En cas de divergence, vérifier les décisions humaines et les preuves les plus récentes ; ne pas arbitrer silencieusement. Aucun contournement du garde, transfert de média ou diffusion sans autorisation explicite. Respecter PUBLICATION-POLICY.md et la règle de PR pour film-chain et garde.

## Mise à jour de la passation
En fin de session, actualiser ce fichier avec date, SHA de travail, preuves, tickets, blocages et prochaine action concrète. Ne publier la mise à jour distante qu'avec autorisation. Ne pas dupliquer les rapports ou l'historique de PLAN.md.
