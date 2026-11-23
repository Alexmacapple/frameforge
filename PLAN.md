# PLAN — Validation progressive

## Phase 0 : pré-revue et faisabilité
- Fixer SHA et licences des dépendances.
- Vérifier HyperFrames sur un rendu de 5 secondes, CLI et repli.
- Vérifier agent-browser sur une capture courte avec repères temporels.
- Comparer les interfaces existantes avant d'écrire un adaptateur.
Sortie : GO/NO-GO documenté, aucun moteur nouveau.

## Phase 1 : chemin vertical minimal
- Scénario autorisé de trois gestes.
- Narration locale et repères audio-first.
- Composition HyperFrames et MP4 de 30 secondes.
- SRT et transcription.
Sortie : premier film, pas seulement des captures.

## Phase 2 : preuves et robustesse
- Contrôles déterministes des fichiers et de la timeline.
- Vérification de confidentialité et revue humaine.
- **Revue éditoriale du film complet**, distincte des contrôles FFmpeg : continuité des actions et résultats, rythme, cadrage et lisibilité dans le format cible, fidélité au scénario et aux sources, intelligibilité de la narration et compréhension des informations essentielles sans vision. Vérifier aussi que les sous-titres ne masquent pas les gestes.
- Pour chaque défaut, consigner l'horodatage ou le plan concerné, l'observation, le statut **bloquant / tolérable / non vérifié**, la justification et les contrôles à refaire après correction. Une appréciation humaine ne remplace pas une mesure déterministe, et inversement.
- Tester les corrections localisées sur une version déterminée, sans écraser les ajustements humains déjà approuvés ; revérifier les dépendances affectées avant toute validation ou diffusion.
- Échec/reprise, cache et second rendu comparé.
Sortie : rapport de recette avec résultats observés.

## Phase 3 : extension conditionnelle
- Montage de rushes, puis vidéo pédagogique, uniquement si les besoins et lacunes sont confirmés.

## Portes de décision
P0 : rendu HyperFrames fonctionne dans l'environnement cible.
P1 : capture et narration sont alignées sur trois gestes observés.
P2 : QA et revue ne déclarent pas de faux succès.
P3 : réexécution avec différences explicables.

## Travail non autorisé par ce cadrage
Aucun déploiement, publication externe, installation système ou traitement de données réelles sensibles sans accord spécifique.

## Clôture du cadrage métier — grill-with-docs (23 novembre 2026)
- Cinq tours terminés ; décisions D1 à D16 validées. Glossaire métier consolidé dans [GLOSSARY.md](GLOSSARY.md).
- Aucun ADR nécessaire avant les essais : les éventuels arbitrages durables de rendu, capture, reprise ou stockage dépendront de preuves techniques.
- **GO pour préparer FF-01 et FF-02**, pas validation de faisabilité ni autorisation implicite d'installation système.
- **FF-01** : vérifier l'accès à l'environnement macOS cible, fixer versions et SHA d'HyperFrames, rendre cinq secondes, décoder intégralement ; si nécessaire mesurer un repli FFmpeg avec garanties équivalentes.
- **FF-02** : vérifier l'accès à l'environnement, l'autorisation du site, du scénario et de la session, puis capturer trois gestes, leurs résultats et horodatages.
- Les formats définitifs du manifeste, la synchronisation complète, le cache/reprise et les modalités de validation ne bloquent pas ces deux expériences ; les traiter dans les issues déjà ouvertes.
- Préserver les preuves et les statuts distincts ; aucun faux PASS en cas d'outil indisponible ou d'essai non exécuté.

## État réel au soir du 23 novembre 2026

Section rédigée par un agent et validée par Alex le 23 novembre 2026 (« oui aux quatre » : feuille de route, sort des outils, clôture de FF-03 et FF-04, règle des PR). Elle n'autorise aucune diffusion.

### La feuille de route existe : elle est dans FF-13

Le rapport de contre-revue d'AlexDot, publié sur l'issue FF-13, fixe quatre expériences dans l'ordre et une liste de choses à ne pas construire. Son verdict : « Conserver le socle, terminer la recette du premier film, puis le mettre à l'épreuve sur des rushes. Rien de nouveau à construire maintenant. » Publier ce rapport ne valait pas l'adopter ; **Alex l'a adopté comme ordre de travail le 23 novembre 2026.**

### Où en sont les quatre expériences

1. **Recette du film précis (FF-06, FF-07, FF-08, FF-09) : partielle.**
   - Fait : deux films identifiés par empreinte et approuvés à l'écoute et au visionnage, le formulaire `ab040730…7125` et la réservation `9c834228…f543` ; gestes et résultats relus sur planche ; sous-titres, transcription et composition au même texte ; résultat de chaque geste affiché pendant la phrase qui l'annonce.
   - Reste : compréhension de chaque information essentielle sans l'image ; comparaison de ce qui est prononcé aux sous-titres ; ouverture des sous-titres externes dans le lecteur prévu ; droits et confidentialité du lot, métadonnées comprises.
