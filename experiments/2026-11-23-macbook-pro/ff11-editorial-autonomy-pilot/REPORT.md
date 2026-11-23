# FF-11 — Pilote de décision éditoriale, résultat contradictoire

Date : 23 novembre 2026. **Verdict : FAIL sur la justification du plan 2 ; PASS technique sur le rendu ; autonomie non démontrée.**

## Protocole

Brief et choix éditoriaux figés avant le rendu dans EDITORIAL-PLAN.md, commit 422d4cb. Corpus NASA déjà connu : Earth Views ISS, NISAR, Perseverance Mars. Choix : ISS 105–111 s, NISAR 158–165 s, rejet Mars. Le plan 2 était annoncé comme « une intervenante scientifique » avec parole.

Exécution : FFmpeg pour découper les deux vidéos ; HyperFrames 0.8.33 pour composer le film sans navigateur. MP4 local clips/ff11-editorial-draft.mp4, 13,000 s, 390 images, H.264/AAC, décodage FFmpeg complet PASS.

SHA-256 des extraits : ISS 417efb66e85c7e10c2479386babc44bc7c9cab15aec3830f90378cec58e85e08 ; NISAR 21f6b8e3c4fa4d067a038c0619c1bdaa60ec8bb5ee115ad1397692bd04cb5042.
SHA-256 MP4 : 205422c93ec282d38e3a3076dc64812ba6cc00568567c02e0b789b51c7f98618.

## Écarts mesurés

| Exigence | Observation | Verdict |
| --- | --- | --- |
| Écarter la vidéo Mars | Aucune source Mars dans le rendu | PASS |
| Montrer la Terre et l'ISS | Image à 2 s : Terre et station visibles | PASS sur échantillon |
| Deuxième plan = intervenante scientifique | Images à 10 et 12 s : fusée, satellite et animation ; **pas l'intervenante annoncée** | **FAIL** |
| Conserver une intervention humaine | Piste audio présente (-23,7 dB moyen entre 7 et 10 s). ASR tiny.en reconnaît une voix parlée ; intelligibilité et attribution non validées | PARTIAL |
| Rendu sans navigateur | 13 s, 390 images, décodage complet | PASS |
| Choix autonome sur sources inconnues | Le modèle connaissait déjà le corpus et les planches de contact | NOT DEMONSTRATED |
| Fidélité des sous-titres | Aucun SRT validé pour ce nouveau passage | NOT DONE |
| Droits de diffusion | Vérification source par source incomplète | UNVERIFIED |

## Analyse

Le choix des deux **titres** est pertinent au regard du brief, mais l'inférence « à 158–165 s, on voit une intervenante » est **fausse**. Les planches de contact consultées auparavant étaient trop espacées pour soutenir cette assertion. La présence d'une voix dans la bande son ne garantit pas que la personne soit visible à l'image.

**Conséquence :** ne pas valider un plan éditorial sur la seule base de métadonnées, d'un titre ou de captures trop espacées. Avant de rendre, vérifier une ou plusieurs images dans chaque intervalle proposé et comparer au critère explicite du brief. Cette vérification peut être réalisée avec FFmpeg déjà présent, sans ajouter d'outil.

## Décision

**FAIL éditorial conservé comme contre-exemple.** Ne pas retoucher rétrospectivement le plan figé pour le déclarer PASS. Si l'on veut tester une nouvelle proposition, créer une version distincte avec justification et contrôles pré-rendu. Le MP4 NASA reste local ; seul le plan, les rapports et les métadonnées de preuve sont versionnés. FF-11 reste ouvert.

Le corpus était connu du modèle, donc ce pilote ne constitue pas une évaluation indépendante d'autonomie éditoriale. Pour une telle évaluation, il faudra un brief neuf et des rushes non pré-analysés, puis une comparaison indépendante avec une référence humaine.
