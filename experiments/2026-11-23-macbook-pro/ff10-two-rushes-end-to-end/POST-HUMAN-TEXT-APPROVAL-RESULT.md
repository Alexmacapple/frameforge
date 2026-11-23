# FF-10 — Rendu après approbation humaine d'un texte précis

23 novembre 2026. La décision explicite de l'utilisateur, limitée au libellé B, est consignée dans HUMAN-TEXT-APPROVAL.md.

## Expérience

Le libellé approuvé est « Rush B : barres de couleur, audio témoin. ». Une modification ciblée du fond du cartouche A (de #101010 à #222222) a été maintenue. Le contrôleur de pré-rendu a vérifié la conservation du bloc B et de la transition par comparaison exacte à la référence de test épinglée, puis HyperFrames 0.8.33 a rendu une copie isolée du projet de deux rushes.

- Nouveau MP4 local : local/two-rushes-after-human-text-approval.mp4
- SHA-256 : fbd342181790dfdbe1bb145785ad8598680d4f974344c86c79e0556459235dea
- Empreinte identique au rendu technique précédent : oui.
- Décodage FFmpeg complet : PASS, vérifié par le wrapper.
- Texte B préservé dans la composition source : PASS.
- Validation visuelle et sonore humaine du nouveau MP4 : UNVERIFIED.
- Autorisation de diffusion : NON ACCORDÉE.

## Limites

La correction humaine est réelle **uniquement sur la formulation textuelle** ; la composition et la fixture ne sont pas approuvées intégralement. Le test conserve le même changement autorisé déjà présent dans le rendu précédent : il démontre la répétabilité du rendu après approbation textuelle, et non une nouvelle demande de remontage éditorial indépendante. Les deux rushes restent des mires de test. Le contrôle n'est pas imposé aux autres chemins de rendu.

**Verdict : PASS technique à périmètre limité ; FF-10 reste ouvert.** Aucun média publié.
