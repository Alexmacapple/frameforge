# FF-10 — Préservation d'un sous-titre évalué positivement et relance

Date : 23 novembre 2026. **Verdict : PASS technique sur la correction ciblée et la préservation des flux ; NOT DEMONSTRATED sur reprise incrémentale et verrou humain généralisé.**

## Référence et protocole

Protocole figé avant test : PROTOCOL.md au commit 98fef0f. Référence : film FF-12 narré local, déjà évalué positivement par l'utilisateur (voix et sous-titres dans QuickTime). **La validation ne portait pas sur chaque caractère et n'a pas établi un verrou formel.**

- Entrée : ff12-independent-cut-v2/local/ff12-narrated-fr-subtitled-DRAFT.mp4.
- Sous-titre 2 conservé intégralement ; sous-titre 1 modifié uniquement sur le retour à la ligne.
- Nouvelle sortie locale : local/ff10-targeted-resumed.mp4.
- Outils : FFmpeg/ffprobe ; aucun nouveau moteur ni cache.

## Exécution

1. Baseline SRT copiée et gelée. Contrôle avant rendu : sous-titre 2 identique octet pour octet ; sous-titre 1 contient les mêmes mots avec un retour à la ligne déplacé.
2. Première tentative FFmpeg avec entrée ralentie pour rendre l'interruption reproductible, terminée par SIGTERM après environ deux secondes ; code de sortie 255 et artefact partiel de 482 Ko. Journal et preuve locale dans interruption.log et interruption.txt. **Cette interruption est artificiellement ralentie, non une panne réelle.**
3. Relance complète FFmpeg sans cache ; MP4 de 13,500 s, 405 images, 634 paquets audio et sous-titres mov_text.
4. Décodage FFmpeg intégral sans erreur. Extraction du SRT final, comparaison avec la référence.
5. Flux vidéo H.264 et audio AAC copiés sans réencodage. Comparaison des SHA-256 des flux élémentaires : identiques pour vidéo et audio.
6. Deuxième sous-titre extrait : mêmes lignes, texte et timecodes que la baseline ; premier sous-titre : mêmes mots et timecodes, lignes modifiées.

## Verdicts

| Garantie | Verdict |
| --- | --- |
| Préserver le sous-titre 2 évalué positivement | PASS exact sur SRT extrait |
| Changer uniquement la présentation du sous-titre 1 | PASS source et extraction |
| Préserver les flux vidéo et audio | PASS exact par SHA-256 |
| Interrompre une exécution | PASS sur tentative ralentie |
| Relancer et obtenir un MP4 complet | PASS |
| Reprendre au milieu du rendu à partir d'un checkpoint | NOT DEMONSTRATED |
| Empêcher un agent de modifier un élément verrouillé | NOT TESTED : aucun verrou formel |
| Qualité perceptive du nouvel habillage | UNVERIFIED : pas de recette humaine du nouveau MP4 |
| Autorisation de diffusion | UNVERIFIED : médias NASA locaux |

## Décision

**REUSE_EXISTING.** La combinaison des outils existants suffit à préserver des flux et un sous-titre témoin au cours d'une modification ciblée et d'une relance. Il n'y a pas de preuve justifiant un moteur de cache ou un orchestrateur. Ne pas déclarer FF-10 entièrement clos sur la base de ce seul test : la garantie de correction humaine verrouillée reste à éprouver. Ne pas écraser le film FF-12 évalué positivement.

Le film et les données temporaires restent locaux ; seuls le protocole, le rapport et les résultats de contrôle sont publiés.
