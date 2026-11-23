# FF-10 — Protocole : voix Kokoro en entrée directe du rendu gardé

23 novembre 2026. Fait suite à KOKORO-GUARD-RESULT.md (commit 2c9223c), dont la limite était : rendu gardé avec la voix Thomas, puis remplacement de la piste audio après coup.

## Objectif

Le rendu gardé du formulaire lit directement les clips Kokoro. Plus de rendu intermédiaire Thomas, plus de remplacement de piste. Répertoire : `form-pilot-kokoro/`, wrapper `guarded_hyperframes_v2.py` réutilisé sans modification.

## Constats préalables, mesurés avant d'écrire le garde

- **Synthèse non reproductible à l'octet.** Kokoro 0.9.4 (torch 2.15.0, voix `ff_siwis`, pipeline `f`) relancé deux fois sur les trois phrases donne des empreintes différentes à chaque passage, et différentes des clips conservés. Avec `torch.manual_seed(0)`, deux passages donnent des empreintes identiques. Les clips approuvés ont été produits sans graine connue : ils ne peuvent pas être régénérés, seulement figés.
- **Vitesse des clips approuvés : 1,2 (inférence).** Les durées obtenues à vitesse 1,2 (2,925 s, 3,175 s, 4,500 s) sont exactement celles de `kokoro-fast1..3.wav` ; à 1,0 et 1,15 elles diffèrent.
- **Recette de la piste approuvée, non consignée jusqu'ici.** `kokoro-new-audio.m4a` est le mixage de `kokoro-fast1.wav` accéléré par `atempo=1.06` à 1,5 s, de `kokoro-fast2.wav` accéléré par `atempo=1.08` à 5,2 s et de `kokoro-fast3.wav` inchangé à 10,0 s. Corrélation mesurée avec la piste approuvée : 0,99993, 0,99994 et 0,99993. Témoin négatif : sans accélération, 0,311 et 0,244 pour les clips 1 et 2. Les deux premières phrases sont donc accélérées de 6 % et 8 % en plus de la vitesse 1,2 ; cette accélération fait partie de la version écoutée et approuvée.

## Entrées

- Clips sources figés par empreinte : `form-pilot/media/kokoro-fast1..3.wav` et `form-pilot/capture.mp4`.
- `prepare_inputs.py` dérive `kokoro1.wav` (atempo 1,06), `kokoro2.wav` (atempo 1,08), `kokoro3.wav` (copie) et copie `capture.mp4`. Il refuse une source modifiée et un clip dérivé dont l'empreinte diffère du manifeste.
- `index.html` : seules les trois balises `audio` changent par rapport à `form-pilot/index.html` (source et durée du créneau). Images, sous-titres et repères inchangés.

## Contrat de sortie

Durée 16 s, H.264 1920×1080, 30 images par seconde en moyenne, 480 images au moins, une piste AAC, plus deux exigences propres à ce pilote :

1. le flux vidéo a l'empreinte du flux approuvé, `86a966e4f9bc6c7d000a179061eb0ba5e6422c10fb84329be6c273decba4eb52` ;
2. le son décodé a l'empreinte du brouillon témoin, rendu directement par HyperFrames depuis les mêmes entrées.

Le brouillon témoin n'est retenu comme référence que si son flux vidéo est celui approuvé et si son son correspond aux trois clips d'entrée à leurs repères (corrélation supérieure à 0,999 par clip).

## Tests attendus

- Entrées autorisées acceptées ; HTML modifié rejeté ; clip Kokoro altéré rejeté.
- Film gardé avec la voix Thomas (`form-pilot/media/form-guarded.mp4`, mêmes images) **rejeté** : c'est le test qui échouerait si le contrat audio n'était pas passé à Kokoro.
- Film portant le son Kokoro mais des images réencodées **rejeté**.
- Film court sans voix rejeté ; brouillon témoin accepté.
- Préparation : source altérée rejetée sans rien déposer ; cas nominal reproduisant les empreintes du manifeste.
- Rendu réel par `python3 render_guarded.py`, puis second rendu comparé au premier.

## Ce que ce protocole ne couvre pas

- Le film produit n'a pas l'empreinte `f4552189…` approuvée à l'écoute : sa piste est encodée par HyperFrames en AAC 48 kHz stéréo, celle approuvée était en 24 kHz mono. L'équivalence est une mesure, pas une écoute. **Une nouvelle écoute humaine de la version exacte reste nécessaire.**
- Aucune synthèse n'est lancée pendant le rendu et aucun nouveau texte n'est accepté. Une synthèse à graine fixe serait reproductible, mais produirait une autre interprétation vocale, à faire approuver.
- Les empreintes de clips dérivés dépendent de la version de FFmpeg (9.0.1 ici) : une autre version fait échouer la préparation, sans dépôt.
- Aucune diffusion. FF-10 reste ouvert.
