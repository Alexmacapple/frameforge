# FF-10 — Interruption et concurrence HyperFrames

23 novembre 2026. Protocole figé avant exécution.

Sur une copie de la composition déjà validée, tester deux risques indépendants :
1. interrompre le processus du rendu HyperFrames après démarrage, vérifier qu'aucun MP4 final n'est utilisable, relancer sur les mêmes entrées et contrôler le MP4 ;
2. pendant un autre rendu, modifier temporairement le sous-titre 2 protégé, puis le rétablir avant la vérification finale. Mesurer si le contrôle avant/après détecte la mutation transitoire ; ne pas inférer qu'elle affecte le film sans vérification de ses images.

Conserver les entrées et la vidéo de référence intactes. Les médias restent locaux. Verdict PASS/FAIL/UNVERIFIED distinct pour chaque garantie. Ne pas ajouter de moteur ni d'orchestrateur.
