# Veille : ffmpeg-skill, analyse pour FrameForge (ticket 68)

Date : 28 novembre 2026. Lecture seule : rien n'a été installé ni exécuté, aucun script amont n'a été lancé.

## Verdict

Ne pas installer, ni le skill ni son serveur MCP. Le verdict initial du ticket, EXTRACT_ONLY, est confirmé : trois idées de contrôle sont à reprendre avec le FFmpeg que nous avons déjà, sans une ligne de code amont. Une quatrième sert la décision du ticket 67.

## Révisions figées

- `kajisho5/ffmpeg-skill` : version `v4.26.0`, commit `53b1be1ec390801d841da8e6e7bd28c9dd002dad` (28 novembre 2026, 12 h 29 UTC), tête de `main` à la lecture. Licence MIT, lue dans `LICENSE`.
- FrameForge : `main` à `d16a2d7`.

## Ce qu'est l'outil

Un skill d'agent qui remplace l'appel direct à FFmpeg par 41 scripts Python (42 fichiers, `crop` étant un alias), tous avec sortie JSON, essai à blanc et relecture de la sortie. Bibliothèque standard seule, FFmpeg 6.1 ou plus. Un script d'orchestration, `render.py`, enchaîne les étapes d'un montage décrit en JSON ; un serveur MCP expose les mêmes outils.

## Contraintes et hypothèses

- **Rythme de publication.** 30 versions en deux jours, produites automatiquement à chaque fusion ; quatre le 28 novembre. La `v4.26.0` change un comportement par défaut dans une version mineure : `join.py` joignait avec un fondu de 0,5 s, il joint désormais bout à bout. Tout usage devrait épingler un commit.
- **Dépôt jeune et très actif.** Créé le 3 septembre 2026, environ 1 000 commits, un auteur principal, une part importante de commits signés par des agents. Environ 2 000 tests et du fuzzing sont présents dans l'arbre ; aucun n'a été exécuté ici.
- **Consigne contraire à notre garde.** Son `SKILL.md` demande à l'agent de ne jamais lancer `ffmpeg` ou `ffprobe` directement. Notre garde le fait, par conception, avec des commandes figées.
- **Installation globale.** L'installeur copie le skill dans `~/.claude/skills/ffmpeg-skill` ; il n'ajoute ni hook ni réglage. Sa commande `setup` peut lancer `brew install ffmpeg-full`, donc changer le FFmpeg de la machine : c'est exactement ce que le ticket 73 demande d'éviter.
- **Réseau.** Aucun appel réseau trouvé dans les scripts lus ; chaque entrée FFmpeg est limitée au protocole `file`. Exception documentée : les moteurs de transcription téléchargent leur modèle. Non essayé sous `sandbox-exec`.
- **Ticket amont à surveiller.** Le ticket 781 du dépôt propose un relevé local, sur option, de l'usage des outils ; rien de tel dans le code à ce commit.

## Verdict par composant

Pour chacun : le besoin, ce que nous avons, ce qui manque, la preuve, et le verdict.

