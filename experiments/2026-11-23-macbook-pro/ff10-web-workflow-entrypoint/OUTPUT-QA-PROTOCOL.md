# FF-10 — Critères de sortie avant publication locale du MP4

23 novembre 2026. Protocole figé avant correctif, suite au FAIL de la contre-revue indépendante.

Pour le pilote V5 seulement, imposer au MP4 temporaire avant dépôt final :
- durée entre 16,10 et 16,23 secondes (attendu 16,166667) ;
- piste vidéo H.264, dimensions 1920 × 1080, cadence 30 fps, au moins 480 images ;
- au moins une piste audio AAC avec durée proche du film, pas de sortie vidéo seule ;
- empreinte du PCM audio décodé identique au témoin V5 déjà observé (f6819e9e643df7e29951eb2fba046111177c65b6334fa05c6defe2c04652ca86), pour ce test qui ne modifie pas la voix ;
- conserver le contrôle de décodage complet et la protection de la sortie existante.

Refuser avant dépôt final un MP4 H.264 de 0,5 seconde, 64 × 64, sans audio ; refuser également un film de bonne durée mais sans audio. Test positif sur V5 réelle. Ces vérifications ne prouvent pas à elles seules les trois actions visuelles ni l'intelligibilité de la voix. Ne pas généraliser ces seuils à d'autres projets.
