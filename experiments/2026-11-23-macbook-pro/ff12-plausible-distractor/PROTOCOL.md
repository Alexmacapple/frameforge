# FF-12 — Test de sélection avec distracteur plausible

23 novembre 2026. Protocole figé avant téléchargement et inspection des images.

## Question produit

Un assistant peut-il choisir des passages montrant une **éclipse solaire observée depuis l'espace**, en distinguant les images d'une éclipse solaire d'autres événements astronomiques visuellement proches ? Le verdict doit dépendre du contenu des plans, pas des seuls titres.

## Brief

Proposer un montage de 12 à 16 secondes, en deux plans : (1) la Lune masque le Soleil ; (2) une observation du phénomène depuis l'espace. Ne pas insérer une éclipse lunaire ni confondre transit et observation d'une éclipse depuis la Terre. Pas de narration ni de publication avant la sélection et la contre-revue.

## Corpus de trois titres NASA identifiés par recherche, non visionnés

- A : GSFC_20150914_SDO_m11993_transit — SDO Transit - September 2015.
- B : GSFC_20170830_MultiSpacecraft_m12698_eclipse — What Spacecraft Saw During the 2017 Solar Eclipse.
- C : GSFC_20140408_LRO_M11516_Lunar — Understanding Lunar Eclipses.

A est un cas ambigu : un transit lunaire devant le Soleil peut ressembler visuellement à une éclipse solaire ; son adéquation au brief doit être jugée, pas présupposée. C est un distracteur proche, puisqu'il traite d'une éclipse mais pas solaire. B est un candidat a priori pertinent, sans garantie sur le contenu d'un intervalle précis.

## Conditions de preuve

1. Récupérer les variantes NASA et consigner URL, taille, durée, SHA-256.
2. Examiner des échantillons visuels de **toutes** les sources, y compris les candidates rejetées ; consigner au moins deux preuves horodatées par rejet.
3. Choisir ou rejeter chaque candidat avec motif, puis figer des intervalles avant rendu.
4. Inspecter début, fin et changements internes de chaque plan retenu ; ne pas annoncer PASS si une scène non vérifiée est nécessaire.
5. Vérifier la différence entre observation réelle, animation, transit et éclipse lunaire.
6. Séparer verdicts : pertinence, sélection, montage technique, compréhension sans image, droits et évaluation indépendante.
7. **Aucune validation indépendante n'est revendiquée** si l'assistant qui choisit est aussi celui qui contrôle. Une contre-revue distincte doit partir de ce protocole, des sources, et d'un gel sans les choix du premier assistant.

Aucune nouvelle architecture, aucun moteur de sélection, aucune issue créée automatiquement. Médias locaux uniquement.
