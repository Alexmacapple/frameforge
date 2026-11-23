# FrameForge — dossier de revue perceptive V3

Date : 23 novembre 2026. Vidéo source : `../vertical-v3/media/prototype-v3.mp4` (9,5 s), SHA-256 `bda462a57d8a0bd99bcf3e8cfd023eb77e71742fdc0dec95776fd8132f51da20`.

## Matériel préparé

- `contact-sheet.png` : huit images extraites du MP4 à 0,5, 1,6, 2,9, 3,8, 5,5, 6,5, 8,6 et 9,2 s.
- `stills/` : les huit images individuelles, en résolution d'origine.
- `narration.wav` : piste audio extraite sans modification du contenu parlé.
- Sous-titres, transcription et MP4 source : `../vertical-v3/`.
- Décodage intégral FFmpeg et empreinte SHA-256 : PASS.

## Script de contrôle indépendant (à réaliser)

La personne qui examine la vidéo doit regarder le film entier, écouter la voix, puis vérifier :

1. **Geste 1** : voit-on la création de « Première tâche » et le résultat, sans ambiguïté ?
2. **Geste 2** : voit-on la création de « Deuxième tâche » et le résultat ?
3. **Geste 3** : voit-on l'achèvement de la première tâche et le changement d'état ?
4. **Narration** : les trois phrases prononcées correspondent-elles exactement au transcript et au sens de l'image ? Sont-elles compréhensibles et correctement placées ?
5. **Sous-titres** : texte exact, durée lisible, position non masquante et accord perceptif avec la voix ?
6. **Accessibilité** : la narration permet-elle de comprendre les résultats essentiels sans voir l'écran ? Le film contient-il des informations visuelles essentielles non restituées ?
7. **Confidentialité** : inspecter toutes les scènes pour des données personnelles, identifiants, URL sensibles ou notifications.
8. **Rythme** : l'enchaînement des trois gestes est-il intelligible, sans coupe ou pause gênante ?

Consigner pour chaque point : PASS, FAIL ou UNVERIFIED, horodatage, observation concrète et action corrective. La revue doit porter sur le film complet, pas seulement sur les huit images.

## Limites et décision

**PASS technique** : extraction d'images et audio, décodage, empreinte source.

**NOT RUN** : écoute humaine indépendante, lecture visuelle critique du film complet, validation du texte effectivement prononcé, contrôle de confidentialité exhaustif, validation d'accessibilité avec technologies d'assistance.

**NO-GO** : ne pas déclarer FF-08 validée ni le MVP prêt à diffusion. Le seuil ±250 ms reste une hypothèse non validée ; il faut d'abord préciser si chaque phrase annonce l'action ou décrit son résultat.

**REUSE_EXISTING** : aucune nouvelle dépendance, skill ou orchestration.
