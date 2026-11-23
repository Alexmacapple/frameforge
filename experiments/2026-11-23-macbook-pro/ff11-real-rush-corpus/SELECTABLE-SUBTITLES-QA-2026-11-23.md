# FF-11 — Sous-titres sélectionnables EN/FR

Date : 23 novembre 2026. Verdict technique : PASS. Verdict éditorial et diffusion : UNVERIFIED / NO-GO.

## Objectif et exécution

Supprimer les deux légendes descriptives incrustées par FrameForge, conserver la parole anglaise originale et ajouter deux pistes de sous-titres sélectionnables (anglais et français).

- HyperFrames 0.8.33 : copie de la composition sans les deux éléments caption1/caption2, rendu local selectable-subtitles/clean-no-baked.mp4.
- FFmpeg 9.0.1 : multiplexage des deux SRT brouillons en pistes mov_text avec métadonnées eng et fra.
- MP4 final local : selectable-subtitles/ff11-en-fr-selectable-DRAFT.mp4, 13 s, 390 images H.264, AAC et deux pistes de sous-titres.
- Les deux pistes ont été extraites à nouveau du MP4 : texte et repères 6,000–8,800 s et 8,800–12,800 s récupérés.
- Audio PCM 48 kHz stéréo strictement identique avant/après multiplexage : SHA-256 528b3ab21e95d143eb7f237d65ca3b486cca6e0ab8730fcbf03a30f83701d546.
- Décodage intégral FFmpeg PASS ; planche de vérification visuelle locale selectable-subtitles/clean-preview.jpg aux secondes 2, 7 et 10 sans bandeaux descriptifs FrameForge.

## Verdicts

| Garantie | Verdict |
| --- | --- |
| Deux sous-titres sélectionnables intégrés dans MP4 | PASS structurel |
| Pistes récupérables, langues et repères vérifiés | PASS |
| Audio conservé | PASS SHA-256 PCM |
| Légendes descriptives FrameForge retirées | PASS sur source et échantillons |
| Absence de textes NASA incrustés dans rushes originaux | NOT GUARANTEED |
| Activation des pistes dans QuickTime et avec VoiceOver | UNVERIFIED |
| Fidélité de la transcription anglaise et traduction française | UNVERIFIED : brouillons |
| Synchronisation et lisibilité perceptives | UNVERIFIED |
| Droits de diffusion des rushes NASA | UNVERIFIED |

## Reproduction

Dans le dossier local selectable-subtitles, exécuter :

    ffmpeg -i clean-no-baked.mp4 -i ../captions-speech-en-DRAFT.srt -i ../captions-speech-fr-DRAFT.srt -map 0:v:0 -map 0:a:0 -map 1:0 -map 2:0 -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=eng -metadata:s:s:1 language=fra -disposition:s:0 0 -disposition:s:1 0 ff11-en-fr-selectable-DRAFT.mp4

## Décision

REUSE_EXISTING : HyperFrames et FFmpeg suffisent. Ne pas ajouter d'éditeur ni de moteur. La vidéo et les médias NASA restent uniquement sur le MacBook Pro, les sources de composition et le rapport seuls sont versionnés. La version n'est pas validée pour diffusion.

Prochaine validation : ouvrir le MP4 dans QuickTime, activer alternativement les sous-titres anglais et français, tester avec VoiceOver, écouter et corriger mot à mot l'anglais puis la traduction. FF-11 reste ouvert.
