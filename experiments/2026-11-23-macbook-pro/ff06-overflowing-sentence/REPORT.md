# Cas temporel adversarial — une phrase qui déborde

23 novembre 2026, MacBook Pro. Deuxième expérience de la feuille de route adoptée (issue 13, expérience 2 ; issue 6). Playwright 1.64.1, HyperFrames 0.8.33, FFmpeg 9.0.1, Kokoro 0.9.4.

## Hypothèse à réfuter

« Les contraintes temporelles usuelles ne font pas disparaître geste, résultat ou parole. » Échec si un mot, un résultat ou une attente significative disparaît sans que ce soit signalé.

## Protocole

Témoin : le film de réservation approuvé `9c834228…f543`. Un seul changement : la deuxième phrase est allongée.

- Avant : « L'option vidéoprojecteur est cochée. », 2,25 s.
- Après : « L'option vidéoprojecteur est cochée, pour que la salle soit équipée dès le début de la réunion. », 5,15 s.

Dans le film témoin, la troisième phrase commence 3,6 s après le début de la deuxième : la phrase allongée déborde de 1,55 s. Les clips des phrases 1 et 3 sont ceux du témoin, inchangés. Aucun outil de `film-chain/` n'est modifié.

## Ce qui se passe sans le garde

Deux rendus directs par HyperFrames, sans passer par le garde, sur la capture du témoin :

- **Durée déclarée laissée à 2,25 s : la phrase est coupée.** Par tranches d'une demi-seconde, la phrase 2 est présente pendant 2 s, partiellement à la tranche suivante (corrélation 0,65), puis absente. Les mots après « est cochée » disparaissent. HyperFrames rend sans avertissement, code 0.
- **Durée réelle déclarée (5,15 s), repères des autres scènes inchangés : deux voix se superposent.** De 9,0 à 10,55 s, la fin de la phrase 2 et le début de la phrase 3 jouent ensemble (corrélations de 0,42 à 0,75 au lieu de 1,00). HyperFrames rend sans avertissement, code 0.

**L'hypothèse est donc réfutée pour un rendu sans garde** : une parole disparaît, ou deux se recouvrent, sans aucun signal.

## Ce que fait le contrôle de la fiche dans les mêmes cas

```text
durée déclarée 2,25 s   FAIL measured_audio — voice2.wav : durée réelle 5.150 s, créneau 2.25 s
durée réelle déclarée   FAIL timeline — reservation-confirmee : narration qui chevauche la précédente
```

Le garde refuse de rendre une fiche en échec : aucun des deux films fautifs ne peut sortir par lui.

## L'ajustement

Comme le demande la feuille de route, composition et pauses sont ajustées, sans adaptateur ni nouvel outil. Dans la fiche seulement :

- la phrase 2 garde son début (5,4 s) et prend sa durée réelle ; son sous-titre va jusqu'à 10,7 s ;
- la scène 3 est repoussée de 9,0 à 11,9 s, avec le même silence qu'au témoin entre deux phrases ;
- le film passe de 15 à 18 s.

Tout le reste en découle par les outils existants : `build_from_fiche.py` régénère composition et sous-titres, `capture.cjs` relit les repères dans la fiche et rejoue les trois gestes, `repin.py` fige, le garde rend.

## Film ajusté

- `media/overflowing-sentence.mp4`, local, non versionné, statut DRAFT. SHA-256 `84d866e70687252cb9ee180535d50203749d863aa504756a02d4e28688151fa8`.
- 18,000 s, 540 images. Brouillon témoin sans avertissement ; deux rendus gardés identiques à l'octet.
- Fiche : 13 PASS, 3 contrôles ouverts.

Mesures sur ce film :

- **Aucune phrase coupée ni recouverte** : corrélation minimale de 0,999 par tranche d'une demi-seconde, pour chacune des trois phrases sur toute sa longueur (5, 10 et 8 tranches).
- **Silences entre phrases** : 1,12 s et 1,35 s.
- **Chaque résultat pendant la phrase qui l'annonce** : 0,41 s, 0,33 s et 0,35 s après le début de la parole ; chacun dans son sous-titre.
- **Résultats du DOM relus** : salle Érable, option cochée, « Salle Érable réservée avec vidéoprojecteur. ».
- **Pointeur visible** aux trois résultats (26, 23 et 24 pixels sur l'image réduite).
- **Planche de huit images lue par l'agent** (`media/planche-phrase-longue.png`, non versionnée) : le sous-titre long tient sur une ligne et occupe environ 88 % de la largeur ; la coche et le message de confirmation ne sont pas masqués.

## Verdict

- **Sans garde : FAIL.** Une phrase trop longue est coupée ou recouverte en silence.
- **Avec le contrôle de fiche : PASS.** Les deux cas fautifs sont refusés avec un motif lisible, et l'ajustement des repères suffit à produire un film où rien ne manque.
- **UNVERIFIED** : visionnage humain du film ajusté.

## Limites

- Un seul contre-exemple, comme prévu par le budget de l'expérience. Le cas « geste plus lent que la narration » n'est pas essayé.
- L'ajustement est fait à la main dans la fiche : rien ne propose les nouveaux repères. Le contrôle dit qu'il y a un problème, pas comment le résoudre.
- La durée du film change, donc le film ajusté n'est plus comparable image par image au témoin ; la comparaison porte sur les phrases et les résultats.
- Pendant la phrase allongée, l'écran reste fixe environ quatre secondes. Le contrôle ne juge pas si c'est acceptable.
- Un sous-titre encore plus long déborderait sur deux lignes ; ce cas n'est pas essayé.
- Aucun test automatisé propre à ce dossier : les mesures ci-dessus sont des commandes lancées une fois.
- Le garde n'est pas obligatoire : rendre directement par HyperFrames reste possible, et c'est là que la parole se perd.
