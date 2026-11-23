# FrameForge — FF-06 / FF-08 : contrôle technique V3 et critère de synchronisation

Date : 23 novembre 2026. Cible : `../vertical-v3/media/prototype-v3.mp4` et `../vertical-v3/captions.srt`.

## Méthode exécutée

Le script `qa.py` utilise ffprobe pour lire durée et codecs, FFmpeg pour décoder intégralement la vidéo et détecter les silences audio (`-36dB:d=0.15`), et un parseur SRT minimal pour contrôler l'ordre, les bornes temporelles et l'absence de chevauchement. Les tests ont été exécutés sur le MacBook Pro.

## Résultats

- Durée : **9,500 s** ; codecs : **H.264 + AAC** ; décodage intégral : **PASS**.
- Trois sous-titres non chevauchants : **0,900–2,720 s**, **3,300–5,666 s**, **5,900–8,405 s**.
- Détection audio à seuil fixé : voix approximativement **0,900–2,616 s**, **3,300–5,553 s**, **5,900–6,313 s** puis **6,543–8,293 s** (pause interne dans la troisième phrase).
- Les sous-titres couvrent ces plages détectées ; cette concordance ne démontre ni la transcription exacte des mots ni la qualité perçue.

## Critère ±250 ms : hypothèse, non garantie

Le seuil de ±250 ms est **provisoire et non validé**. Les changements d'images de la V3 ont été précédemment estimés à environ 1,4, 3,7 et 6,4 s ; les phrases commencent à 0,9, 3,3 et 5,9 s, soit une anticipation approximative de 0,5, 0,4 et 0,5 s. Les changements d'images ne sont pas des repères événementiels certifiés. On ne peut donc pas déclarer un FAIL formel à ±250 ms, ni un PASS.

L'anticipation de la narration peut être éditorialement voulue : le seuil doit porter sur un événement défini (début de geste, résultat visible, mot-clé prononcé), et non sur deux signaux arbitrairement comparés.

## Revue indépendante FF-08

**NOT RUN** : écoute humaine de la voix, compréhension de la démonstration, lisibilité visuelle des résultats, exactitude de chaque phrase prononcée, informations visuelles essentielles, confidentialité image par image, et revue avec technologies d'assistance. Ne pas présenter ce contrôle automatique comme une revue indépendante.

## Verdict

- **PASS technique** : fichiers, codecs, décodage, structure et placement nominal des sous-titres, présence de plages audio.
- **UNVERIFIED** : synchronisation événementielle ±250 ms, fidélité éditoriale, accessibilité, confidentialité et qualité perceptive.
- **NO-GO** clôture FF-06/FF-08 et validation du MVP.
- **REUSE_EXISTING** : pas de besoin démontré d'un nouveau skill, moteur ou orchestrateur.

## Étape discriminante

Faire une revue humaine de la V3 et définir le point d'ancrage de chaque phrase (début du geste ou apparition du résultat). Tester ensuite ce point d'ancrage avec les mécanismes de capture récents. Ne pas multiplier les captures sans critère éditorial explicite.
