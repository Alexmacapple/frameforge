# FF-12 — Narration française et sous-titres, recette technique

Date : 23 novembre 2026. **Statut : DRAFT ; recette humaine de compréhension sans image non effectuée.**

## Fichier local

local/ff12-narrated-fr-subtitled-DRAFT.mp4 sur le MacBook Pro. Fichiers annexes locaux : ff12-voice-1.wav, ff12-voice-2.wav, ff12-captions-fr.srt, ff12-captions-fr.vtt et ff12-narration-fr.txt.

Le montage vidéo d'origine local/ff12-independent-cuts-13s5-DRAFT.mp4 est conservé. La vidéo H.264 est copiée sans réencodage dans le nouveau MP4 ; les coupes ne sont pas modifiées.

## Narration effectivement synthétisée avec Kokoro ff_siwis

- Plan 1, audio à 0,350 s (durée synthétisée 5,075 s) : « La Lune passe devant le Soleil. Le satellite S D O observe cette occultation. »
- Plan 2, audio à 8,450 s (durée synthétisée 4,150 s) : « Depuis l’espace, D S C O V R montre son ombre sur la Terre. »

Les sigles sont espacés pour favoriser leur épellation par la synthèse. La qualité réelle de leur prononciation reste UNVERIFIED par écoute humaine.

## Sous-titres

SRT/VTT en français et piste mov_text fra intégrée au MP4. Repères : 0,350–5,425 s et 8,450–12,600 s. Ces repères suivent la durée du TTS ; ils n'ont pas été vérifiés perceptivement.

## Contrôles techniques

| Contrôle | Résultat |
| --- | --- |
| Vidéo conservée | H.264, 405 images, 13,500 s |
| Piste audio française | AAC, 634 paquets, présente sur les deux plans |
| Sous-titres sélectionnables | mov_text, langue fra, détectés par ffprobe |
| Décodage FFmpeg intégral | PASS |
| Niveaux audio sur les plages parlées | Moyennes entre -20,6 et -23,3 dB sur les échantillons |
| SHA-256 MP4 | 26d5242151aa1b4288f8f64e377d7acd443e5d3a4646f7c249085fd3b5917b66 |
| Compréhension sans image | UNVERIFIED |
| Synchronisation perceptive des SRT | UNVERIFIED |
| Prononciation des sigles | UNVERIFIED |
| Droits de diffusion | UNVERIFIED |

La source NASA B comporte des bandeaux anglais incrustés et représente plusieurs observations instrumentales ; le film ne doit pas être présenté comme une prise continue. La narration est une proposition de description, pas une garantie de précision scientifique supplémentaire.

## Prochaine décision

Demander à l'utilisateur d'écouter le MP4 sans image et de vérifier la clarté du récit, la prononciation des sigles et la fluidité de la voix. Ensuite, vérifier la piste de sous-titres dans QuickTime. Aucun nouveau moteur, aucune diffusion des médias, aucune clôture de FF-12.
