# FF-10 — Transfert du garde V2 au formulaire : résultat

23 novembre 2026. Protocole figé : FORM-GUARD-PROTOCOL.md, commit 5d2f2b7.

## Implémentation

Réutilisation de ff10-hyperframes-guarded-integration/guarded_hyperframes_v2.py sans modification. Le point d'entrée form-pilot/render_guarded.py fixe un contrat spécifique : référence HTML technique de fixture, empreintes de dix ressources déclarées, empreinte du manifeste et empreinte de référence de sortie. Le précontrôle est rejoué sur la copie isolée avant rendu. Le validateur vérifie durée 16 s, vidéo H.264 1920×1080, cadence moyenne 30 fps, 480 images minimum, piste AAC de durée suffisante et empreinte PCM du brouillon témoin. Le MP4 est décodé intégralement avant dépôt.

## Preuves exécutées sur MacBook Pro

- 5/5 tests unitaires PASS : entrée autorisée, modification HTML rejetée, sous-titres altérés rejetés, MP4 synthétique de 0,5 s sans voix rejeté, brouillon témoin accepté.
- Rendu réel par python3 render_guarded.py : PASS, environ 28 s.
- MP4 gardé local : SHA-256 548b31087df3165d856cbff0216389116fb0301f59a21547af66663ee3e7b0e5, identique au brouillon HyperFrames direct précédent.
- Aucun MP4 ni média joint au commit, aucun média publié.

## Limites

Le script npm render-draft direct reste disponible dans le package expérimental : le garde n'est pas obligatoire. Les références techniques sont fixées dans le code et ne prouvent aucune approbation éditoriale indépendante. La narration macOS Thomas et la présence visuelle des gestes n'ont pas encore de recette humaine sur ce MP4 exact. La capture Playwright repose sur un chemin local absolu, donc la reproductibilité sur une autre machine est UNVERIFIED. La cadence moyenne n'atteste pas une cadence constante.

**Verdict : PASS pour le transfert technique du wrapper à un deuxième scénario web, UNVERIFIED pour la recette humaine et NO-GO pour une promotion générale.** FF-10 reste ouvert ; publication interdite.