2. **Cas temporel adversarial (FF-06) : non fait.** Ni geste ralenti, ni phrase qui déborde n'ont été essayés.
3. **Révision et reprise (FF-10) : non faite telle que décrite.** Un élément s'en approche : la correction du pointeur a changé les images en conservant la piste son approuvée, identique à l'octet. Le verrouillage d'un choix humain, l'interruption et la reprise ne sont pas essayés.
4. **Deux rushes sans navigateur (FF-11) : inchangé aujourd'hui.** Verdict écrit du dépôt : pilote local clos à périmètre restreint, issue ouverte.

### Ce qui a été construit hors de cette feuille de route

Le 23 novembre, sur recommandations successives de l'agent, validées une à une par Alex sans que le rapport de FF-13 ait été relu :

- une fiche de film (manifeste de provenance) et son contrôle, pour FF-04 ;
- un générateur de composition, sous-titres et transcription depuis la fiche ;
- un second film de démonstration web, la réservation de salle ;
- un dossier d'outils communs, `film-chain/`, avec un garde de rendu partagé.

Le rapport demandait de corriger dans le flux existant et de ne rien construire de nouveau. Ces outils ne sont ni un orchestrateur, ni un éditeur, ni un cache ; ils restent du travail que la feuille de route ne demandait pas, et un second film web ne remplace pas l'essai sur des rushes. **Décision d'Alex : les conserver, sans rien y ajouter avant la fin des quatre expériences.**

### Constats ouverts

- **Contre-revue adverse du garde : faite, neuf failles corrigées.** Un relecteur indépendant a rendu neuf constats, tous reproduits puis corrigés par les PR 16 à 21 (issue 15) : films trafiqués acceptés, fiche qui s'approuvait elle-même, tests aveugles à la suppression d'un contrôle, résultat observé sans observation, outil d'empreintes trop permissif, film révoqué qui se rendait. Les deux films approuvés ressortent identiques à l'octet après chaque correction. Restent deux soupçons non reproduits, et la revue de Codex, interrompue par son fournisseur avant son rapport.
- **Médias approuvés non versionnés.** Une capture figée a été écrasée puis restaurée. Une copie locale existe désormais hors dépôt, sur le même disque.
- **Synthèse Kokoro non reproductible à l'octet**, même avec graine ; environnement de synthèse installé dans un dossier temporaire.
- **Aucune PR avant le soir du 23 novembre** : le travail de la journée est allé directement sur `main`, sans relecture préalable. Les corrections de la contre-revue sont les premières à être passées par des PR.

### Ordre de travail

1. Corriger les failles confirmées par la contre-revue adverse : fait (PR 16 à 21).
2. Finir l'expérience 1 sur un des deux films approuvés : écoute sans l'image, voix comparée aux sous-titres, sous-titres externes dans le lecteur prévu, droits et confidentialité.
3. Expérience 2 : un geste ralenti ou une phrase qui déborde, sur une scène existante.
4. Expérience 3 : correction d'une scène, interruption, reprise, sur copies.
5. Expérience 4 : deux rushes sans navigateur.
6. Aucun nouvel outil avant la fin de l'expérience 4, sauf pour corriger un écart constaté.

### État des issues

Les commentaires d'état du 23 novembre donnent le détail. FF-03 et FF-04 sont fermées sur décision d'Alex ; les autres restent ouvertes.

- **FF-01** : garder ouverte. Rendu de 5 s acquis ; manquent le SHA d'HyperFrames et le cas de repli.
- **FF-02** : garder ouverte. Repères précis, action incertaine et sélecteur ambigu non couverts.
- **FF-03** : fermée. Capture réelle intégrée, rendu décodable, écart documenté.
- **FF-04** : fermée sur ses trois critères d'origine. Les critères ajoutés (types de plans, rôle et session) restent partiels et sont à reprendre si l'essai sur des rushes les rend nécessaires.
- **FF-05** : garder ouverte. Licence de la voix non documentée, pas de cache, échec de synthèse non testé.
- **FF-06** : garder ouverte. Expérience 2 à faire.
- **FF-07** : garder ouverte. Films de 15 et 16 s pour une cible d'environ trente ; voix non comparée au texte.
- **FF-08** : garder ouverte. Expérience 1 à finir.
- **FF-09** : garder ouverte. Confidentialité non vérifiée partout.
- **FF-10** : garder ouverte. Expérience 3 à faire ; tolérances de comparaison non documentées.
- **FF-11** : garder ouverte. Expérience 4.
- **FF-12** : garder ouverte, non commencée, reportée après l'expérience 4 comme le demande le rapport.
- **FF-13** : recommandations adoptées comme ordre de travail ; garder ouverte jusqu'à la fin des quatre expériences.
- **FF-15** : contre-revue adverse du garde. Neuf constats corrigés ; garder ouverte pour les deux soupçons non reproduits.

### Règle de travail

Adoptée par Alex le 23 novembre 2026. Tout changement de `film-chain/` ou du garde d'un film passe par une branche et une PR, relue avant fusion. Les comptes rendus d'expérience peuvent rester en commits directs.
