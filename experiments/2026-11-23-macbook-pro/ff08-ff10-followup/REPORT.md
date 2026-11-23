# FrameForge — FF-08 et FF-10, suite des preuves

Date : 23 novembre 2026. Machine : macbook-pro. Dépôt source : `main` ; référence V5 : `../vertical-v5-kokoro-siwis/media/prototype-v5.mp4`.

## FF-08 : retour humain et recette documentaire

**Retour de l'utilisateur** : la voix Kokoro Siwis convient et les trois résultats sont compris à l'écoute sans image. **PASS utilisateur déclaré** sur ces deux aspects ; pas de test tiers indépendant. Aucun constat de visionnage humain avec image n'a encore été fourni.

**Contrôles automatiques exécutés sur le MP4 V5 exact :**
- SHA-256 `99792213f5706e7764bb970e776de875eb65f35a6d10528f91ff7a9018caebd1`.
- Décodage intégral de **493 images** ; H.264 et AAC ; durée **16,433333 s** : PASS technique.
- Trois blocs SRT identiques aux trois lignes de la transcription : PASS textuel.
- Segments de narration sans chevauchement et entièrement contenus dans le film : PASS temporel structurel.
- Les images échantillonnées ont été inspectées lors de la production V5 ; **ce n'est pas une revue visuelle humaine du film en lecture intégrale**.

**Toujours UNVERIFIED** : synchronisation perçue, fidélité de la parole réelle aux sous-titres, lecture du SRT externe dans le lecteur cible, accessibilité du lecteur VoiceOver, inspection de confidentialité et droits exhaustifs, revue visuelle humaine complète, autorisation de diffusion. **FF-08 reste ouvert / NO-GO diffusion.**

## FF-10 : deux essais ciblés, sans modification de la V5

### A. Interruption simulée après modification d'un sous-titre

Dans un bac à sable temporaire, copier le SRT V5, changer uniquement la phrase de la scène 2, écrire un `checkpoint.json`, arrêter le premier script, puis lancer un second script pour vérifier la reprise. Résultat : **PASS limité** pour la conservation de la scène 1 et de la scène 3, le hash de la voix 1 et l'intégrité des fichiers sources. La nouvelle phrase diverge de la voix 2 : l'essai la marque explicitement comme **invalidation de la concordance parole/SRT et des sous-titres incrustés**, non comme une correction prête à diffuser.

La « validation humaine » utilisée est une **fixture simulée**, pas une approbation réelle. Le test ne prouve ni verrou d'approbation, ni reprise du moteur après crash.

### B. Correction localisée de volume et second rendu complet

Copie de la composition V5 dans `/tmp/frameforge-ff10-render-revision-20261123`, sans toucher à l'original. **Seul** le volume de `voice2` est passé de `1` à `0.9` dans `index.html`. Les trois médias vocaux, la capture, les sous-titres et les autres paramètres sont inchangés.

- HyperFrames 0.8.33 : rendu complet **PASS**, 16,433333 s, MP4 décodable.
- MP4 révisé : `revised-voice2-volume.mp4`, SHA-256 `1877f742be70b552f20db2d08e5446b85bc68a188c54b339fcff53db9acfc095`.
- Comparaison **framemd5** après décodage : **493/493 images vidéo strictement identiques** entre V5 et révision. Cela prouve l'absence de modification visuelle sur cet essai précis, pas la conservation des pistes audio.
- Les fichiers de voix source, dont `voice1.m4a` considéré comme choix à préserver, n'ont pas été modifiés. Le MP4 final a été **entièrement rendu** : pas de preuve de cache ou de recomposition partielle.
- Aucun nouveau contrôle perceptif de la révision audio ; aucune autorisation de diffusion.

**Verdict FF-10 : PARTIAL.** Une révision audio isolée peut être rendue sans changer les 493 images décodées, et une reprise de données sur copie peut conserver les scènes non concernées. **Non démontré** : préservation d'une véritable correction humaine dans le workflow, interruption réelle du rendu, reprise d'étapes et cache, invalidation et réapprobation automatiques.

## Décision

- **Ne pas ajouter d'architecture**. Ces deux essais n'ont pas révélé de besoin démontré de nouveau moteur, cache ou orchestrateur.
- **Ne pas clore FF-08 ni FF-10.** Continuer la revue humaine complète de la V5 et les essais de reprise réalistes.
- **FF-11** (deux rushes hors navigateur) reste le prochain test de généralisation, distinct de la validation de diffusion de la V5.

Les scripts de ce dossier sont des reproductions de tests en bac à sable ; ils utilisent les chemins du poste d'essai et ne constituent pas un outil de production portable.
