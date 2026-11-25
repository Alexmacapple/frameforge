# REPRISE — FrameForge

Dernière mise à jour : 25 novembre 2026, fin de session, MacBook Pro. `main` à `7216e90`, synchronisée avec GitHub, arbre propre. Vérifier HEAD au démarrage.

## Prochaine action
Faire les deux écoutes humaines du film de réservation : [#35](https://github.com/Alexmacapple/frameforge/issues/35) (une personne qui n'a jamais vu le film) et [#36](https://github.com/Alexmacapple/frameforge/issues/36) (voix comparée aux sous-titres), avec `experiments/2026-11-23-macbook-pro/ff04-room-booking-film/LISTENING-SHEET.md` et `media/room-booking-son-seul.m4a`. Même feuille prête pour les fenêtres modales (`ff59-film-fenetres-modales-recap/LISTENING-SHEET.md`) ; sa partie B y est déclarée conforme par Alex le 25 novembre, sa partie A reste à faire. [#61](https://github.com/Alexmacapple/frameforge/issues/61) (prononciation par transcription française) attend ces écoutes.

## Fait le 25 novembre 2026
- #47 : film des fenêtres modales produit et approuvé (PR #57, `d10c50b8…0845`). Le ticket reste ouvert : à fermer après relecture de ses critères.
- #56 fermé (verdict COMPOSE) ; ses manques 1, 2, 4 (PR #58), 5 et 6 (PR #62 : fiche v3 à sous-titres découpés, `contact_sheet.py`) traités.
- #59 : insert animé jugé utile (PR #63), intégré en fin de film par la fiche v4 (PR #64) ; film `ff59-film-fenetres-modales-recap` approuvé (`3720625a…1af6`), à côté du film 47 inchangé.
- #65 : le rendu gardé et le brouillon témoin tournent sous `sandbox-exec`, sans réseau sortant (PR #66). La police Inter que HyperFrames demandait à Google n'entrait pas dans l'image.
- Essai du prompt de motion design rangé dans `ff59-essai-motion-design/` ; note de source `research/comparaison-claude-remotion-hyperframes.md`.
- Télémétrie HyperFrames coupée sur le MacBook Pro.

## Points à surveiller
- Mac Studio : HyperFrames jamais lancé. Au premier usage, couper sa télémétrie, et vérifier que `npx` a HyperFrames 0.8.33 en local (`~/.npm/_npx`) : le rendu n'a plus de réseau pour le télécharger.
- `sandbox-exec` est marqué obsolète par Apple : vérifier qu'il fonctionne après chaque mise à jour de macOS (`test_rendu_hors_ligne.py`).
- Disque du MacBook Pro plein à 99 % le 25 novembre, ramené à 89 % : un rendu de 66 s demande environ 16 Go temporaires.
- Contrôle par mutation : dernier passage complet sur la PR #64 (104/106, deux trous comblés par des tests vérifiés un à un) ; à relancer après la prochaine série de changements du garde.
- #40/#41, #44, #46, thèmes #5–#12/#15 : consulter leur état courant.

## Règles
GitHub (issues et preuves) reste la source de vérité du suivi. En cas de divergence, vérifier les décisions humaines et les preuves les plus récentes ; ne pas arbitrer silencieusement. Aucun contournement du garde, transfert de média ou diffusion sans autorisation explicite. Respecter PUBLICATION-POLICY.md et la règle de PR pour film-chain et garde.

## Mise à jour de la passation
En fin de session, actualiser ce fichier avec date, SHA de travail, preuves, tickets, blocages et prochaine action concrète. Ne publier la mise à jour distante qu'avec autorisation. Ne pas dupliquer les rapports ou l'historique de PLAN.md.
