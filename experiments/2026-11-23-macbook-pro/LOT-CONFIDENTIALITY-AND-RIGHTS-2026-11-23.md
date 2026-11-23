# Confidentialité et droits du lot — films du formulaire et de la réservation

23 novembre 2026, MacBook Pro. Suite de la première expérience de la feuille de route (issue 13) : vérifier le lot, droits et confidentialité inclus. Relevé établi par un agent. **Ce document n'est pas un avis juridique et n'autorise aucune diffusion.**

Films examinés, tous deux approuvés à l'écoute et au visionnage :

- formulaire, `ab040730a5bdc4bb36e77be4a7b22da067dd3da2bfaddd436c5a636f7b567125` ;
- réservation de salle, `9c834228ae4db81dda154f5bf62e3bfc8fd3ac4012f9f64bbfddfcc29dfbf543`.

## Confidentialité des films et de leurs fichiers

- **Étiquettes des fichiers MP4 : PASS.** Conteneur : marque du format, version de l'encodeur (`Lavf63.1.101`), `hyperframes_version` et `hyperframes_renderer`. Flux : langue indéfinie, noms de gestionnaires génériques, `Lavc63.1.101 libx264`. Aucune date, aucun auteur, aucun chemin.
- **Chaînes de texte dans les fichiers MP4 : PASS.** Aucune chaîne de six caractères ou plus n'évoque un chemin du poste, un nom d'utilisateur ou un secret (recherche de `/Users/`, du nom d'utilisateur, `.local`, `macbook`, `Claude`, `password`, `token`, `secret`).
- **Sous-titres, transcription et composition : PASS.** Mêmes recherches, aucun résultat.
- **Images : PASS sur les états examinés.** Seules des données fictives apparaissent (Camille Martin, `camille@example.test`, salles Cèdre, Érable, Tilleul) ; ni barre de navigateur, ni autre fenêtre, ni notification. Deux planches de huit images lues par l'agent ; les images ne changent qu'aux instants des gestes. Chaque image du film n'a pas été regardée une à une.
- **Seule adresse électronique présente** dans les fichiers suivis : `camille@example.test`, fictive, sur un domaine réservé aux essais.

## Ce que le dépôt public expose, hors films

Le dépôt est public. Deux expositions ne viennent pas des films :

- **Dix fichiers suivis contiennent un chemin du poste de travail**, donc un nom d'utilisateur : trois scripts de `ff08-ff10-followup/`, trois fichiers de résultats et deux journaux de rendu des pilotes FF-10, `form-pilot/capture.cjs` et `film-chain/capture_lib.cjs`.
- **Les 151 commits portent une adresse électronique personnelle d'auteur**, lisible par quiconque clone le dépôt.

Aucun des deux n'est un secret, et aucun ne figure dans un film. Les retirer de l'historique demanderait de le réécrire, opération destructive qui n'est pas proposée ici. Pour la suite, deux gestes simples existent : lire le chemin de Playwright dans une variable d'environnement, déjà prévue par `capture_lib.cjs` (`FF_PLAYWRIGHT`), et configurer l'adresse « noreply » de GitHub pour les prochains commits. Décision à prendre par Alex.

## Droits

Ce qui est établi par une source, et ce qui ne l'est pas.

- **Pages filmées** : écrites pour le projet, dans un dépôt sous licence MIT. Données fictives.
- **Modèle de voix Kokoro-82M** : la fiche du modèle annonce des poids sous licence Apache 2.0. Le paquet `kokoro` 0.9.4 installé déclare la même licence dans ses métadonnées.
- **Voix `ff_siwis`** : présente dans le cache local du modèle. La fiche du modèle cite le jeu de données SIWIS parmi ses données d'entraînement, sous licence CC BY 4.0, qui demande une attribution. **Non établi** : si l'usage de cette voix dans un film diffusé impose de créditer SIWIS, et sous quelle forme. La liste des voix du modèle (`VOICES.md`) n'a pas été consultée.
- **eSpeak NG**, utilisé pour la phonétisation, est sous GPLv3 d'après la même fiche. **Non établi** : toute conséquence sur le son produit.
- **HyperFrames 0.8.33** : Apache-2.0, lu dans le `package.json` du paquet installé.
- **FFmpeg, libx264, Playwright, police Arial affichée dans les pages** : licences et conséquences sur un film diffusé non vérifiées.

Avant toute diffusion, une revue des crédits et des licences reste à faire par une personne compétente. Un crédit prudent serait de mentionner la voix de synthèse Kokoro et le jeu de données SIWIS ; c'est une proposition, pas une obligation démontrée.

## Ce qui reste de la première expérience

- **Compréhension sans l'image** : écoute faite par l'approbateur, qui avait déjà vu le film (`ff04-room-booking-film/AUDIO-ONLY-REVIEW.md`). Non faite avec une personne qui découvre le film.
- **Voix comparée aux sous-titres** : non faite. Aucun outil de transcription en français n'est installé ; seule l'écoute de l'approbateur en répond.
- **Sous-titres externes dans le lecteur prévu** : non fait. Aucun lecteur de destination n'est défini.

## Sources

- [Fiche du modèle Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) et [son README](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/README.md), consultés par recherche le 23 novembre 2026.
- [SIWIS French Speech Synthesis Database, copie sur Hugging Face](https://huggingface.co/datasets/Aviv-anthonnyolime/SIWIS_French_Speech_Synthesis_Database) et [rapport Idiap d'origine](https://publications.idiap.ch/publications/show/3580).

Les pages elles-mêmes n'ont pas été lues en entier : les éléments ci-dessus viennent des résumés de recherche, à confirmer avant de s'en prévaloir.
