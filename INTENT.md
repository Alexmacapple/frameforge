# INTENT — Besoins et garanties

## Cas d'usage initial
À partir d'une application web de démonstration autorisée, produire une vidéo d'environ 30 secondes montrant trois interactions réelles, avec narration, sous-titres et rapport de vérification.

## Critères d'acceptation MVP
1. Le brief identifie public, message, source, autorisation et durée cible.
2. Trois interactions sont capturées et associées à leurs résultats observés.
3. La narration locale est générée et ses repères temporels sont conservés.
4. Les gestes sont alignés sur les repères de narration sans couper une phrase.
5. HyperFrames rend un MP4 décodable intégralement.
6. Un SRT et une transcription texte sont produits et comparés à la narration.
7. Un rapport distingue les contrôles exécutés, réussis, échoués et non exécutés.
8. Une seconde production est comparée à la première, avec différences expliquées.
9. Les données sensibles sont contrôlées avant toute diffusion ; aucun envoi externe implicite.
10. L'ensemble est pilotable en CLI et produit des rapports textuels accessibles.

## Invariants
- Pas de fonction présentée comme observée sans preuve.
- Pas de succès de rendu assimilé à une validation finale.
- Pas de transition qui cache une action ou un résultat déterminant.
- Pas de suppression silencieuse d'une scène en erreur.
- Pas de publication sans validation explicite.

## Questions ouvertes
- Formats et ratios prioritaires (16:9 initialement supposé).
- Politique des voix, langues et licences.
- Critères exacts de comparaison de deux rendus (identité binaire non exigée a priori).
- Confidentialité et conservation des médias de travail.
- Premier site et scénario de démonstration autorisés.

## Orientation produit confirmée (23 novembre 2026)
FrameForge est un studio vidéo généraliste. Le premier prototype est une démonstration web de 30 secondes ; montage de rushes et vidéos pédagogiques sont des extensions futures, non incluses dans le MVP.

## Décisions métier validées — grill-with-docs D1 à D16 (23 novembre 2026)
- **Exploration et preuves (D1, D4, D7, D8, D11, D14)** : une production peut commencer par l'exploration ; chaque affirmation filmée est reliée au geste, au résultat observable, à la source et au contexte. Une capture historique ne prouve pas l'état actuel ; vérifier sa pertinence avant validation sans recapture systématique. Un manifeste minimal référence les preuves originales. Statuts de preuve et de validation sont indépendants.
- **Échecs et temporalité (D2, D5, D9, D12, D15)** : exclure toute scène invérifiable du rendu validé ; conserver les scènes valides en brouillon si le film est incomplet, avec rapport d'échec. Reprendre les étapes invalides et revérifier les dépendances affectées. Adapter le montage à la durée réelle des gestes et des phrases, sans coupe ou accélération silencieuse. Tout repli technique est documenté et soumis aux mêmes garanties.
- **Validation et livraison (D3, D6, D10, D13, D16)** : vérifier les scènes puis le film ; l'approbation humaine explicite porte sur une version déterminée. Réévaluer les contrôles affectés et demander une nouvelle approbation après tout changement significatif. Le MVP complet comprend MP4, sous-titres, transcription, provenance et rapport de recette. Un rendu techniquement réussi n'autorise jamais à lui seul la diffusion.

Le vocabulaire métier est défini dans [GLOSSARY.md](GLOSSARY.md). Ces décisions ne prouvent pas la faisabilité technique.
