# FF-10 — Deuxième démonstration web : formulaire local

23 novembre 2026. Scénario choisi avec accord utilisateur : saisie du nom, saisie de l'adresse électronique, envoi et confirmation. **Statut : PASS capture et rendu de brouillon ; UNVERIFIED pour transfert du garde et recette humaine.**

## Réalisation

- Fixture HTML locale form.html, sans réseau applicatif ni données réelles : nom Camille Martin, adresse camille@example.test.
- Playwright/Chromium a exécuté les trois interactions. Résultat DOM observé : « Demande enregistrée pour Camille Martin. »
- Capture réelle du navigateur via Playwright ; fichier WebM local de 14,52 s. Conversion à 30 images/s et prolongement de la dernière image pour obtenir 16 s.
- Trois narrations françaises synthétisées localement avec la voix macOS Thomas, sous-titres SRT/VTT et transcription.
- Composition HyperFrames 0.8.33 et rendu local de brouillon : PASS, 16,000 s, 480 images à 30 images/s, vidéo et audio présents. Aucun média publié.
- Le premier essai de rendu signalait l'absence d'identifiants des éléments média. La composition a été corrigée avec des id stables et rendue à nouveau.

## Frontière des preuves

Le rendu a utilisé **la commande HyperFrames directe** pour constituer un brouillon expérimental, pas encore le wrapper de sortie FF-10 adapté au nouveau contrat. La réutilisation complète du garde reste UNVERIFIED. Le rendu ne prouve pas automatiquement la concordance perceptive des trois gestes et de la voix ; la recette humaine reste UNVERIFIED.

Les médias (capture, voix, MP4) sont conservés **localement uniquement** et ne sont pas ajoutés au dépôt. Les scripts et documents permettent d'examiner la méthode ; le script de capture contient un chemin absolu vers Playwright installé sur ce Mac et n'est pas encore portable.

**Décision : poursuivre par l'adaptation minimale du contrat de sortie au formulaire, puis la recette humaine de ce film exact.** Ne pas réutiliser l'approbation V5. FF-10 reste ouvert.
