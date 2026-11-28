# Veille : rea-video, analyse pour FrameForge

Date : 28 novembre 2026. Lecture seule : rien n'a été installé, exécuté ni copié.

## Verdict

Aucune intégration. rea-video analyse des vidéos faites par d'autres pour dire comment elles ont été fabriquées et comment les refaire ; FrameForge fabrique ses propres films et en connaît l'origine par construction. Les deux fonctions qui auraient pu servir (transcription de la voix, lecture des sous-titres) ne couvrent pas le français. Trois idées de forme sont à retenir, sans code.

## Révision figée

- Dépôt : `JuneYaooo/rea-video`, SHA `70a0d5ea314329a617d493ab5b4c9eddcdd1365c` (27 novembre 2026).
- Licence Apache-2.0, version 0.1.0, dépôt créé le 29 octobre 2026, 988 fichiers, Python 3.10 ou plus.
- Chiffres de l'API GitHub le 28 novembre : 14 107 étoiles, 2 051 forks, 14 tickets ouverts.
- FrameForge : `main` à `85486ef`.

## Ce que fait l'outil

Une commande `rea-video decompose` découpe une vidéo en plans, sépare voix, musique et bruitages, puis juge plan par plan si l'image est filmée, générée par IA, rendue en 3D, produite par du code ou capturée à l'écran. Elle produit un rapport pour un lecteur humain et un dossier `VIDEO.md` pour un agent, puis un plan pour refaire la vidéo avec d'autres éléments. Un modèle de vision distant (Gemini ou autre) est optionnel.

## Contraintes et hypothèses

- **Langues.** Reconnaissance vocale SenseVoice : chinois, anglais, japonais, coréen, cantonais, plus un modèle bengali (`rea_video/speech.py`). Lecture de texte à l'écran : chinois, anglais, japonais, coréen (`rea_video/overlay.py`). Pas de français. Hypothèse à vérifier, non testée : le modèle anglais lit mal les caractères accentués.
- **Réseau.** Les modèles sont téléchargés au premier usage depuis `github.com` et `modelscope.cn` (environ 67, 149 et 160 Mo selon les fonctions), avec une empreinte contrôlée pour ceux que j'ai lus. Le rendu de FrameForge tourne sans réseau.
- **Envoi de médias.** Avec Gemini, les extraits de la vidéo sont envoyés à Google. Notre règle interdit tout transfert de média sans autorisation.
- **Écritures hors projet.** Préférences dans `~/.rea-video`, modèles dans `~/.cache/rea-video/models`. L'installation en plugin ajoute un skill, rédigé en chinois, à l'agent.
- **Maturité.** `pyproject.toml` désigne un dossier `tests` qui n'existe pas dans l'arbre à ce SHA ; pas de CI. L'exactitude annoncée (98 à 100 %) vient d'un jeu d'évaluation de l'auteur (`eval/RESULTS.md`), non reproduit ici. Le dépôt change chaque jour.
- **Licence.** Apache-2.0 est compatible avec MIT moyennant attribution : contrairement à OpenMontage (AGPL-3.0), la licence n'est pas l'obstacle.

## Verdict par composant

- **Détection filmé, IA, 3D, code : REJECT.** FrameForge ne juge pas des vidéos tierces ; l'origine de chaque média est déjà dans `provenance-manifest.json`.
- **Plan pour refaire une vidéo, tables de modèles génératifs, capsule-cinema, ChatCut : REJECT.** Hors sujet, et génération par services distants payants.
- **Transcription de la voix : REJECT.** Pas de français ; inutile pour #36 et #61.
- **Lecture des sous-titres dans l'image : REJECT en l'état.** Pas de français.
- **Format VIDEO.md : REJECT.** Décrit une vidéo analysée ; la fiche de provenance couvre notre besoin, et un second format de description ferait doublon.
- **Séparation voix, musique, bruitages : REJECT.** Nos films n'ont qu'une voix de synthèse, connue à la source.

## Idées à retenir, sans code

1. **Distinguer ce qui est mesuré de ce qui est déduit, dans le fichier lui-même.** Dans `VIDEO.md`, une clé suivie de `~` est une déduction ; sans ce signe, elle est vue ou mesurée. Même règle que notre contrat de preuve, mais portée par le format.
2. **Dater par numéro d'image, pas par secondes arrondies.** Chaque instant y porte le numéro d'image de la source. À regarder si un écart d'arrondi réapparaît dans nos sous-titres ou nos gestes ; non vérifié : la forme actuelle de nos horodatages.
3. **Hiérarchie des sources de vérité pour une évaluation.** Trace de production d'abord, étiquette de plateforme ensuite, jugement à l'œil en dernier et marqué comme douteux (`docs/dev/evaluation.md`).

Une quatrième idée dépend d'un outil que nous n'avons pas : mesurer dans le film rendu l'apparition et la disparition de chaque sous-titre, et comparer à la fiche. `hyperframes check` contrôle la composition, pas le fichier rendu. Elle demande une lecture de texte fiable en français.

## Fait annexe

Pour refaire un plan produit par du code, rea-video recommande HyperFrames ou Remotion (`skills/rea-video/references/code-render.md`). Cela ne change rien pour nous.

## Limites de cette analyse

Lus : `README.md`, `pyproject.toml`, `docs/en/videomd.md`, `docs/dev/evaluation.md`, `skills/rea-video/references/setup.md` et `code-render.md`, l'en-tête de `speech.py` et de `overlay.py`, la liste des commandes. Non lus : le reste du code (environ 2,5 Mo de Python). Rien n'a été exécuté : aucune affirmation de l'auteur sur l'exactitude n'est vérifiée.
