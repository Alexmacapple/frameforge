# FF-10 — Finalisation gardée de la voix Kokoro

23 novembre 2026. Protocole préalable : KOKORO-GUARD-PROTOCOL.md, commit 08f3fca.

## Résultats

- 4/4 tests du finaliseur PASS : audio non approuvé rejeté avant rendu, flux vidéo invalide rejeté sans dépôt, sortie déjà existante rejetée, reproduction exacte de la version approuvée depuis le témoin gardé.
- Rendu HyperFrames réel via wrapper FF-10 V2 : PASS.
- Finalisation audio dans un répertoire temporaire et validation avant dépôt final : PASS.
- MP4 final local : form-pilot/media/form-kokoro-guarded.mp4.
- SHA-256 final : f4552189c24758879f60a87c0a0a369dbd49a8e3a333c683eac0b42057ecefad, **identique au MP4 Kokoro approuvé éditorialement**.
- Audio source figé SHA-256 : 857e6be89c8747c264ae2d4fd65d6b1beddb9e89188d4ca31c52faf3b3c46ea0.
- Le garde refuse de finaliser si le flux vidéo diffère de la référence approuvée. Aucune vidéo ni piste audio publiée ou jointe au dépôt.

## Périmètre exact

Le workflow produit le rendu initial avec la narration Thomas gardée, puis remplace **dans un espace temporaire** l'audio par la piste Kokoro déjà approuvée. Il ne s'agit pas d'une synthèse Kokoro intégrée nativement au moteur de composition, ni d'une généralisation à de nouveaux textes. Cette solution conserve les images et l'empreinte finale approuvées sans réinventer le moteur.

Les références de la fixture restent modifiables par les personnes autorisées à modifier le code ; la chaîne n'est pas une barrière contre un mainteneur malveillant. Les médias restent locaux et la reproductibilité hors Mac n'est pas établie. Les tests de recette perceptive ne sont pas remplacés par les empreintes.

**Verdict : PASS pour la reproduction technique gardée de cette version exacte ; NO-GO pour la promotion générale et toute diffusion.** FF-10 reste ouvert.
