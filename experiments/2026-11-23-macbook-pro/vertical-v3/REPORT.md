# FrameForge V3 — capture instrumentée, horloges divergentes

Date : 23 novembre 2026. MacBook Pro Apple M2 Max, macOS 26.5.2. Versions : agent-browser 0.31.1, HyperFrames 0.8.33, FFmpeg 9.0.1. Site : TodoMVC React public, données fictives. **Expérience, pas MVP validé.**

## Protocole et incident

Le premier essai a échoué car un marqueur DOM injecté avant `record start` n'existait plus après démarrage de l'enregistrement. Un WebM incomplet a été écarté. Le protocole a été corrigé : injecter le marqueur **après** `record start`, puis passer son fond de rouge à vert.

Le second essai a réussi : trois actions (ajouter la première tâche, ajouter la deuxième, cocher la première) et trois assertions DOM positives, journalisées dans `events.json` avec `time.monotonic_ns()` et UTC. Les résultats observés sont respectivement une tâche, deux tâches, puis première tâche `completed=true`.

## Découverte principale : ne pas confondre horloges

Le journal monotone couvre environ **16,74 s** de la demande de démarrage à la fin de l'enregistrement, alors que le WebM décodable dure **9,5 s**. Les actions du journal sont environ à 3,78 s, 7,98 s, 12,14 s après la demande de démarrage ; les principaux changements d'image apparaissent vers **1,4 s, 3,7 s, 6,4 s** dans la vidéo.

Ces repères visuels ont été estimés en extrayant 10 images/s et en calculant des différences de pixels avec Pillow. Le marqueur de synchronisation produit de fortes différences autour de 0,6 et 1,0 s. L'association action → changement d'image est cohérente avec l'ordre et les assertions, mais **elle n'est pas une preuve frame-accurate** : aucun identifiant d'événement n'est inscrit dans la vidéo et aucune transformation d'horloge fiable n'a été démontrée. Le protocole capture la différence entre horloges ; il ne la résout pas encore.

## V3 rendue

- Narration locale française déjà utilisée dans la V2, repositionnée à **0,9 s**, **3,3 s**, **5,9 s** avant les changements visuels estimés.
- MP4 H.264 + AAC, durée **9,500 s**, 471590 octets, SHA-256 `bda462a57d8a0bd99bcf3e8cfd023eb77e71742fdc0dec95776fd8132f51da20`.
- Décodage FFmpeg intégral **PASS** ; présence de trois plages de parole mesurée par `silencedetect`. SRT/VTT/transcription générés avec temps éditoriaux, non validés à l'écoute.
- Le film est volontairement court, sans remplissage pour atteindre artificiellement 30 secondes.

## Évaluation FF-02 / FF-06 / FF-08

| Garantie | Statut |
| --- | --- |
| Trois actions et assertions DOM réelles | PASS |
| Capture vidéo décodable | PASS |
| Journal monotone des appels | PASS |
| Signal visuel de synchronisation | PASS technique, corrélation approximative |
| Correspondance temporelle précise action ↔ image | UNVERIFIED |
| Audio, MP4, SRT/VTT/transcription | PASS technique |
| Synchronisation perceptive et vérification des paroles | UNVERIFIED |
| Revue indépendante accessibilité/confidentialité | NOT RUN |
| Reproductibilité et comparaison avec méthode manuelle | NOT RUN |

## Décision

**REUSE_EXISTING** pour la production vidéo ; **BUILD_MINIMAL uniquement si** une nouvelle expérience démontre que les outils natifs ne permettent pas de relier les actions à la vidéo avec la précision nécessaire. Le premier composant éventuel serait une instrumentation ciblée des repères, pas un skill ni un orchestrateur.

Sources médias vocaux de V2 : `../vertical-v2/media/voice1.m4a`, `voice2.m4a`, `voice3.m4a`. Pour relancer le rendu, copier ces fichiers et `media/capture.webm` à côté de `index.html`, puis `npx --yes hyperframes@0.8.33 render -o prototype-v3.mp4`. La reproduction depuis le dossier Git n'a pas été relancée.
