# FrameForge — analyse du mécanisme natif d'enregistrement d'agent-browser

Date : 23 novembre 2026. Revue documentaire et statique du code source, **sans modification de l'installation agent-browser**.

## Versions et sources effectivement consultées

- Version installée sur MacBook Pro : **agent-browser 0.31.1** ; paquet npm local, Apache-2.0, dépôt officiel `vercel-labs/agent-browser`.
- Source exacte de cette version : https://github.com/vercel-labs/agent-browser/blob/v0.31.1/cli/src/native/recording.rs
- Branche `main` étudiée au commit **d2dfc782ccdd79d25a9b4f0acced9321789cecb8** : https://github.com/vercel-labs/agent-browser/blob/d2dfc782ccdd79d25a9b4f0acced9321789cecb8/cli/src/native/recording.rs
- Documentation actuelle : https://github.com/vercel-labs/agent-browser/blob/d2dfc782ccdd79d25a9b4f0acced9321789cecb8/docs/content/docs/recording.mdx

## Résultat 1 — version 0.31.1

Le code définit `CAPTURE_INTERVAL_MS=100` et `CAPTURE_FPS=10`. La tâche d'enregistrement exécute périodiquement `Page.captureScreenshot`, décode chaque image JPEG et l'envoie par pipe à FFmpeg avec `-f image2pipe -c:v mjpeg -framerate 10`. Elle compte les images transmises, mais ne transmet pas à FFmpeg les instants réels de capture.

**Conséquence** : la durée encodée dépend du nombre d'images acceptées à 10 images/s, non directement du temps réel écoulé dans le script. Cette mécanique est une explication technique cohérente avec les écarts mesurés dans les expériences V3.

## Résultat 2 — branche main examinée

Le mécanisme récent collecte les événements CDP `Page.screencastFrame` et lit `metadata.timestamp`, avec une valeur de repli si absente. Il conserve aussi un temps écoulé et un instant de capture dans `CapturedVideoFrame`. En cas de densité insuffisante, une voie de capture par captures d'écran peut prendre le relais.

L'encodeur diffuse les images vers FFmpeg selon une cadence demandée ; il peut maintenir la dernière image entre deux captures. La documentation indique 30 images/s par défaut, `--fps` de 1 à 60, `--cursor`, `--contact-sheet`, et un retour `capturedFrames` au stop. Il existe une gestion plus explicite des délais et du retard d'encodage.

**Limite** : le code inspecté ne démontre pas un export public, image par image, de la correspondance entre `metadata.timestamp`, les événements DOM et les timestamps de présentation du média. La présence de métadonnées internes ne vaut pas contrat d'API.

## Décision

1. **REUSE_EXISTING** : ne pas écrire d'adaptateur de synchronisation sur la base des seuls échecs observés avec la version 0.31.1.
2. **EXP** : essayer la version récente dans un environnement isolé, sans remplacer la version globale ; mesurer les durées, les images encodées, les marqueurs et la corrélation avec les assertions DOM.
3. **BUILD_MINIMAL uniquement si nécessaire** : si la version récente ne fournit pas de preuve temporelle exploitable, envisager un export ciblé des événements/frames, avec test d'équivalence et non-régression. Aucun nouveau moteur, skill ni orchestrateur.
4. **FF-06/FF-08 restent ouverts** : pas de synchronisation exacte démontrée ni de revue audiovisuelle indépendante.

Aucun test de la version récente n'a été exécuté dans cette revue.
