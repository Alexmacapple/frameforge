# Révision et reprise — corriger une scène sans défaire le reste

23 novembre 2026, MacBook Pro. Troisième expérience de la feuille de route adoptée (issue 13, expérience 3 ; issue 10). Playwright 1.64.1, HyperFrames 0.8.33, FFmpeg 9.0.1, Kokoro 0.9.4. Tout se passe sur une copie du film de réservation ; le film approuvé `9c834228…f543` et son dossier ne sont pas touchés.

## Hypothèse à réfuter

« Une retouche et une interruption ne détruisent pas les décisions existantes. » Échec si l'ancien accord est présenté comme couvrant la nouvelle version.

## Protocole

1. Point de départ : la copie de travail, rendue par le garde, redonne le film approuvé à l'octet.
2. Choix humain verrouillé : les scènes 1 et 2 telles qu'approuvées, avec leurs clips de voix et la capture.
3. Correction du plan B : la phrase de la scène 3 seule. « Un message confirme la salle et l'option. » devient « Un message confirme la salle Érable et le vidéoprojecteur. » Seul ce clip est resynthétisé ; la capture est réutilisée.
4. Deux oublis volontaires, pour voir si l'ancienne approbation peut couvrir la nouvelle version.
5. Chemin honnête : la version corrigée redevient un brouillon, le rendu gardé est interrompu en cours de route, puis relancé.

## L'ancien accord ne couvre pas la nouvelle version

Approbation laissée en place dans la fiche (statut REVIEWED, empreinte du film approuvé) :

```text
rendu gardé, référence de sortie d'origine     BLOCKED film_output_video_changed, code 2, aucun film déposé
rendu gardé, référence de sortie mise à jour   BLOCKED film_output_differs_from_approved_film, code 2, aucun film déposé
repin.py --record-output sur le film corrigé   BLOCKED film refusé par le garde, code 2, la fiche garde 9c834228…
```

**Ce que le contrôle de fiche ne voit pas** : lancé seul avant le rendu, il répond `PASS approval`. Le document d'approbation nomme bien l'empreinte que la fiche porte encore ; il ne sait pas que les entrées ont changé depuis. La protection vient du garde, au moment du rendu, pas de la fiche.

## Interruption et reprise

Signal d'arrêt envoyé au rendu gardé pendant qu'il tourne, deux fois :

```text
code de sortie               2, {"status": "BLOCKED_OR_INTERRUPTED", "reason": "guarded render interrupted"}
film déposé                  non
dossier temporaire restant   aucun
empreintes du film           inchangées (repin.py --check : PASS)
```

Reprise par la même commande, sans autre geste : PASS, film identique à l'octet au brouillon témoin de la version corrigée.

**Perte constatée : des processus du moteur de rendu restent en vie.** Après chaque interruption, six processus `chrome-headless-shell` lancés par HyperFrames survivent, rattachés au processus 1. Ils étaient encore là une minute et demie après le retour du garde lors de la seconde interruption, et ont été arrêtés à la main. Après la première, ils avaient disparu deux à trois minutes plus tard, sans que la cause soit établie. L'enveloppe de rendu arrête le groupe de processus de `npx`, pas ces processus Chrome. Aucun fichier n'est affecté ; c'est une fuite de processus.

## Ce que la correction a changé, et ce qu'elle a laissé intact

Film avant correction `9c834228…f543`, film corrigé `070167a84b7d282202cd4fe3ccec94d0537a72850f29bef337d48fbbec9a347e`.

- **Entrées inchangées**, identiques à l'octet : capture, journal de capture, clips des phrases 1 et 2.
- **Entrées changées** : clip de la phrase 3, composition, sous-titres, transcription, fiche.
- **Fiche** : scènes 1 et 2 identiques ; scène 3 modifiée dans sa narration (texte, durée 4,025 s devenue 5,225 s) et la fin de son sous-titre. Repères des gestes inchangés.
- **Son de 0 à 8,9 s** : identique échantillon pour échantillon (0 différence sur 427 200).
- **Images de 0 à 7,9 s** : identiques (237 images).
- **Images de 7,9 à 8,9 s** : 30 images diffèrent, alors que la capture et la composition sont les mêmes à ces instants. Écart mesuré très faible, rapport signal sur bruit moyen de 71 dB. Explication proposée, non démontrée : l'encodeur vidéo anticipe sur les images suivantes, et celles-ci changent à 9,0 s avec le nouveau sous-titre. Aucun contenu ne diffère à l'œil sur l'image comparée à 8,5 s.
- **Images à partir de 8,9 s** : toutes différentes, comme attendu, le sous-titre de la scène 3 ayant changé.
- **Statut** : REVIEWED devenu DRAFT. La version corrigée n'a ni empreinte approuvée ni document d'approbation tant qu'un humain ne l'a pas écoutée.

## Verdict

- **L'ancienne approbation ne peut pas couvrir la version corrigée : PASS.** Trois tentatives, trois refus.
- **Interruption sans dégât sur les fichiers, reprise par la même commande : PASS.**
- **Correction localisée : PASS avec une réserve expliquée.** Rien ne change avant 7,9 s ; une seconde d'images diffère à peine avant la scène corrigée.
- **Nettoyage après interruption : FAIL.** Des processus Chrome restent en vie.
- **UNVERIFIED** : écoute et visionnage humains de la version corrigée.

## Limites

- La « reprise » est une relance complète du rendu : rien n'est repris à mi-chemin, et rien n'est mis en cache. C'est ce que le projet avait déjà constaté.
- Le verrouillage d'un choix humain n'est pas un mécanisme distinct : il tient au fait que les entrées des scènes approuvées sont figées par empreinte et réutilisées telles quelles.
- La correction choisie ne décale aucun geste. Une correction qui déplacerait une scène demanderait une nouvelle capture ; ce cas n'est pas essayé ici.
- L'explication de l'écart d'images entre 7,9 et 8,9 s est une hypothèse.
- Aucun test automatisé propre à ce dossier.

## Suite possible, non engagée

La feuille de route dit de ne construire une protection que si l'essai montre une perte précise. Deux pertes précises ressortent : les processus Chrome orphelins après interruption, et un contrôle de fiche qui répond PASS sur une approbation devenue périmée. Les corriger toucherait l'enveloppe de rendu et le contrôle de fiche ; c'est à décider.
