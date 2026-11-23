# Formulaire, voix Kokoro — recette des trois gestes

23 novembre 2026, MacBook Pro. Film examiné : `form-pilot-kokoro/media/form-kokoro-native.mp4`, SHA-256 `0d9d0c9cb5d04f0d947b946f4072a84112e6cd2b0e987bde9490a567e7f392a5`, approuvé à l'écoute (KOKORO-NATIVE-EDITORIAL-APPROVAL.md). FFmpeg 9.0.1.

Ce document sépare ce qui a été mesuré, ce que l'agent a observé sur une planche d'images, et ce qui attend un verdict humain. Aucune ligne « observation de l'agent » ne vaut validation éditoriale.

## Méthode

- Détection des changements d'image par score de scène FFmpeg (seuil 0,0008), séparément sur la zone du formulaire (940 lignes du haut) et sur la bande des sous-titres (140 lignes du bas).
- Zones de parole : amplitude supérieure à 0,01 sur la piste décodée ; silences : `silencedetect` à −50 dB, 1 s au moins.
- Planche de dix images à 0,5 · 1,4 · 3,0 · 4,5 · 4,8 · 6,5 · 8,3 · 8,6 · 12,0 · 15,5 s, conservée en local (`form-pilot-kokoro/media/planche-trois-gestes.png`, non versionnée), lue par l'agent.
- Aucune transcription automatique de la parole : la concordance entre voix et script n'est pas mesurée.

## Mesures

Repères par geste, en secondes depuis le début du film :

- **Geste 1, saisie du nom.** Résultat visible à 1,233. Sous-titre de 1,500 à 4,300. Parole de 1,855 à 3,917. La parole commence 0,62 s après le résultat.
- **Geste 2, saisie de l'adresse.** Résultat visible à 4,633. Sous-titre de 5,200 à 8,167. Parole de 5,540 à 7,812. La parole commence 0,91 s après le résultat.
- **Geste 3, envoi et confirmation.** Résultat visible à 8,433. Sous-titre de 10,000 à 14,600. Parole de 10,375 à 14,154. La parole commence 1,94 s après le résultat.

Autres mesures :

- Chaque sous-titre encadre entièrement sa phrase : il apparaît 0,34 à 0,38 s avant la parole et disparaît 0,36 à 0,45 s après.
- Silences : 0 à 1,85 s, 3,94 à 5,54 s, 7,83 à 10,37 s (2,55 s), 14,17 à 16 s.
- Niveau intégré −19,7 LUFS, plage 5,1 LU, crête −5,4 dB. Aucun seuil n'est défini dans le projet : mesure consignée sans verdict.
- Transcription, SRT, VTT et sous-titres incrustés portent exactement le même texte.
- Deux variations d'image mineures à 1,000 s et 9,000 s (scores 0,0011 et 0,0019), sans changement lisible sur l'image à 1,1 s. Cause non identifiée ; hypothèse : clignotement du curseur ou frontière d'encodage.

## Observations de l'agent sur la planche

Pour chaque point : horodatage, observation, statut proposé, justification, contrôle à refaire après correction.

1. **1,233 s — nom saisi.** « Camille Martin » apparaît d'un coup dans le champ, contour de champ actif visible. Aucune frappe progressive, aucun pointeur. Statut proposé : tolérable. Le résultat est lisible et la narration le décrit ; la saisie instantanée vient de `fill()` dans la capture. À refaire si la capture change : repères et planche.
2. **4,633 s — adresse saisie.** « camille@example.test » apparaît d'un coup, même remarque. Statut proposé : tolérable.
3. **8,433 s — envoi.** Le message vert « Demande enregistrée pour Camille Martin. » apparaît. **Le clic sur « Envoyer la demande » n'est pas visible** : pas de pointeur, pas d'état enfoncé sur les images examinées. Statut proposé : à trancher par l'approbateur. SPEC.md classe bloquant un « geste ou résultat déterminant invisible » ; ici le résultat est visible, le geste ne l'est pas.
4. **7,83 à 10,37 s — résultat avant son annonce.** La confirmation s'affiche pendant un silence de 2,55 s et n'est commentée que 1,94 s plus tard. Statut proposé : tolérable, à confirmer. Aucune information n'est perdue, mais le spectateur voit le résultat avant qu'on lui dise que le formulaire est envoyé.
5. **Sous-titres et formulaire.** Sur les trois images sous-titrées, la bande ne recouvre ni les champs, ni le bouton, ni le message de confirmation ; la marge lue sur la planche est d'environ 70 lignes. Statut proposé : PASS sur les images examinées. Valeur approximative, non mesurée au pixel.
6. **Cadrage.** Le formulaire occupe les deux tiers supérieurs ; le tiers inférieur est vide hors sous-titres. Statut proposé : tolérable.
7. **Données affichées.** Seules des données fictives apparaissent (Camille Martin, camille@example.test) ; pas d'interface de navigateur ni d'autre fenêtre. Les dix images couvrent chaque état situé entre deux changements nets détectés. Statut proposé : PASS sur ces images ; les métadonnées du fichier ne sont pas inspectées ici.

## Non vérifié

- **Compréhension sans image.** À la lecture du script, le titre du formulaire (« Demande de documentation ») n'est jamais prononcé, l'adresse saisie est décrite sans être dite, et le message de confirmation est paraphrasé. Aucun test d'écoute sans image n'a été fait.
- **Voix conforme au script.** Non mesurée ; seule l'écoute de l'approbateur en répond.
- **Cadence constante**, gels et saccades : non mesurés.
- **Lisibilité à la taille de diffusion** : aucune destination n'est définie.

## Verdict humain

En attente, geste par geste : geste 1, geste 2, geste 3 (dont la question du clic invisible), délai d'annonce du geste 3, compréhension sans image.

Aucune diffusion autorisée. FF-08 et FF-10 restent ouverts.
