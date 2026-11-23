# FF-10 — Interruption, relance et décision sur le point d'entrée

23 novembre 2026. SHA de départ : b0701d4.

## Protocole exécuté

Depuis le MacBook Pro, un script d'intégration déclenche guarded_export.py sur une copie locale de FF-12. Pour rendre l'interruption observable, un wrapper ralentit la lecture FFmpeg (option -re) ; le processus et son groupe sont interrompus par SIGTERM après deux secondes. Le script vérifie l'absence de sortie finale, nettoie les répertoires temporaires abandonnés et relance l'export sans ralentissement.

## Résultats

- Processus interrompu : code -15 (SIGTERM).
- Aucun MP4 final après interruption : PASS.
- Un répertoire temporaire abandonné après l'arrêt brutal ; nettoyage explicite par le script d'essai.
- Relance complète : code 0, MP4 produit.
- Empreintes SHA-256 des trois entrées avant/après : identiques.
- SHA-256 du MP4 après relance : 73c84ea720beabb588a4ac1e421871847eb55fa8d9ec6875b63e252595693597, identique au rendu antérieur.
- Résultats structurés : INTERRUPTION-RESULTS.json.

## Décision sur le point d'entrée

**Ne pas promouvoir maintenant guarded_export.py comme point d'entrée officiel de toute production FrameForge.** Il ne gère que deux blocs SRT et un remux MP4. Les autres scénarios utilisent encore des scripts d'expérience et HyperFrames ; les forcer à travers ce script serait une fausse généralisation.

Conserver ce point d'entrée comme référence de contrôle ciblé et décider du contrat de production lorsque le véritable chemin de rendu commun sera identifié ou implémenté. Ne pas créer un nouvel orchestrateur pour rendre obligatoire un contrôle qui n'a pas encore de périmètre de production.

## Limites

- La récupération après SIGTERM est **assistée par le script d'essai** ; pas de nettoyage automatique garanti après SIGKILL ou crash.
- La relance repart de zéro ; pas de checkpoint.
- Les contrôles ne sont pas obligatoires sur tous les chemins de rendu.
- Pas de preuve d'absence de contournement par un agent, ni d'approbation humaine formelle.
- Le film et les rushes NASA restent locaux ; aucune diffusion autorisée.

**Verdict : PASS technique pour interruption et relance à périmètre limité ; FF-10 non clôturé en tant que garantie produit générale.**
