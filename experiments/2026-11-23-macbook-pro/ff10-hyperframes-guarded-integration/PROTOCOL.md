# FF-10 — Intégration gardée sur une vraie composition HyperFrames

23 novembre 2026. Protocole avant exécution.

Réutiliser la composition HyperFrames FF-10 (TodoMVC, 16,166 s), sans modifier sa source. Protéger l'élément caption2 tel qu'il existe dans la version témoin. Autoriser uniquement le changement de couleur de fond de caption1 (du gris très sombre vers un gris légèrement différent), sans changer les mots ni les timecodes.

Le script de production de ce pilote doit exécuter le contrôle HTML AVANT la commande réelle HyperFrames 0.8.33. Scénario positif : rendu MP4. Scénario adversarial : modifier caption2, obtenir un refus sans lancer HyperFrames ni créer de MP4. Vérifier le décodage, le maintien des médias sources, et distinguer la protection de la source de la protection perceptive des pixels.

Statut : pilote sur un chemin identifié ; ne pas déclarer un point d'entrée universel.
