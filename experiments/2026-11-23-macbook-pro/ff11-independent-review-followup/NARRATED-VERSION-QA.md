# FF-11 — Version française narrée après contre-revue

Date : 23 novembre 2026. **Statut : DRAFT / recette humaine non effectuée.** Recommandations issues du rapport indépendant AlexDot transmis par l'utilisateur.

## Livrable local

Dossier local/ sur le MacBook Pro :
- eclipse-narrated-fr-subtitled-DRAFT.mp4, film de 13,5 s avec narration Kokoro ff_siwis en français et sous-titres français mov_text sélectionnables.
- captions-fr.srt et captions-fr.vtt ; transcript-fr.txt ; narration.txt ; voice-1.wav et voice-2.wav ; montage-contact-sheet.jpg.
- Deux extraits source découpés depuis les vidéos NASA déjà disponibles : A 3,5–9 s (5,5 s) et B 15,5–23,5 s (8 s).
- Source NASA et provenance : ../ff11-blind-editorial-v1/SOURCE-MANIFEST.json. Le MP4 et les médias NASA ne sont pas publiés sur GitHub.

## Contrôles exécutés

| Contrôle | Résultat |
| --- | --- |
| Rendu et décodage FFmpeg | PASS : 13,500 s, H.264/AAC, 405 images |
| Audio français généré | PASS technique : Kokoro ff_siwis, 4,275 s et 4,825 s, inséré vers 0,3 s et 6,2 s |
| Présence de la voix dans les deux plans | PASS technique : niveaux moyens mesurés autour de -21 à -23 dB dans les plages parlées |
| Piste française sélectionnable | PASS structurel : mov_text, langue fra |
| SRT et VTT français | PASS fichiers ; repères temporels issus des durées synthétisées, non validés par écoute |
| Animation distinguée de l'observation à l'oral | PASS sur le texte : « Schéma animé » et « Images de la NASA » |
| Images aux bornes et rejet du distracteur | PASS sur échantillons ; voir PREFLIGHT.md |
| Continuité narrative et compréhension sans image | UNVERIFIED : aucun test d'écoute indépendant |
| Lisibilité des bandeaux anglais hérités et du SRT français | UNVERIFIED : des textes anglais restent incrustés dans le média NASA |
| Droits de diffusion et crédit définitif | UNVERIFIED ; usage local de test uniquement |

SHA-256 du MP4 : bc1706b800c1928b5fa8fed008eed11d278fa8515fc21d7b841895339bce1994.

## Narration effectivement synthétisée

1. « Schéma animé : la Lune passe devant le Soleil. Son ombre atteint la Terre. »
2. « Images de la NASA : depuis l’espace, on voit cette ombre traverser l’Amérique du Nord. »

Le texte est un brouillon de narration, pas un jugement de compréhension. L'ombre peut être peu visible sur certaines images. Le montage ne doit pas être décrit comme une observation continue en temps réel.

## Recette à obtenir avant clôture

Deux personnes ne connaissant pas le brief doivent reformuler à la première écoute : la cause de l'éclipse, la nature animée du premier plan, et la signification de la tache sombre dans les images NASA. L'une commence sans image, l'autre avec image ; puis inverser. Consigner séparément leurs réponses, sans les orienter.

**Décision : CORRECT_EXISTING / REUSE_EXISTING.** Aucun nouveau moteur ni orchestrateur. Ne pas clôturer FF-11 ; ne pas diffuser la vidéo. La preuve de compréhension et les droits restent manquants.
