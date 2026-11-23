# FF-10 — Mission de contre-revue indépendante

**Dossier à transmettre à un évaluateur qui n'a pas construit le pilote.** Le présent document est une demande, pas un rapport indépendant.

Dépôt : Alexmacapple/frameforge. Référence de lecture : commit 922536d. Périmètre : experiments/2026-11-23-macbook-pro/ff10-web-workflow-entrypoint et le wrapper ff10-hyperframes-guarded-integration/guarded_hyperframes_v2.py.

## Question

Le chemin npm du pilote V5 refuse-t-il vraiment toute modification non autorisée des sous-titres, voix, capture et fichiers de référence avant un rendu HyperFrames, et les garanties restent-elles valables après interruption ou altération concurrente ?

## Protocole indépendant

1. Lire d'abord uniquement les sources du point d'entrée, les tests et les références, sans consulter les rapports ni les verdicts antérieurs.
2. Construire sa propre liste d'invariants et de contre-exemples ; exécuter les tests avec preuves et timecodes si une inspection vidéo est effectuée.
3. Chercher activement : modification des fichiers annexes, symlinks, substitution de manifeste, changement de source pendant snapshot, écrasement de sortie, processus orphelins après interruption, chemins de rendu et publication alternatifs, droits sur les empreintes de référence.
4. Examiner si l'assertion « le film respecte la correction humaine » est fondée sur une approbation humaine de la V5 ou seulement sur une fixture.
5. Figer les conclusions avant de consulter ENTRYPOINT-ADVERSARIAL-REVIEW.md, REGRESSION-REVIEW.md et les décisions antérieures.
6. Comparer ensuite, classer les écarts en erreur factuelle, preuve insuffisante ou préférence technique.

## Livrable attendu

Déclaration d'indépendance, SHA de lecture, environnement, commandes et sorties, défauts reproduits et non reproduits, conséquences, remédiations minimales, verdict PASS/FAIL/UNVERIFIED par garantie et verdict global. Aucun média publié. Ne pas confondre précontrôle local et permission de publication.

**Limite de la mission :** la recette humaine de la V5 ne peut pas être déclarée PASS par un agent sans retour perceptif humain.
