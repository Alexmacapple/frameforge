# Second film produit depuis une fiche — réservation d'une salle

23 novembre 2026, MacBook Pro. Décidé par Alex : fabriquer un second film sur une autre page, en partant d'une fiche neuve, pour voir ce qui casse dans la chaîne construite sur le film du formulaire. Playwright 1.64.1, HyperFrames 0.8.33, FFmpeg 9.0.1, Kokoro 0.9.4.

## Verdict

**PASS technique** : le film existe, rendu par le garde, avec une fiche sans échec. **Approbation éditoriale** consignée après coup dans EDITORIAL-APPROVAL.md. **NO-GO** : toute diffusion.

## Film produit

- `media/room-booking.mp4`, local, non versionné. SHA-256 `9c834228ae4db81dda154f5bf62e3bfc8fd3ac4012f9f64bbfddfcc29dfbf543`.
- 15,000 s, 450 images à cadence constante, H.264 1920×1080, AAC 48 kHz stéréo, niveau intégré −19,6 LUFS. Décodage intégral : PASS.
- Page filmée : `booking.html`, fixture locale à données fictives. Trois gestes : choisir la salle Érable, cocher le vidéoprojecteur, réserver.
- Statut : DRAFT au moment du rendu, REVIEWED après approbation.

## Ordre de fabrication

1. Fiche écrite d'abord, avec les trois phrases et sans repère.
2. Narration synthétisée depuis la fiche (`synthesize_kokoro.py`), durées mesurées.
3. Repères posés dans la fiche d'après ces durées ; composition, sous-titres et transcription générés par `build_from_fiche.py`.
4. Capture (`capture.cjs`) : chaque geste est déclenché 0,5 s après le début de sa phrase, lu dans la fiche.
5. Rendu gardé, empreinte du film reportée dans la fiche, second rendu identique.

## Preuves exécutées

- **Fiche** : 13 PASS, 4 contrôles ouverts UNVERIFIED, code de sortie 2.
- **Gestes** : résultats visibles 0,33 à 0,34 s après le début de chaque phrase (clics à 2,21 s, 6,09 s et 9,70 s ; parole à 1,876 s, 5,772 s et 9,376 s). États du DOM relus : salle Érable, option cochée, « Salle Érable réservée avec vidéoprojecteur. ».
- **Son** : corrélation de chaque clip avec le film à son repère, 0,99977, 0,99936 et 0,99981.
- **Reproductibilité du rendu** : brouillon témoin et deux rendus gardés, même empreinte.
- **Tests** : 9 sur 9 dans `test_room_booking.py`, dont le rejet d'un clip altéré, le rejet du film de l'autre pilote, le pointeur présent aux trois gestes et la confirmation affichée dans son sous-titre. Les 46 tests du pilote du formulaire passent toujours.
- **Planche** de la capture lue par l'agent : pointeur visible, libellés et coche non masqués après correction (voir plus bas).

## Ce qui a cassé ou manqué

- **La fiche ne savait pas décrire un film pas encore rendu.** Elle exigeait une empreinte de film et un document d'approbation. Corrigé dans `check_manifest.py` : un brouillon peut avoir les deux à `null`, le contrôle répond alors UNVERIFIED ; un film REVIEWED sans empreinte reste un échec.
- **La fiche est une entrée figée du rendu qui produit le film dont elle porte l'empreinte.** Il faut deux passes : rendre, reporter l'empreinte, figer de nouveau, rendre encore. Le second rendu redonne le même film, mais la manœuvre est manuelle.
- **Le garde ne se réutilise pas, il se copie.** `render_guarded.py` fait 207 lignes dont 57 diffèrent de celui du formulaire, pour des noms de fichiers, des empreintes et deux seuils de durée qui étaient en dur (480 images, 15,9 s) et sont maintenant lus dans la référence de sortie.
- **Le script de capture se réécrit presque entièrement** : 112 lignes sur 124 diffèrent. Seuls le pointeur, le déplacement et la conversion sont communs.
- **Le générateur a servi tel quel**, à une option près : il ne visait que la fiche de son propre dossier.
- **Le pointeur masquait le résultat du deuxième geste.** Posé sur la case à cocher, il cachait la coche pendant toute la phrase qui l'annonce. Corrigé en visant la fin du libellé. Aucun contrôle automatique ne l'a vu : c'est la planche qui l'a montré.
- **La synthèse n'est pas reproductible à l'octet, même avec graine.** Sur trois phrases, deux ressortent identiques d'un passage à l'autre ; la première varie entre au moins trois versions. Graine avant le chargement du modèle, synthèse d'échauffement et fil d'exécution unique essayés sans effet, puis abandonnés. Les clips utilisés sont figés par empreinte ; `narration-synthesis.json` consigne ceux de ce film.
- **Un outil de session a été nécessaire** pour recalculer les trois empreintes du garde après chaque changement. Il n'est pas versionné.

## Limites

- Nouvelle interprétation vocale, jamais écoutée par un humain. Vitesse Kokoro 1,2, sans accélération ajoutée.
- L'environnement Kokoro est hors dépôt (`/tmp/frameforge-kokoro-pilot-20261123/.venv`) ; il disparaîtra au prochain nettoyage de `/tmp`.
- `capture.cjs` appelle Playwright par un chemin absolu propre à ce Mac.
- Le tiers inférieur de l'image est vide hors sous-titres.
- Compréhension sans l'image et conformité de la voix au texte : non vérifiées.

## Ce que l'essai suggère, sans le décider

Deux films suffisent à voir ce qui est commun : le pointeur, la conversion de la capture, le garde hors de ses constantes, le calcul des empreintes. Les factoriser est une décision d'architecture distincte, non prise ici.
