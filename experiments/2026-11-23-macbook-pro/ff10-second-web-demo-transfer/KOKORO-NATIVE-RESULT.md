# FF-10 — Résultat : voix Kokoro en entrée directe du rendu gardé

23 novembre 2026, MacBook Pro. Protocole : KOKORO-NATIVE-PROTOCOL.md. Révision de départ : 2c9223c. HyperFrames 0.8.33, FFmpeg 9.0.1, Python 3.14.7.

## Verdict

**PASS technique** : `python3 render_guarded.py` (ou `npm run render`) dans `form-pilot-kokoro/` produit en un seul rendu gardé le film du formulaire avec la voix Kokoro. Plus de rendu intermédiaire Thomas ni de remplacement de piste.

**UNVERIFIED** : écoute humaine de ce film exact. **NO-GO** : promotion générale et toute diffusion. FF-10 reste ouvert.

## Film produit

- `form-pilot-kokoro/media/form-kokoro-native.mp4`, local, non versionné.
- SHA-256 `0d9d0c9cb5d04f0d947b946f4072a84112e6cd2b0e987bde9490a567e7f392a5`.
- 16,000 s, 480 images, 30 images par seconde en moyenne, H.264 1920×1080, AAC 48 kHz stéréo. Décodage intégral : PASS.
- Ce n'est **pas** l'empreinte `f4552189…` approuvée à l'écoute : la piste approuvée était en AAC 24 kHz mono.

## Preuves exécutées

- **Images identiques à la version approuvée.** Empreinte du flux vidéo : `86a966e4…eb52`, égale à celle de `form-kokoro-guarded.mp4`.
- **Son conforme aux clips d'entrée.** Corrélation par clip à son repère : 0,99966 à 1,5 s, 0,99979 à 5,2 s, 0,99973 à 10,0 s.
- **Son proche de la piste approuvée.** Corrélation 0,99968, rapport signal sur écart 32,0 dB, écart de niveau −0,01 dB. C'est une mesure, pas une écoute.
- **Reproductibilité sur ce Mac.** Brouillon témoin direct et deux rendus gardés successifs : même empreinte SHA-256.
- **Refus du nom déjà pris.** Second lancement sans déplacer la sortie : `output_already_exists`, code 2.
- **Tests.** 10 sur 10 PASS dans `test_kokoro_guard.py`. Les 9 tests de `form-pilot/` passent toujours ; aucun fichier suivi de `form-pilot/` n'est modifié.
- **État avant.** Le validateur de `form-pilot/` rejetait tout film Kokoro (`form_output_audio_changed`) et acceptait le film Thomas. Le nouveau fait l'inverse : film Thomas rejeté (`kokoro_output_audio_changed`).
- **Tests de mutation.** Contrôle du flux vidéo, contrôle du son et contrôle des clips neutralisés tour à tour : à chaque fois un test échoue (`test_reencoded_video_with_kokoro_audio_rejected`, `test_thomas_voiced_film_rejected`, `test_altered_kokoro_clip_rejected`). Garde restauré à l'identique ensuite.
- **Rendu sans avertissement HyperFrames**, après ajustement des créneaux audio à la durée réelle des clips (2,767 s, 2,948 s, 4,5 s).

## Ce que le chantier a révélé

- **Accélération non consignée dans la version approuvée.** Les phrases 1 et 2 sont accélérées de 6 % et 8 % par FFmpeg (`atempo`), en plus de la vitesse Kokoro 1,2. Recette retrouvée par balayage et prouvée par corrélation (0,9999). Elle est désormais écrite dans `prepare_inputs.py`. La version a été approuvée à l'écoute avec cette accélération ; la décision de la conserver appartient à l'approbateur.
- **Synthèse Kokoro non reproductible sans graine.** Deux synthèses du même texte diffèrent à l'octet. Avec `torch.manual_seed(0)`, deux passages sont identiques. Les clips approuvés ne peuvent donc pas être régénérés : ils sont figés par empreinte.
- **Sous-titres plus longs ou plus courts que la voix de quelques centièmes.** Les sous-titres gardent les durées de la voix Thomas (2,78 s, 2,96 s, 4,57 s) pour préserver les images approuvées ; la voix Kokoro dure 2,768 s, 2,949 s et 4,5 s. L'écart maximal est de 0,07 s sur la troisième phrase.

## Limites

- Aucune synthèse pendant le rendu, aucun nouveau texte : le garde consomme trois clips figés.
- Les clips sources (`form-pilot/media/kokoro-fast1..3.wav`) et les médias restent locaux. Sans eux, la préparation refuse et rien n'est reproductible ailleurs.
- Les empreintes des clips dérivés dépendent de FFmpeg 9.0.1 ; reproductibilité hors de ce Mac : UNVERIFIED.
- Le garde n'est pas obligatoire : un rendu HyperFrames direct reste possible. Les références sont modifiables par qui peut modifier le code.
- `form-pilot/finalize_kokoro.py` reste en place comme trace de la version approuvée ; ce pilote ne l'utilise plus.
- Cadence moyenne contrôlée, pas cadence constante. Visibilité des trois gestes et compréhension sans image : non réévaluées ici.

## Suite proposée

Écouter `form-kokoro-native.mp4` et consigner l'approbation ou le refus de cette empreinte exacte.
