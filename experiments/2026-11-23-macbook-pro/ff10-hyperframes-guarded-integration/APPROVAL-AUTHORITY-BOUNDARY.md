# FF-10 — Autorité d'approbation distincte de l'agent de rendu

23 novembre 2026. SHA de lecture : 0379988. Verdict : **FAIL de la garantie de non-contournement avec l'architecture actuelle ; décision d'autorité requise**.

## Contre-épreuve exécutée

Le script test_approval_authority_boundary.py utilise des copies temporaires des HTML et l'API de contrôle de V3. Trois tests PASS :
1. Empreinte fixe externe au candidat + référence originale : acceptation.
2. Empreinte fixe + référence falsifiée : rejet.
3. Référence falsifiée et empreinte recalculée par le même acteur : acceptation. **Contournement démontré**.

Sur le MacBook Pro, les fichiers de référence et candidats sont détenus par le compte alex. Un simple chmod en lecture seule, un fichier JSON supplémentaire ou un hash dans le dépôt ne constituent pas une frontière de confiance si l'agent a le droit de les modifier, de modifier la commande ou d'invoquer directement HyperFrames.

## Proposition minimale de responsabilités

- **Approbateur humain** : examine une version exacte du média ou du projet, puis autorise explicitement une empreinte et le périmètre protégé. L'approbation doit être conservée dans un système que l'agent de production ne peut pas réécrire.
- **Agent de production** : peut préparer les modifications et exécuter un rendu contrôlé ; ne peut ni créer ni remplacer une approbation.
- **Point d'entrée de production** : lit la référence approuvée depuis une source indépendante et vérifie son intégrité avant de produire. Le point d'entrée doit être effectivement imposé au workflow concerné.
- **Relecteur** : distingue PASS technique, acceptation éditoriale et autorisation de diffusion.

## Options, non implémentées

A. **Validation humaine externe au compte de production**, via un service/compte avec permissions distinctes. Nécessite un mécanisme d'identité et de permissions réellement vérifié ; pas d'installation ou de création de compte décidée ici.

B. **Approbation manuelle hors workflow automatisé** et vérification humaine avant publication. Solution opérationnelle immédiate, mais **pas** un verrou technique empêchant les rendus non approuvés.

C. **Signature de l'approbation** vérifiée par le contrôleur avec clé publique et clé privée inaccessible à l'agent. Intéressante uniquement si l'isolation de la clé, du vérificateur et du chemin de production est démontrée ; sinon sécurité illusoire. Ne pas ajouter de PKI avant besoin.

## Décision

**REUSE_EXISTING + NEEDS_HUMAN_DECISION.** Ne pas multiplier les scripts de hachage ni promouvoir V3. Choisir d'abord où réside l'autorité d'approbation et quels droits possède l'agent de rendu. Dans l'attente : la revue humaine et l'approbation de diffusion restent obligatoires ; FF-10 ouvert. Aucun média publié, aucune configuration de sécurité système modifiée.
