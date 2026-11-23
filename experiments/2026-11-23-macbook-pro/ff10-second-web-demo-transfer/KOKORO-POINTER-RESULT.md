# Formulaire, voix Kokoro — pointeur visible et envoi annoncé à temps

23 novembre 2026, MacBook Pro. Fait suite à KOKORO-NATIVE-GESTURE-REVIEW.md, dont l'approbateur a retenu deux défauts à corriger : clic d'envoi invisible, confirmation affichée 1,94 s avant son annonce. Playwright 1.64.1, HyperFrames 0.8.33, FFmpeg 9.0.1.

## Verdict

**PASS technique** : le rendu gardé de `form-pilot-kokoro/` produit un film où le pointeur est visible aux trois gestes et où la confirmation apparaît pendant la phrase « Le formulaire est envoyé. ».

**En attente** : visionnage et approbation humaine de ce film exact. **NO-GO** : toute diffusion. FF-08 et FF-10 restent ouverts.

## Film produit

- `form-pilot-kokoro/media/form-kokoro-pointeur.mp4`, local, non versionné.
- SHA-256 `ab040730a5bdc4bb36e77be4a7b22da067dd3da2bfaddd436c5a636f7b567125`.
- 16,000 s, 480 images, H.264 1920×1080, AAC 48 kHz stéréo. Décodage intégral : PASS.
- **Son décodé identique à l'octet** à celui du film approuvé `0d9d0c9c…92a5` (même empreinte PCM `644eee55…b8f6`). La voix approuvée n'a pas changé ; seules les images changent.
- Le film `0d9d0c9c…92a5` est remplacé (statut SUPERSEDED) ; son garde reste lisible au commit b5209eb.

## Ce qui a changé

- **Capture refaite** par `capture.cjs`. Les gestes sont de vrais événements Playwright : clic dans chaque champ, frappe caractère par caractère, clic sur le bouton. Les trois états du DOM sont relus après coup : nom, adresse, message « Demande enregistrée pour Camille Martin. ».
- **Pointeur** : disque orange dessiné par un script injecté dans la page, qui suit les événements souris réels et s'entoure d'un halo au clic. C'est un ajout de lisibilité, pas une image du curseur du système. La fixture `form.html` n'est pas modifiée.
- **Gestes calés sur la narration**, et non l'inverse : la narration et les sous-titres gardent leurs repères, le clic d'envoi est retardé de 8,43 s à 10,57 s. La piste son reste ainsi celle qui a été approuvée.
- **Frappe progressive** : écart par rapport à la demande, qui ne portait que sur le pointeur et le délai. Un pointeur qui clique puis un texte qui apparaît d'un bloc aurait été incohérent.
- **Images clés** : une par seconde dans `capture.mp4`. Le premier rendu signalait des images clés espacées de 8,33 s, avec risque de gel ; corrigé à la conversion, plus aucun avertissement.

## Preuves exécutées

- **Contrôles de gestes** (`test_gesture_alignment.py`) : sur l'ancien film, les deux échouent (confirmation à 8,433 s hors de la fenêtre 10,375 à 11,641 s ; 0 pixel de pointeur). Sur le nouveau, les deux passent : confirmation à 10,567 s, soit 0,19 s après le début de la phrase ; 24 pixels de pointeur à chacun des trois gestes sur l'image réduite.
- **Garde** : 10 tests sur 10 dans `test_kokoro_guard.py`, 12 sur 12 avec les contrôles de gestes. Les 9 tests de `form-pilot/` passent toujours.
- **Reproductibilité sur ce Mac** : brouillon témoin et deux rendus gardés, même empreinte SHA-256.
- **Planche** de huit images de la capture lue par l'agent : le pointeur ne masque ni le texte saisi ni le libellé du bouton ; le halo de clic est visible sur les deux champs et sur le bouton.

## Limites

- La capture n'est pas reproductible à l'octet : chaque prise donne un fichier différent. Celle-ci est figée par empreinte dans le manifeste ; ses événements horodatés sont dans `capture-events.json`.
- `capture.cjs` appelle Playwright par un chemin absolu propre à ce Mac.
- Le silence de 7,8 à 10,4 s subsiste ; le pointeur s'y déplace vers le bouton à partir de 9,5 s.
- Compréhension sans image, conformité de la voix au script, cadence constante : toujours non vérifiées.
- Les contrôles de gestes regardent des pixels et des repères ; ils ne disent pas si le film se comprend.

## Suite

Visionner `form-kokoro-pointeur.mp4` et consigner l'approbation ou le refus de l'empreinte `ab040730…7125`.
