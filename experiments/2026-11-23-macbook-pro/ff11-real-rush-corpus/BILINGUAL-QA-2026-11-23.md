# FF-11 — Recette bilingue EN/FR, premier passage

Date : 23 novembre 2026. Montage local inchangé : clips/earth-nisar-draft.mp4, SHA-256 6d7f1f3758cc9c48b2507e2a6c73a95b4a1ecc89b65b44fbad7787fc29a86204.

## Travail exécuté

- Deux reconnaissances vocales anglaises du passage NISAR (tiny.en et small.en). Les deux convergent sur la deuxième phrase. Le premier modèle proposait « short length changes », le second « shoreline changes ». Le second résultat est plus plausible, mais reste UNVERIFIED à l'écoute.
- Transcription anglaise de travail issue de small.en, décalée de +6 s pour les repères temporels du montage final.
- Traduction française de travail, sans ajout de contenu à la phrase tronquée.
- Quatre fichiers de sous-titres : captions-speech-en-DRAFT.srt, captions-speech-fr-DRAFT.srt, et leurs versions VTT.
- Transcription parallèle : transcript-bilingual-DRAFT.md. Manifeste de provenance et SHA-256 : bilingual-checks.json.
- Contrôles automatiques des deux plages : 6,000–8,800 s et 8,800–12,800 s, sans chevauchement. PASS structurel.
- La vidéo source n'a pas été rendue à nouveau, ses médias et son audio n'ont pas été modifiés.

## Critères de recette

| Critère | Résultat |
| --- | --- |
| Deux pistes de sous-titres EN et FR | PASS fichiers |
| Synchronisation déclarée des plages | PASS structurel |
| Vidéo source conservée | PASS SHA-256 |
| Fidélité de l'anglais à la voix | UNVERIFIED ; deux ASR, aucune vérification humaine mot à mot |
| Exactitude de la traduction française | DRAFT ; nécessite écoute et relecture |
| Affichage des pistes SRT/VTT dans le lecteur final | NOT TESTED |
| Non-concurrence avec les légendes descriptives incrustées | FAIL pour une livraison sans correction : elles sont toujours présentes dans le MP4 |
| Accessibilité des sous-titres et lisibilité visuelle | UNVERIFIED |
| Droits de diffusion | UNVERIFIED |

## Points à traiter avant validation

1. Écouter de 6 à 13 secondes et confirmer les mots, en particulier « shoreline changes », la formulation des radars et la fin tronquée.
2. Revoir le français en fonction de cette écoute.
3. Pour une version livrable, **éviter de superposer les sous-titres de parole aux légendes visuelles déjà incrustées** : produire une version sans ces légendes, puis tester l'affichage des pistes sélectionnables. Ne pas présenter le SRT descriptif comme transcription de la parole.
4. Vérifier les droits des deux extraits NASA et effectuer la recette audiovisuelle humaine.

**Verdict : PARTIAL, FF-11 ouvert, NO-GO diffusion.** Aucun nouveau moteur de traduction ou de sous-titrage n'est nécessaire à ce stade.
