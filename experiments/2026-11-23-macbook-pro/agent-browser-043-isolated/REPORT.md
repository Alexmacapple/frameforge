# FrameForge — essai isolé d'agent-browser 0.43.0

Date : 23 novembre 2026, MacBook Pro Apple M2 Max. `npx --yes --package agent-browser@0.43.0` : **version locale globale 0.31.1 inchangée**.

## Motivation

La revue de `recording.rs` a établi que 0.31.1 envoie des captures d'écran toutes les 100 ms à FFmpeg en déclarant 10 fps sans horodatage de capture. La version récente utilise Chrome `Page.screencastFrame` et une sortie à cadence fixe 30 fps par défaut. Voir `../agent-browser-recording-source-review/REPORT.md`.

## Test exécuté

- Page TodoMVC React publique avec données fictives.
- `record start recording.webm --fps 30 --contact-sheet`.
- Trois actions et assertions DOM réussies : une tâche, deux tâches, puis première tâche terminée.
- `record stop` réussi.
- `ffprobe` : WebM **6,866 s**, **30 fps**, 172923 octets.
- Feuille de contact générée avec **quatre images sélectionnées**.
- Temps monotone entre début de la première action et fin des gestes + pauses : **5,397 s** ; il ne représente pas la durée totale d'enregistrement.

## Interprétation

**PASS** : la version récente est exécutable de manière isolée sur le MacBook Pro, sans remplacer l'installation 0.31.1 ; capture 30 fps et feuille de contact fonctionnent ; les résultats DOM sont observés.

**UNVERIFIED** : correspondance exacte entre événements DOM et timestamps vidéo, reproductibilité de l'essai, qualité de la vidéo, accessibilité et confidentialité. La durée 6,866 s ne prouve pas à elle seule une synchronisation correcte. Aucun export public frame-par-frame de `metadata.timestamp` n'a été démontré.

## Décision

**REUSE_EXISTING / EXP**. Avant de développer une couche de synchronisation, tester les garanties utiles de la version récente : qualité des gestes à 30 fps, éventuels diagnostics de frames et corrélation temporelle dans la même prise. Ne pas installer de skill, moteur ou orchestrateur. FF-06 et FF-08 restent ouverts.
