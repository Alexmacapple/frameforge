# Skills tiers — provenance et utilisation

Ces fichiers sont des copies des skills publiés par Matt Pocock dans [mattpocock/skills](https://github.com/mattpocock/skills), licence MIT : [licence amont](https://github.com/mattpocock/skills/blob/main/LICENSE).

## Fichiers importés

| Destination | Source | SHA du blob Git amont au moment de la copie |
| --- | --- | --- |
| `.agents/skills/grill-with-docs/SKILL.md` | `skills/engineering/grill-with-docs/SKILL.md` | `62b9efb6f991d1b229adee7506962f13ced0c499` |
| `.agents/skills/grilling/SKILL.md` | `skills/productivity/grilling/SKILL.md` | `d2f09a18e6a6c65c55f1271ba08dfeaf06f0bed3` |
| `.agents/skills/domain-modeling/SKILL.md` | `skills/engineering/domain-modeling/SKILL.md` | `a4438c6879c517d1a08e2b5fbca049b632688dfe` |
| `.agents/skills/codebase-design/SKILL.md` | `skills/engineering/codebase-design/SKILL.md` | `3f63c8146dd2604b419c929e9876b90c30d410e9` |

Ces valeurs identifient des **blobs**, pas un SHA de commit global. La copie a été réalisée le 23 novembre 2026. Aucun changement intentionnel des contenus.

## Utilisation prévue

- `grill-with-docs` : questionner le cadrage et tenir à jour le glossaire et les décisions d'architecture ; dépend de `grilling` et `domain-modeling`.
- `domain-modeling` : préciser scène, capture, événement, cue, narration, preuve et rendu.
- `codebase-design` : concevoir les interfaces minimales seulement après les essais FF-01 et FF-02.
- `grilling` : primitive de questionnement, non orchestrateur de production.

Ces copies ne prouvent pas que Claude Code ou Codex les découvre et les invoque automatiquement. Vérifier le chargement sur chaque hôte ; le skill `grill-with-docs` appelle un outil Skill, dont la disponibilité dépend de l'hôte. Ne pas installer simultanément une copie locale et un plugin contenant les mêmes skills sans dédoublonnage.

Le projet conserve sa licence MIT. Les notices de droits amont restent applicables aux fichiers copiés. Aucun des skills n'autorise une publication automatique ou une modification hors du périmètre demandé.
