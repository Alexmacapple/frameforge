# Passation : essai motion design « Le focus clavier »

Date : 2026-11-25

## État

PROMPT.md est exécuté. Les livrables sont terminés et validés visuellement par l'utilisateur (« ça m'a l'air bien »).

| Fichier | Rôle |
|---|---|
| `index.html` | Composition HyperFrames 0.8.33 (1920 × 1080, 30 i/s, 16 s). L'état de chaque élément est une fonction pure du temps. La timeline est exposée dans `window.__timelines["focus-modale"]`. |
| `media/essai.mp4` | Rendu final : h264, 480 images, sans piste audio (consigne « Pas de son »). |
| `RAPPORT.md` | Concept, horaires, rendus et retouches, vérifications, limites. |
| `~/Downloads/essai.mp4` | Copie demandée par l'utilisateur. |

## Attention : emplacement temporaire

Ce dossier se trouve sous `/private/tmp/claude-502/…`. Un redémarrage ou un nettoyage système peut l'effacer. Pour conserver le projet, copiez-le dans un emplacement durable, par exemple `~/Claude/`. Seule la vidéo existe déjà ailleurs, dans Téléchargements.

## Refaire le rendu

```bash
cd <ce dossier>
HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 \
  npx --yes hyperframes@0.8.33 render . --output=media/essai.mp4 --workers=2 --no-best-effort
```

Pour prouver qu'aucun réseau n'est utilisé, lancez la même commande préfixée par :

```bash
sandbox-exec -p '(version 1)(allow default)(deny network-outbound)(allow network-outbound (remote ip "localhost:*"))(allow network-outbound (remote unix-socket))'
```

## Piège connu : les polices

HyperFrames 0.8.33 remplace « Avenir Next », « Helvetica Neue » et Arial par Inter (table `FONT_ALIAS_MAP`), qu'il télécharge depuis Google Fonts. La composition l'évite avec une famille propre, `FocusSans`, déclarée par `@font-face` en `local("AvenirNext-…")`. Ne remettez pas de nom de police système directement dans `font-family`.

Le premier rendu, fait avant cette correction, a laissé un cache dans `~/.cache/hyperframes/fonts/inter`. Il n'est plus utilisé et peut être supprimé.

## Pistes non traitées, si l'on y revient

- Visionner la vidéo en temps réel pour juger les courbes de mouvement : elles n'ont été examinées que sur des images fixes.
- Faire tester la compréhension par une personne qui ne connaît pas le sujet.
- Montrer éventuellement Maj+Tab, qui boucle en sens inverse dans le code : ce n'est pas illustré dans la vidéo.
- Le lint signale un avertissement « fichier trop long » (plus de 400 lignes). Il est conservé volontairement, car il s'agit d'un plan unique.
