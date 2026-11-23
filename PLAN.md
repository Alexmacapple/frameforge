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