1. **Contrôle d'intégrité d'un film rendu** (`check.py`, `probe.py`). Nous avons plus strict : le garde compare images, son, paquets et étiquettes à une référence, à l'octet près. `check.py` n'a pas d'attente sur un nombre d'images ou une durée exacte. **REUSE_EXISTING.**
2. **Contrôle du contenu d'un film neuf** (`check.py --content`). Besoin : voir une piste muette, un écran noir, une image figée, un horodatage répété, avant l'écoute humaine. Nous n'avons rien de tel : la fiche contrôle la durée des clips (`measured_audio`), pas leur niveau ; le garde fige ce qu'on lui donne, clip muet compris. Lacune déduite du code, non démontrée par un essai. Les filtres en jeu (`silencedetect`, `blackdetect`, `freezedetect`, lecture des `pts`) sont ceux de FFmpeg. **EXTRACT_ONLY**, priorité 1.
3. **Niveau sonore** (`loudness.py`, mesure dans `check.py`). Besoin : des clips et des films au même niveau, question devenue concrète avec deux voix (Kokoro et Libra-TTS) dont rien ne dit qu'elles sortent au même niveau. Nous ne mesurons pas le niveau. La mesure se fait par `loudnorm` avec `print_format=json`, sans rien modifier. La normalisation, elle, change le son : hors de question sans validation. **EXTRACT_ONLY pour la mesure**, priorité 1 ; **REJECT pour la normalisation automatique.**
4. **Présence effective de la voix** (`silence.py --list`). Même besoin que le point 2, côté son. Mesure seule, sans coupe. **EXTRACT_ONLY**, regroupé avec le point 2.
5. **Comparaison de deux films** (`check.py --compare`, SSIM et PSNR). Besoin : chiffrer l'écart entre le rendu du Mac Studio et celui du MacBook Pro, que le garde constate sans le mesurer (ticket 67). Les filtres `ssim` et `psnr` sont dans FFmpeg. **EXPERIMENT**, au service de la décision 67.
6. **Version de FFmpeg dans la clé de cache** (`render.py`). L'idée : un résultat n'est réutilisable que pour la version de FFmpeg qui l'a produit. Notre reçu de rendu ne note pas cette version, alors que le film la porte (ticket 73). **EXTRACT_ONLY**, priorité 2.
7. **Protection des sources et sorties partielles** (`_common/runner.py`). Refus d'écraser, fichier temporaire puis renommage, verrou, délai : nos outils font déjà chacun de ces refus (capture, synthèse, garde, reçu de rendu). **REUSE_EXISTING.**
8. **Montage : découpe, assemblage, transitions** (`cut.py`, `join.py`, `render.py`). FrameForge compose avec HyperFrames et ne découpe pas. Le besoin n'existerait que si le montage de rushes (thème 11, ticket 48) reprenait. La rupture de la `v4.26.0` montre le risque d'en dépendre. **REJECT aujourd'hui, WATCH pour le thème 11.**
9. **Sous-titres et transcription** (`caption.py`). HyperFrames incruste nos sous-titres. La transcription repose sur un moteur Whisper installé à part : c'est ce moteur, pas ffmpeg-skill, qui intéresse le ticket 61. **REJECT.**
10. **Planche d'images** (`look.py`). Nous avons `contact_sheet.py`. Ses horodatages demandent le filtre `drawtext`, absent de notre FFmpeg comme du leur sans `ffmpeg-full`. **REUSE_EXISTING.**
11. **Revue humaine en page locale** (`_review.py`). Elle sert à éditer un projet de montage, pas à approuver un film ; hors contrat, non exposée par le serveur MCP. **REJECT.**
12. **Skill complet et serveur MCP.** Coût : 6 Mo de code tiers dans le contexte de l'agent, une consigne qui contredit le garde, un rythme de publication impossible à suivre. Bénéfice : aucun des points ci-dessus n'en a besoin. **REJECT.**

## Suites proposées, sans ticket ouvert

Le ticket 68 demande une contre-revue indépendante et une décision d'Alex avant tout nouveau ticket. Ni l'une ni l'autre n'est faite. Par ordre d'intérêt :

1. Une mesure de contenu sur le brouillon témoin et sur chaque clip de voix : niveau sonore, silence, écran noir, image figée. Critère d'acceptation : un clip muet et un film à l'image figée, fabriqués pour l'essai, sont refusés ; les films approuvés passent.
2. Un essai chiffré pour le ticket 67 : SSIM entre le film 47 rendu sur chaque Mac. Critère : un chiffre par plage de texte, qui dit si l'écart est visible.
3. La version de FFmpeg notée dans le reçu de rendu.

## Limites de cette analyse

- Le relevé du dépôt a été délégué à un agent de lecture, puis recontrôlé par moi sur sept points : commit et notes de la `v4.26.0`, changement de `join.py`, commande de mesure du niveau, refus d'écraser, délai par défaut, consigne « never run raw ffmpeg », clé de cache. Le reste repose sur ce relevé.
- Non lus en détail : `verify.py`, `cut.py`, `caption.py`, `join.py`, `export.py`. Ce que `verify.py` contrôle vient de la documentation, pas du code.
- Rien n'a été exécuté : ni les tests amont, ni un seul script. Les chiffres du README amont ne sont pas vérifiés.
- La lacune du point 2 est déduite de la lecture de `check_manifest.py` et du garde, pas démontrée par un clip muet.
- Valable pour ce commit seulement : le dépôt change plusieurs fois par jour.
