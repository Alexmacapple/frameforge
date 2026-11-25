# Essai : le prompt de motion design appliqué au focus clavier

25 novembre 2026, MacBook Pro. Prompt de la vidéo comparée dans `research/comparaison-claude-remotion-hyperframes.md`, adapté au focus clavier dans une fenêtre modale (`PROMPT.md`), exécuté par Alex dans une session Claude séparée, hors du dépôt. Les fichiers de cette session sont repris tels quels : `index.html`, `PROMPT.md`, `RAPPORT.md`, `PASSATION.md`. Les références citées par le prompt (`references/`) sont la page, le texte et la planche du film 47, dans `../ff47-film-fenetres-modales/`.

Vidéo : `media/essai.mp4`, locale, non versionnée, 16 s, 1920 × 1080, 30 i/s, sans son, `e89aab8a97aa38f33ffb2cfd52744a903804fced7c368a7dfa79cde48179aa97`. Planche de 16 images : `media/essai-planche.png`.

## Verdict

- **Ambition tenue.** Un seul fil : l'anneau orange du focus engendre le bouton, la page, la fenêtre, puis la fenêtre se replie dans le bouton. Les mots « Entre », « Reste », « Revient », « Reprend », associés à leur touche, rendent la vidéo lisible sans son. Au second Tab, l'anneau sort par un bord de la fenêtre et rentre par l'autre : la boucle se voit.
- **Finition incomplète.** Sur la planche : deux libellés « Supprimer mon compte » superposés à 4,5 s, touches « Échap » et « Tab » qui se chevauchent à 13,5 s, petit rectangle gris isolé à 3,5 s.
- **Hors de la chaîne.** Un seul rendu final, police système Avenir Next, aucune voix : ni reproductibilité prouvée, ni compréhension sans l'image.
- Jugement d'Alex rapporté par la passation : « ça m'a l'air bien ».

## Comparaison avec l'insert du ticket 59

- Insert du ticket 59 : schéma sobre, calé sur une voix, rendu reproductible trois fois, intégré à un film gardé et approuvé.
- Cet essai : mouvement bien plus riche, fabriqué en 15 minutes avec 3 séries de retouches, sans voix ni garde.
- Les deux partent de la même méthode (composition écrite par Claude, timeline en fonction pure du temps, HyperFrames 0.8.33) ; la différence tient au prompt, pas à l'outil.

## Ce que l'essai apporte à la chaîne

1. **Police téléchargée** : HyperFrames remplace Arial par Inter, téléchargée depuis Google Fonts ; toute la chaîne est concernée (ticket 65).
2. **Preuve d'absence de réseau** : `sandbox-exec` sans réseau sortant pendant le rendu ; piste pour le garde (ticket 65).
3. **Mots-clés à l'écran** associés aux touches : piste pour de prochains inserts.
