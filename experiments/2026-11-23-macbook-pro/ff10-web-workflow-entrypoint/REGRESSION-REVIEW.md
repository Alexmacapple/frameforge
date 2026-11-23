# FF-10 — Consolidation des contrôles de non-régression

23 novembre 2026. SHA de départ c0dcd51. **Verdict : PASS sur les suites ciblées ; revue humaine du film toujours UNVERIFIED.**

## Résultats exécutés

- Neuf tests du chemin npm web : 9/9 PASS.
- Quatre tests de conservation de correction sur deux rushes : 4/4 PASS.
- Cinq tests de référence épinglée : 5/5 PASS.
- Total : 18/18 PASS, exécution sur MacBook Pro.
- Première exécution des neuf tests : 8/9, une assertion de test incorrecte supposait que le précontrôle renvoyait None alors qu'il renvoie une valeur vraie. Assertion corrigée, puis les trois suites ont été rejouées avec succès. Aucun changement produit pour ce défaut de test.

## Garanties effectivement couvertes

- Le candidat autorisé est accepté.
- Le sous-titre 2 protégé et le sous-titre 3 ne peuvent pas être modifiés sur ce précontrôle.
- La source capture.webm ne peut pas être remplacée dans la composition sans rejet.
- Une référence de fixture falsifiée est rejetée.
- Une sortie MP4 déjà existante est conservée ; le wrapper refuse l'écrasement.
- Le script npm publish du **pilote seulement** renvoie un code non nul.
- Le script npm render du **pilote seulement** invoque le wrapper.
- Le MP4 local préexistant conserve l'empreinte attendue.

## Limites et suite

Ces tests ne démontrent ni l'absence de contournement par HyperFrames direct, ni la qualité perceptive de la V5, ni une approbation humaine du film. Ils ne testent pas l'exécution complète d'un nouveau rendu dans cette passe, ni une publication externe. L'approbation humaine de la formulation du rush B est distincte de la V5 Kokoro.

Décision : conserver FF-10 ouvert. Ne pas promouvoir le pilote en protection globale. Pour la clôture, recueillir un verdict humain sur le film V5 et sélectionner le point d'entrée officiel avant de généraliser le contrôle. Aucun média publié.
