# Essai : Libra-TTS comme seconde voix

Date : 28 novembre 2026, Mac Studio (macOS 27.0). Essai isolé, hors de la chaîne : rien n'a été modifié dans `experiments/`.

## Résultat

Libra-TTS lit nos phrases en français, en local et réseau coupé, et deux synthèses de suite donnent les mêmes fichiers à l'octet près. Alex a jugé les voix « superbes » après écoute de la réservation en Kokoro puis en Libra-TTS. Aucune décision d'intégration n'est prise.

## Révisions figées

- Modèle : `Ekam/Libra-TTS` sur Hugging Face, révision `a29b9e64155bffd08966f180502ca412cb358c92`. Apache-2.0, 16 langues dont le français, 8 voix, 12 styles. Distillé de `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`.
  - `model.safetensors` : `f57fbe7cf62a429e470a7b90b4ad5ca4405ae909d17db6f641c5b9cec1ed9ec2` (614 Mo)
  - `codec.safetensors` : `6e943a7e31d72f3d51e012562756af941a7a01b60eb42c9a32f4fc166d62c00c` (373 Mo)
- Code : `ekambrar100/Libra-TTS`, commit `2642632179db91866041ba1a90d0988705217a09`, version 0.1.1, Apache-2.0.
- Environnement : Python 3.12, 25 paquets, dont `mlx` 0.32.5, `numpy` 2.5.5, `tokenizers` 0.23.3, `huggingface-hub` 2.5.0, `soundfile` 0.14.0. Versions non figées par empreinte dans cet essai.

## Ce qui a été fait

1. Lecture du code avant installation (1 906 lignes) : aucune commande système, un seul accès réseau, le téléchargement du modèle par `huggingface_hub`.
2. Installation dans un environnement jetable, depuis l'archive du commit figé.
3. Téléchargement du modèle à la révision figée, dans un dossier local.
4. Synthèse de huit phrases (les trois de la réservation, cinq des fenêtres modales), voix `nina`, langue `fr`, graine 0, moteur MLX, sous `sandbox-exec` avec réseau interdit et `HF_HUB_OFFLINE=1`.
5. Seconde synthèse identique, fichiers comparés par `cmp`.

## Mesures

- Sortie : WAV mono, 24 kHz, 16 bits.
- Durée de synthèse : 0,9 à 3,0 s par phrase (2,96 à 10,96 s de son) ; 11,8 s pour la première, chargement compris.
- Reproductibilité : huit fichiers sur huit identiques entre les deux passages. Pour mémoire, Kokoro ne redonnait que deux clips sur trois le 24 novembre.

## Limites

- Reproductibilité vérifiée sur un seul Mac, dans une seule session : ni après redémarrage, ni sur le MacBook Pro (macOS 26.5.2), ni avec une autre version de `mlx`.
- Jugement d'écoute global, par l'approbateur, sans feuille phrase par phrase ; la prononciation de « Tab », « Échap » et « Érable » n'a pas été relevée mot par mot.
- Une seule voix essayée (`nina`), sans style.
- Projet publié le 19 novembre 2026, un seul auteur, aucune version publiée : le code s'installe depuis une archive de commit. Les taux d'erreur annoncés par l'auteur (2,74 % en français) ne sont pas vérifiés.
- Les clips et l'environnement de l'essai sont dans le dossier temporaire de la session et ne sont pas conservés.

## Ce qu'une intégration demanderait

- Un fichier d'exigences figé par empreintes, comme `voice-requirements.txt`, et le modèle contrôlé par ses deux empreintes.
- Un script de synthèse par film, à côté de `synthesize_kokoro.py`, et la voix déclarée dans la fiche de provenance.
- La même vérification sur le MacBook Pro.
- Une écoute et une approbation pour chaque film produit avec cette voix. Les films approuvés restent en Kokoro : leurs clips sont figés.
