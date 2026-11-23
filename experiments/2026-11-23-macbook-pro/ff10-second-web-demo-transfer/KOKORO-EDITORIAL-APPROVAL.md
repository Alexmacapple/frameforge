# Deuxième démonstration web — Validation éditoriale Kokoro

Date : 23 novembre 2026.

Après écoute de form-kokoro-review.mp4 dans QuickTime, l'utilisateur a répondu « parfait la suite ». Ce retour est consigné comme **approbation éditoriale de la voix et de la version présentée**, dans la continuité du retour précédent « nickel juste la voix que j'aime pas bien ». Il ne constitue **aucune autorisation de diffusion**.

Version exacte : SHA-256 f4552189c24758879f60a87c0a0a369dbd49a8e3a333c683eac0b42057ecefad, 16,000 s, 480 images, 30 fps moyens, H.264 et AAC. La voix est Kokoro ff_siwis, français, synthèse locale. Le MP4 est conservé sur le MacBook Pro, non versionné.

La comparaison de flux vidéo par SHA-256 confirme l'identité bit à bit du flux H.264 avec la version gardée précédente ; seul le flux audio a changé. Voir KOKORO-REVIEW-EVIDENCE.json. Décodage FFmpeg intégral : PASS.

**Frontière des preuves :** la nouvelle version a été produite par remplacement contrôlé de la piste audio *après* le rendu gardé précédent. Le validateur de sortie du scénario FF-10, qui attend l'empreinte PCM de la voix Thomas, **ne reconnaît pas encore** cette nouvelle piste Kokoro. Ne pas qualifier la nouvelle version de rendu intégralement gardé, ni la promouvoir en production sans adapter et tester le contrat audio et la finalisation.

Aucune publication autorisée. FF-10 reste ouvert.
