# REPRISE — FrameForge

Dernière mise à jour : 25 novembre 2026. Référence de la contre-revue : `4f2c9f69c4c5bb666ea712ee40bdbe68dd7a19e5` (SHA historique, pas HEAD courant). Vérifier HEAD au démarrage.

## Prochaine action
Reprendre [#47 — film de référence](https://github.com/Alexmacapple/frameforge/issues/47), en suivant [le brief de passation](https://github.com/Alexmacapple/frameforge/issues/47#issuecomment-7153851626). Sujet validé : accessibilité des fenêtres modales, français, environ 60 secondes. Page exacte à sélectionner et valider. Vérifier la disponibilité du Mac et des dépendances ; #43 est clôturée mais Kokoro sur Mac Studio reste à vérifier. Dernier constat : MacBook Pro hors ligne, Mac Studio non connecté à Desktop Commander. Aucun rendu de ce film lancé.

## Ordre opérationnel
1. Lire AGENTS.md, README.md, WHY.md, INTENT.md, SPEC.md, PLAN.md et les tickets actuels. Vérifier branche, SHA, modifications locales et dépendances ; ne pas écraser le travail existant.
2. Produire #47 avec la chaîne existante `experiments/2026-11-23-macbook-pro/film-chain/`, selon son README et ses contrats. Mesurer temps, interventions, erreurs et reprises sans ajouter de skills.
3. Vérifier les exigences pertinentes #35–#39 (compréhension sans image, concordance voix/sous-titres, lecteur, licence). Les validations humaines et droits restent distincts du PASS technique.
4. Exploiter les manques observés dans [#56](https://github.com/Alexmacapple/frameforge/issues/56) selon [la contre-revue](https://github.com/Alexmacapple/frameforge/issues/56#issuecomment-7153717541) : COMPOSE, recherche orientée besoin avec skill-researcher et catalogue find-skills, sans installation par défaut. Essai visuel HyperFrames local uniquement si besoin démontré. Aucun nouveau méta-skill.
5. #48 : montage de rushes lorsque les médias autorisés sont fournis. Les autres tickets restent suivis selon leurs dépendances et labels ; ne pas les fermer sur la seule base de ce document.

## Points à surveiller
#40/#41 (approbation de fiche), #44 (sauvegarde), #46 (sort de V5), et thèmes #5–#12/#15 : consulter leur état courant. PLAN.md contient l'historique et le découpage en tickets. Les labels ready-for-agent, ready-for-human, needs-info et plus-tard orientent la reprise ; vérifier leur actualité.

## Règles
GitHub (issues et preuves) reste la source de vérité du suivi. En cas de divergence, vérifier les décisions humaines et les preuves les plus récentes ; ne pas arbitrer silencieusement. Aucun contournement du garde, transfert de média ou diffusion sans autorisation explicite. Respecter PUBLICATION-POLICY.md et la règle de PR pour film-chain et garde. Aucune publication de code ou modification distante sans accord spécifique.

## Mise à jour de la passation
En fin de session, actualiser ce fichier localement avec date, SHA de travail, preuves, tickets, blocages et prochaine action concrète. Ne publier la mise à jour distante qu'avec autorisation. Ne pas dupliquer les rapports ou l'historique de PLAN.md.
