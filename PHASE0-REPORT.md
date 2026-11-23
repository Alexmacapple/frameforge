# FrameForge — Phase 0, état des essais et décisions

Date : 23 novembre 2026. Revue en lecture seule des documents de cadrage et vérification des outils disponibles dans cet environnement isolé. Aucune modification GitHub.

## Observations mesurées
- Node.js : v22.16.0, présent.
- FFmpeg : 7.1.5, présent ; ffprobe disponible.
- `agent-browser` : exécutable non trouvé dans le PATH.
- `hyperframes` : exécutable non trouvé dans le PATH.
- Interrogation du registre npm : expiration du délai ; version/API non vérifiées.

## État des essais discriminants
| Référence | Essai | Statut | Condition de clôture |
|---|---|---|---|
| R01 | Trois interactions agent-browser et capture de médias/timestamps | BLOQUÉ | outil installé, environnement autorisé, trois événements et rushes inspectés |
| R02 | Narration longue et geste lent, sans coupe | NON EXÉCUTÉ | contrat temporel fondé sur les mesures R01 et R03 |
| R03 | Rendu HyperFrames de 5 s et décodage intégral | BLOQUÉ | CLI/API vérifiée, MP4 de 5 s réellement produit et décodé |
| R04 | Comparaison de deux rendus | NON EXÉCUTÉ | métriques et tolérances documentées |
| R05 | Confidentialité des captures, logs et métadonnées | NON EXÉCUTÉ | fixtures autorisées et politique de conservation |
| R06 | Cohérence documentaire V0.3 | CORRIGÉ LOCALEMENT | vérifier le contenu de README.md |
| R07 | Vision généraliste / MVP web | CORRIGÉ LOCALEMENT | vérifier INTENT.md |
| R08 | Description des informations visuelles essentielles | À DÉFINIR | contrôle éditorial et preuve de revue |

## Décisions de conception provisoires
- Horloge maître : timeline de composition en secondes ; enregistrer séparément temps monotone de capture et offsets des médias, sans supposer une précision non mesurée.
- Synchronisation : ne jamais accélérer ou tronquer une action ni une phrase sans décision éditoriale explicite ; conserver une marge de fin de scène.
- Reproductibilité : comparer durée, ordre des scènes, présence audio, sous-titres et intégrité des fichiers ; ne pas imposer une égalité binaire MP4.
- Confidentialité : utiliser des données de démonstration, inventorier médias temporaires et métadonnées ; revue humaine avant diffusion.
- Aucune compatibilité agent-browser → HyperFrames n'est encore démontrée.

## Prochaine exécution requise
Sur un environnement macOS autorisé : fixer SHA et versions HyperFrames/agent-browser ; exécuter le rendu HyperFrames 5 s ; mesurer trois interactions agent-browser ; relever les formats médias et horloges ; tester ensuite les deux cas temporels adversariaux. Consigner commandes, versions, logs, fichiers et résultats sans secrets.

## Verdict
`BLOCKED_ON_ENVIRONMENT` pour les essais R01–R03. Le cadrage peut être précisé, mais pas déclarer la faisabilité prouvée.
