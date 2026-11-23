# FF-10 — Reproductibilité depuis un checkout neuf

23 novembre 2026. Protocole préalable au correctif.

Sur une copie propre de main, reconstruire les entrées locales du pilote V5 à partir des fichiers V5 versionnés et du package.json/asset-pins.json versionnés du pilote, sans récupérer le MP4 historique. Vérifier chaque empreinte, la référence HTML et le seul changement autorisé du sous-titre 1. Exécuter la suite de tests sans dépendre du MP4 historique ; le test de sortie réelle doit être SKIP explicitement en son absence. Vérifier ensuite un rendu HyperFrames réel sur le MacBook Pro si possible. Aucune donnée ou média supplémentaire publié.
