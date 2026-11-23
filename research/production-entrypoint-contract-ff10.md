# FrameForge — Contrat minimal de production contrôlée (proposition)

Date : 23 novembre 2026. SHA examiné : fb2edcd. **SPEC PROPOSAL — non implémentée.**

## État observé

- SPEC.md décrit render-adapter et qa comme frontières conceptuelles.
- Les expériences vertical-v5-kokoro, ff11-two-rushes-no-browser et ff10-targeted-resume utilisent npx --yes hyperframes@0.8.33 render dans leur script npm render. Les fichiers hyperframes.json ont une structure similaire, sans preuve d'interchangeabilité.
- ff10-lock-guard-pilot/guarded_export.py assure un remux MP4/SRT local protégé, pas un contrôle des rendus HyperFrames.
- L'interruption et la relance ont été testées pour ce remux ; pas de checkpoint.

## Contrat proposé

1. Identifier le projet, la commande de rendu existante et ses versions/paramètres.
2. Fixer les empreintes des médias d'entrée et la provenance.
3. Référencer les éléments approuvés et la version précise approuvée, indépendamment des candidats modifiables.
4. Définir explicitement le périmètre du changement autorisé et les éléments protégés.
5. Avant le rendu, refuser les altérations hors périmètre, les références manquantes et les entrées incompatibles avec l'approbation.
6. Rendre avec HyperFrames existant ; réserver FFmpeg aux contrôles et opérations de remux déjà démontrées.
7. Après le rendu, décoder le média, extraire les pistes, vérifier les contenus et comparer les éléments protégés. La recette perceptive humaine reste distincte du décodage technique.
8. Ne jamais écraser silencieusement un média approuvé. Après interruption, relancer intégralement avec les mêmes entrées contrôlées, sans revendiquer de checkpoint.
9. Conserver des statuts séparés : preuve technique, validation éditoriale, autorisation de diffusion.

## Test discriminant minimal

Sur un projet HyperFrames existant, modifier un élément non protégé tout en conservant une correction humaine approuvée. Le cas autorisé doit produire le changement demandé et préserver la correction ; le cas adversarial doit être bloqué avant le rendu. Interrompre puis relancer, contrôler le MP4 final et documenter les chemins qui peuvent contourner le contrôle.

## Décisions

- REUSE_EXISTING : HyperFrames, FFmpeg, contrôles déterministes, rapports.
- EXPERIMENT : une intégration sur un projet HyperFrames réel, avant toute généralisation.
- BUILD_MINIMAL conditionnel : extraire un précontrôle partagé seulement si le manque est démontré.
- REJECT : nouveau moteur temporel, orchestrateur, cache général ou schéma obligatoire prématuré.

## Conditions de clôture

| Garantie | PASS requis |
| --- | --- |
| Changement autorisé | Modification attendue et éléments protégés inchangés |
| Changement adversarial | Rejet avant rendu sur le chemin nominal |
| Relance | Aucune sortie partielle présentée comme finale ; nouveau rendu contrôlé |
| Produit final | Pistes et contenu vérifiés, recette humaine distincte |
| Non-contournement | Le chemin de production ciblé invoque effectivement le contrôle |

**FF-10 reste ouvert.** Le présent contrat est une proposition documentaire, non une intégration ni une preuve de protection générale. Aucun média NASA publié.
