# FF-10 — Contre-revue contradictoire de la V2

Date : 23 novembre 2026. SHA figé : 457d88e5722b9bf7d28efa95b0845e71a64390f2. **Verdict : PARTIAL PASS, ne pas promouvoir comme chemin officiel.**

## Indépendance et méthode

Revue effectuée après l'implémentation V2 ; il ne s'agit **pas** d'une contre-revue aveugle ni d'un second relecteur humain indépendant. Lecture du code exact, des protocoles et rapports, plus une contre-épreuve Python locale sur copies de HTML. Aucun rendu vidéo supplémentaire pendant cette revue. Les PASS de rendu et d'interruption proviennent des expériences précédentes et sont qualifiés comme preuves historiques.

## Constats par gravité

### P1 — Référence d'approbation non authentifiée (contre-épreuve exécutée)

Le code accepte --baseline comme simple chemin de fichier (guarded_hyperframes_v2.py, lignes 43-50) et le recopie dans le répertoire temporaire (lignes 60-62). Aucune empreinte attendue indépendante, aucun identifiant de version approuvée, ni contrôle d'origine humaine. Un agent pouvant modifier la référence peut remplacer celle-ci par la version candidate. **Contre-épreuve exécutée :** lorsque baseline et candidate sont remplacés par le même HTML modifié, preflight renvoie True ; avec la baseline originale et la modification du sous-titre 2, preflight rejette protected_caption2_changed. La comparaison de fichiers n'est pas une authentification d'approbation.

### P1 — Chemin facultatif et contournable

L'exécutable est un pilote local ; les projets conservent leurs scripts HyperFrames directs. Il n'existe pas de mécanisme prouvé rendant le précontrôle obligatoire pour le workflow produit. Ne pas revendiquer une protection globale.

### P2 — Isolation limitée aux entrées connues

CONFIG et MEDIA sont des listes fermées (lignes 16-17, 56-59). Les ressources indirectes de la composition (répertoires d'assets, sous-compositions, ressources distantes, fichiers chargés dynamiquement) ne sont pas toutes identifiées ni vérifiées. La copie est suffisante pour la fixture TodoMVC testée, pas pour une composition HyperFrames générale.

### P2 — Arrêt des descendants et nettoyage après crash

Le code supervise un groupe de processus (lignes 23-37, 76-84). Le SIGTERM testé est un résultat positif, mais il n'établit pas la maîtrise de tous les descendants détachés ni le nettoyage après SIGKILL ou arrêt machine. Le test différé de cinq secondes n'est pas une garantie absolue.

### P2 — Publication et vérification du résultat

La V2 décode intégralement le MP4 et crée le fichier final sans écrasement par os.link (lignes 85-93). Elle ne démontre pas la fidélité perceptive du sous-titre protégé à l'écran. La validation humaine n'est pas attachée cryptographiquement au film exporté.

### P2 — Test automatisé incomplet

Les expériences précédentes ont exécuté une interruption, une mutation temporaire puis une relance, mais il manque une suite de tests d'intégration répétables pour la V2 avec assertions sur les descendants et le MP4 après délai.

## Matrice

| Garantie | Verdict |
| --- | --- |
| Refus d'une modification du bloc 2 avec référence intacte | PASS, cas historique |
| Référence remplacée par un fichier modifié | FAIL, contre-épreuve locale |
| Isolation du rendu contre mutation temporaire de la source | PASS limité, cas historique |
| SIGTERM et relance complète | PASS limité, cas historique |
| SIGKILL et nettoyage après crash | UNVERIFIED |
| Ressources indirectes de projets variés | UNVERIFIED |
| Contrôle obligatoire dans FrameForge | NOT IMPLEMENTED |
| Qualité perceptive et approbation humaine finale | UNVERIFIED |

## Décision

**REUSE_EXISTING + EXPERIMENT.** Conserver le point d'entrée isolé pour FF-10. Avant adoption, lier une version approuvée à une empreinte ou preuve d'approbation vérifiée hors du fichier candidat ; choisir explicitement le workflow cible et rendre le contrôle obligatoire sur ce chemin ; vérifier les ressources indirectes ; automatiser les deux contre-exemples. Ne pas construire de moteur ni d'orchestrateur. FF-10 reste ouvert.

Aucun média NASA diffusé, aucun changement produit effectué dans cette contre-revue.
