# FF-10 — Recette du MP4 V5 validé

23 novembre 2026. Protocole préalablement figé : V5-RECIPE-PROTOCOL.md, commit 60c33cc.

## Version contrôlée

Fichier local guarded-web-demo.mp4, SHA-256 9fbb7c316fb20ef94a0424f231881b5f0f24d86daf32418aadc1a92e94ae11ad. Aucune modification du film.

## Résultats techniques

- Durée 16,166667 s ; H.264 et AAC présents ; 485 images ; cadence moyenne 30/1.
- PCM audio décodé SHA-256 f6819e9e643df7e29951eb2fba046111177c65b6334fa05c6defe2c04652ca86, conforme au témoin du pilote.
- Sous-titres SRT et transcription disponibles, avec trois fenêtres : 2,55–5,37 s ; 6,65–10,52 s ; 11,20–15,695 s. La concordance textuelle a été contrôlée dans AUDIOVISUAL-REVIEW.md.
- Échantillonnage d'images vidéo à 1,0 s, 4,0 s, 8,5 s et 13,5 s (RGB 320×180). Les différences de composantes octet par octet entre images successives sont respectivement 28,079 %, 29,490 % et 11,168 %. Les empreintes exactes des échantillons figurent dans v5-recipe-evidence.json.

**Interprétation limitée :** les images changent entre les trois fenêtres. Une différence de pixels ne prouve pas que la première tâche est créée, que la seconde apparaît ou que la première est cochée et barrée. Elle peut provenir des sous-titres ou d'autres éléments. La présence et la compréhension des trois gestes restent non vérifiées par une inspection perceptive indépendante du MP4 exact.

## Validation humaine

L'utilisateur a déclaré explicitement : « Mon verdict éditorial sur la V5 FrameForge est : validé. Ce verdict n'autorise aucune publication. » Décision liée à l'empreinte exacte dans HUMAN-EDITORIAL-APPROVAL-V5.md.

**PASS pour l'appréciation éditoriale globale humaine.** L'utilisateur n'a pas fourni de compte rendu séparé des trois gestes ni d'une écoute sans image ; ne pas attribuer ces observations spécifiques.

## Verdicts et décision

- Identité du MP4, paramètres techniques, PCM : PASS.
- Évolution visuelle mesurée aux quatre instants : PASS.
- Trois gestes identifiables à l'écran : UNVERIFIED par cette méthode.
- Compréhension de la narration sans image : UNVERIFIED en tant que test distinct.
- Appréciation éditoriale humaine globale : PASS.
- Promotion du chemin FF-10 en production : NO-GO tant que le point d'entrée n'est pas rendu obligatoire ou son périmètre officiellement limité et que les garanties manquantes ne sont pas arbitrées.

Aucun média publié ni transmis. FF-10 reste ouvert.
