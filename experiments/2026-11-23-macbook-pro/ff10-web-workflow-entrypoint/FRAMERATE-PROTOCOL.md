# FF-10 — Contrôle de cadence après seconde contre-revue

23 novembre 2026. Protocole figé avant correction, SHA initial d97c4bd.

L'exigence 30 images/s est présente dans le protocole de sortie mais le validateur ne la vérifie pas. Ajouter une vérification de cadence vidéo réelle via ffprobe, distincte du nombre total d'images. Refuser une sortie à 24 images/s même si elle respecte la durée, les dimensions, le nombre minimal d'images et les pistes audio. Conserver l'acceptation de la V5 témoin à 30 images/s. Refaire un seul rendu V5 complet sur Mac avec la nouvelle vérification, sans publication ni approbation humaine implicite.
