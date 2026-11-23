# HyperBD — étude d'inspiration pour FrameForge

**Date :** 23 novembre 2026  
**Statut :** étude documentaire, sans installation ni reprise de code  
**Verdict :** `EXTRACT_ONLY + REUSE_EXISTING`  
**Source principale :** [flavien-ia/hyperbd](https://github.com/flavien-ia/hyperbd), version annoncée **0.16.2** dans le README et le manifeste du plugin.  
**Destination :** [FrameForge](https://github.com/Alexmacapple/frameforge), studio vidéo généraliste dont le premier cas est une courte démonstration web réelle et vérifiable.

## 1. Objet et portée

Examiner les mécanismes de création de bandes dessinées de HyperBD susceptibles d'améliorer la conception, la production, la correction et la validation des vidéos FrameForge. **Une analogie métier n'est pas une preuve de faisabilité technique.**

La revue a porté sur le README, le manifeste du plugin, SECURITY.md, CHANGELOG.md et les skills `bd-brief`, `bd-scenario`, `bd-dialogues`, `bd-planche-test`, `bd-planches`, `bd-lettrage`, `bd-voix`, `bd-audit` et `bd-album`. Il s'agit d'une analyse de documentation et de procédures ; **aucune production HyperBD ni aucun banc de tests HyperBD n'a été exécuté**. Les affirmations de coût et de performance du projet sont rapportées comme telles, non vérifiées indépendamment.

## 2. Mécanismes réellement décrits dans HyperBD

- **Cinq temps métier :** fondation/brief, univers, scénario, voix et dialogues, production des planches. L'atelier Studio Entremondes conserve univers, scènes, images et décisions.
- **Brief orienté message :** public, canal, format, ton, distance de transposition, éléments intouchables et incertitudes de la source (`bd-brief`).
- **Découpage avant génération :** chaque case décrit valeur de plan, angle, action, texte, emplacement et références propres ; le gabarit précède la production (`bd-dialogues`).
- **Épreuve verticale représentative :** une vraie scène et un vrai script passent par la chaîne entière avant le lancement de l'album (`bd-planche-test`).
- **Production progressive :** cases produites séparément, puis planche assemblée ; contrôle avec références de style et continuité de la planche précédente (`bd-planches`).
- **Correction selon le défaut :** valider, itérer, retoucher localement ou régénérer. La documentation annonce une préservation au pixel près hors de la zone retouchée dans l'atelier ; cette garantie n'est pas transposable telle quelle au montage vidéo.
- **Texte indépendant du visuel :** le lettrage dérive du script puis devient la référence éditoriale ; une correction humaine ne doit pas être écrasée par une nouvelle dérivation. Les traductions suivent le texte validé (`bd-lettrage`).
- **Jugement et mesures séparés :** relecteurs en aveugle pour les choix qualitatifs ; épreuve d'attribution des voix anonymisées et score calculé par script (`bd-voix`). Attention aux biais de thème et de répartition des répliques.
- **Audit de cohérence :** lots disjoints, référentiel et journal communs ; vérification des rappels, contradictions, continuité et fidélité aux sources ; consolidation des doublons (`bd-audit`).
- **Jalons et reprise :** plan de production, première scène et album relu soumis à signatures dans les modes guidés ; reprise depuis l'état de l'atelier ; suivi des coûts et plafonds (`bd-album`).
- **Sécurité et provenance logicielle :** séparation des secrets, consentement aux dépenses, contrôles d'archives et signatures décrits dans SECURITY.md. Ce sont des choix du projet HyperBD, pas des garanties automatiquement héritées par FrameForge.

## 3. Matrice de transposition

| Enseignement | État dans FrameForge | Décision | Preuve ou limite |
| --- | --- | --- | --- |
| Storyboard par plan : cadrage, geste, résultat, narration | Précisé dans `SPEC.md` | **REUSE_EXISTING / intégré conceptuellement** | Pas encore de test systématique avant rendu |
| Planche test sur scène réelle | Chemin vertical déjà prévu dans `PLAN.md` | **REUSE_EXISTING** | Le prototype technique n'est pas une validation éditoriale |
| Séparer texte, image, narration et sous-titres | `SPEC.md` et livrables MVP | **REUSE_EXISTING** | Concordance perceptive encore à vérifier |
| Retouches locales et conservation des choix humains | Reprise ciblée et contrôles affectés déjà prévus ; précisés dans `SPEC.md` | **REUSE_EXISTING / à éprouver** | Aucune garantie technique d'immuabilité pixel/son démontrée |
| Défauts bloquants versus tolérables | Précisé dans `SPEC.md` et `PLAN.md` | **Intégré conceptuellement** | Critères et jugement à tester sur des films réels |
| Revue du film entier, pas seulement de plans isolés | Ajoutée dans `PLAN.md` | **Intégré conceptuellement** | Revue audiovisuelle indépendante encore ouverte |
| Journal des variantes retenues/écartées et raisons | Journal de preuves et décisions déjà prévu | **EXP différée** | Éviter un nouvel « établi » sans besoin démontré |
| Jalons de validation : storyboard, scène témoin, film | Validation des scènes, film et approbation humaine prévue | **EXP ciblée** | Ne pas multiplier les signatures sans bénéfice observé |
| Audit des promesses narratives sans résolution et des résultats sans préparation | Revue de cohérence générale prévue | **À tester dans la recette existante** | Pertinent surtout pour les vidéos pédagogiques plus longues |
| Comparaison aveugle de deux montages ou voix | Non nécessaire au prototype unique | **P2, différer** | Exige un protocole qui évite les biais et une mesure utile |
| Traduction sans redessiner/régénérer | Sous-titres et voix séparés | **Extension conditionnelle** | Synchronisation, durée des langues et accessibilité à étudier |
| Budgets, plafonds et coûts réels | Pas de boucle payante démontrée dans le MVP local | **Différer** | À activer si génération facturée ou volume significatif |
| Bibles de personnages, décors, casting, atelier distant | Hors du cas d'usage initial | **REJECT** | Spécifique à la bande dessinée narrative |
| Nombreux skills et orchestration d'album | Contraires au principe minimal actuel | **REJECT** | Aucun manque de capacité justifiant cette complexité |

## 4. SWOT relatif à FrameForge

**Forces :** méthode métier explicite, découpage avant fabrication, arbitrages conservés, revue indépendante, reprise et protection des validations.

**Faiblesses :** forte spécialisation bande dessinée ; le fonctionnement complet dépend de l'atelier Studio Entremondes ; les bénéfices ne sont pas démontrés pour un pipeline vidéo.

**Opportunités :** réduire les défauts de cadrage, éviter les régressions lors des retouches, renforcer la compréhension sans vision, distinguer qualité technique et qualité narrative.

**Risques :** importer une usine à skills, surmultiplier les étapes et signatures, faire confiance à une auto-notation, imposer une métrique de synchronisation sans ancrage éditorial, confondre image test et vidéo validée.

## 5. Application déjà effectuée dans FrameForge

- `SPEC.md` : section « Précisions éditoriales par plan — extraction HyperBD » : cadrage, échelle de lecture, résultat attendu, informations essentielles à narrer, défauts bloquants/tolérables et correction ciblée.
- `PLAN.md` : revue éditoriale du film complet distincte des contrôles FFmpeg, observations localisées, décisions de correction et revérification des éléments affectés.
- `INTENT.md`, `AGENTS.md` et `GLOSSARY.md` : garanties existantes conservées, sans duplication.
- **Aucun nouveau skill, orchestrateur, moteur, format obligatoire ou dépendance** introduit à la suite de l'étude.

## 6. Hypothèses à éprouver sans nouvelle architecture

1. Sur le prochain film, rédiger pour chaque plan une courte description du geste, de son résultat visible, du cadrage et de ce qu'une personne sans vision doit comprendre ; mesurer si cela détecte les erreurs **avant** le rendu.
2. Lors d'une correction de cadrage, de sous-titre ou de voix, vérifier que les segments et validations non affectés sont réellement préservés.
3. Pendant la revue du film complet, rechercher explicitement les informations promises mais jamais montrées et les résultats montrés sans explication.
4. Pour les futures productions plus longues, tester un journal léger des variantes écartées et un jalon de validation de la première scène. Ne les pérenniser qu'après gain démontré.

Les expériences de FrameForge ont déjà montré qu'un MP4 décodable et des assertions DOM positives ne prouvent pas la lisibilité, la synchronisation perceptive ni l'accessibilité. Cette étude **ne change pas** les statuts de FF-06/FF-08 et n'autorise pas la diffusion.

## 7. Décision

**`EXTRACT_ONLY + REUSE_EXISTING`** : conserver HyperBD comme référence méthodologique et ses liens précis ; ne pas installer le plugin dans FrameForge et ne pas copier son atelier ou son système de skills. Les apports immédiats sont documentés dans les fichiers existants. Les autres idées sont des hypothèses à vérifier sur des besoins concrets, pas une feuille de route obligatoire.

## 8. Sources

### HyperBD

- [Dépôt et README](https://github.com/flavien-ia/hyperbd)
- [Brief](https://github.com/flavien-ia/hyperbd/blob/main/skills/bd-brief/SKILL.md)
- [Scénario](https://github.com/flavien-ia/hyperbd/blob/main/skills/bd-scenario/SKILL.md)
- [Découpage et dialogues](https://github.com/flavien-ia/hyperbd/blob/main/skills/bd-dialogues/SKILL.md)
- [Planche test](https://github.com/flavien-ia/hyperbd/blob/main/skills/bd-planche-test/SKILL.md)
- [Production des planches](https://github.com/flavien-ia/hyperbd/blob/main/skills/bd-planches/SKILL.md)
- [Lettrage](https://github.com/flavien-ia/hyperbd/blob/main/skills/bd-lettrage/SKILL.md)
- [Voix](https://github.com/flavien-ia/hyperbd/blob/main/skills/bd-voix/SKILL.md)
- [Audit](https://github.com/flavien-ia/hyperbd/blob/main/skills/bd-audit/SKILL.md)
- [Pilotage de l'album](https://github.com/flavien-ia/hyperbd/blob/main/skills/bd-album/SKILL.md)
- [Sécurité](https://github.com/flavien-ia/hyperbd/blob/main/SECURITY.md)
- [Historique des versions](https://github.com/flavien-ia/hyperbd/blob/main/CHANGELOG.md)

### FrameForge

- [INTENT.md](../INTENT.md)
- [SPEC.md](../SPEC.md)
- [PLAN.md](../PLAN.md)
- [AGENTS.md](../AGENTS.md)
- [GLOSSARY.md](../GLOSSARY.md)

**Note de méthode :** les liens vers `main` sont évolutifs. La présente étude porte sur l'état documentaire consulté le 23 novembre 2026, avec HyperBD annoncé en version 0.16.2. Les évaluations et décisions de transposition sont celles de FrameForge, pas des recommandations formulées par les auteurs de HyperBD.
