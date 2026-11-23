# FF-10 — Point d'export gardé, implémentation minimale

23 novembre 2026. **Verdict : PASS sur le point d'export expérimental ; protection globale FrameForge NOT DEMONSTRATED.**

## Inspection préalable

La recherche des fichiers suivis sur main et la lecture de SPEC.md, README.md, AGENTS.md montrent des scripts d'expérimentation et une architecture d'adaptateurs encore conceptuelle. Aucun point d'entrée produit centralisé de rendu/export n'a été identifié. Il serait inexact de présenter ce changement comme l'intégration d'une protection à tous les rendus FrameForge.

## Implémentation

- guarded_export.py : point d'entrée CLI Python standard, contrôle déterministe SRT avant remux FFmpeg.
- test_guarded_export.py : cinq tests de contrôle, sans nouvelle dépendance.
- Aucun changement aux rendus ou aux médias précédemment approuvés.
- Le contrôle exige exactement deux blocs SRT ; conserve à l'identique le second ; n'autorise que le retour à la ligne du premier ; refuse la sortie déjà existante. Re-vérifie les empreintes des trois entrées avant et après FFmpeg. Produit d'abord un fichier partiel puis le renomme à la fin.

## Tests réellement exécutés

- 5/5 tests unitaires PASS : modification autorisée, modification du bloc protégé rejetée, changement de timecode rejeté, ajout de bloc rejeté, absence de sortie pour un changement interdit.
- CLI autorisé : PASS, MP4 produit et décodable ; SHA-256 73c84ea720beabb588a4ac1e421871847eb55fa8d9ec6875b63e252595693597.
- CLI adversarial : BLOCKED avec motif protected_cue_2_changed ; aucun MP4 adversarial produit.
- Les fichiers médias et SRT de test restent locaux.

## Limites

- Il s'agit d'un **point d'export expérimental**, pas du chemin de rendu général de FrameForge.
- Un agent peut toujours appeler directement FFmpeg ou HyperFrames et contourner ce script. Aucun contrôle d'accès système ou garantie de non-contournement.
- La comparaison des empreintes ne constitue pas une transaction atomique face à une mutation concurrente entre contrôle et lecture FFmpeg.
- Les deux blocs et le type de modification sont codés pour ce pilote, pas pour tous les projets.
- La relance après interruption était prouvée dans le pilote précédent, mais **n'a pas été rejouée sur ce point d'entrée**.
- Aucune recette humaine du nouveau MP4. Droits de diffusion NASA non vérifiés.

## Décision

**BUILD_MINIMAL expérimental, REUSE_EXISTING produit.** Le contrôle est exécutable et testé, sans nouveau moteur ni orchestrateur. Avant d'annoncer un verrou produit, il faudra définir le véritable point d'entrée obligatoire, le périmètre de l'approbation humaine et le comportement de reprise. Ne pas clôturer FF-10 comme garantie générale.
