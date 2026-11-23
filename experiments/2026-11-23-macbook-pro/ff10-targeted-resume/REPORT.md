# FF-10 — Pilote de correction ciblée et reprise après interruption

Date : 23 novembre 2026. MacBook Pro. **Expérience sur copie ; ne constitue pas une validation humaine de la V5.**

## Hypothèse et périmètre

Tester la possibilité de modifier **uniquement la présentation du sous-titre 2** sans régénérer la capture, la narration Kokoro ni les sous-titres 1 et 3, puis interrompre un rendu et le relancer. Le texte parlé reste identique. Référence : `../vertical-v5-kokoro/media/prototype-v5.mp4`, SHA-256 `779cadcd5e53be7cd85bca7a38b526a0b0653f312cb236599cf46c80b2526cc3`.

**Correction de test, non approuvée humainement** : sous-titre 2 réparti sur deux lignes après « apparaît. ». Même texte et mêmes horodatages. Les sous-titres 1 et 3 et la transcription restent inchangés. Le changement est effectué dans `index.html`, `captions.srt` et `captions.vtt` ; aucun autre élément métier modifié.

## Protocole et preuves

1. Copie indépendante du projet V5. `input-comparison.json` atteste les **SHA-256 identiques** de `capture.webm` et des trois pistes `voice1/2/3.m4a`. `transcript.txt` est identique.
2. Premier rendu HyperFrames 0.8.33 démarré puis **interrompu en cours d'exécution** (processus terminé par signal ; aucun MP4 achevé). Voir `interruption.json` et `interrupted-render.log`.
3. Second rendu complet à partir des **mêmes entrées** : `media/resumed.mp4`. Le moteur a refait le rendu ; **aucune reprise intra-rendu ou cache réutilisé n'a été démontré**. Voir `resumed-render.log`.
4. Contrôle FFmpeg : **PASS**, H.264/AAC, 16,166667 s, **485 images**. SHA-256 du résultat `abd531d8faf3f8fcfb940a5996a43ce576f521a85422ab219372a16fc7fb76a9`.
5. `output-comparison.json` : audio décodé en PCM stéréo 48 kHz, **SHA-256 identique** entre V5 et reprise. Les **485 images** ont été comparées par hash de trames décodées : 182 identiques et 303 différentes, dont 187 hors de la plage du sous-titre 2. **Ce n'est donc pas une préservation pixel à pixel du rendu.**
6. Analyse PSNR (`psnr.txt`) : hors plage modifiée, les différences observées sont majoritairement faibles (avant : minimum 61,61 dB ; après : médiane 60,12 dB, avec une image sous 40 dB à la frontière). Les images à 6, 8, 11 et 14 secondes sont comparées dans `side-by-side.png` : le changement de mise en page est visible à 8 s, les autres états semblent préservés sur ces échantillons. **Les PSNR élevés ne remplacent pas une recette visuelle exhaustive.**

## Résultats et limites

| Garantie | Verdict | Preuve / réserve |
| --- | --- | --- |
| Modification ciblée du sous-titre 2 dans les sources | PASS | Trois fichiers éditoriaux modifiés, texte inchangé |
| Conservation des quatre médias sources | PASS | SHA-256 identiques |
| Conservation de la transcription | PASS | SHA-256 identique |
| Interruption effective d'un rendu | PASS | Processus interrompu, aucun artefact complet |
| Nouveau rendu après interruption | PASS | MP4 complet, 485 images, décodage intégral |
| Audio final inchangé | PASS mesuré | SHA-256 PCM identique |
| Pixels hors sous-titre 2 inchangés | FAIL pour identité stricte | 187 images décodées différentes hors plage, écarts principalement faibles |
| Absence de régression perceptive ailleurs | PARTIAL | Quatre comparaisons visuelles, pas une revue humaine exhaustive |
| Reprise à partir d'un checkpoint interne | NOT DEMONSTRATED | Rendu intégral relancé ; aucune récupération partielle |
| Protection d'un choix **humain** approuvé | NOT TESTED | V5 utilisée comme témoin provisoire, aucun verrou humain exercé |
| Confidentialité, droits, approbation de diffusion | UNVERIFIED | Hors de ce pilote |

## Décision

**Expérience utile, mais FF-10 reste ouvert.** La reprise par relance complète fonctionne, les médias sources et l'audio sont préservés, mais ni la reprise incrémentale, ni la protection d'un élément humain verrouillé ne sont prouvées. Ne pas inventer un moteur de cache : tester une vraie correction approuvée et comparer le coût de relance avant de construire un mécanisme supplémentaire. FF-08/FF-09 restent des dépendances non closes.

Ce dossier contient le rendu de reprise, les manifests, logs, mesures et planche de comparaison. Les sources de la V5 originale ne sont pas modifiées.

**Hygiène des preuves :** les images temporaires générées par HyperFrames pendant l'essai interrompu ne sont pas des livrables ni un cache validé. Elles ont été retirées du suivi Git dans un commit correctif ; les journaux, manifests, comparaison et MP4 de reprise sont conservés. Le premier commit d'expérience les avait incluses par erreur.
