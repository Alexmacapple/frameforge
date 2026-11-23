# FF-10 — Pré-recette technique et fiche d'écoute de la démonstration V5

23 novembre 2026. Protocole préalable : REVIEW-PROTOCOL.md, commit 4548606. **Verdict : PASS technique, recette humaine UNVERIFIED, diffusion NON AUTORISÉE.**

## Film concerné

- Brouillon local : local/guarded-web-demo.mp4
- SHA-256 : 9fbb7c316fb20ef94a0424f231881b5f0f24d86daf32418aadc1a92e94ae11ad.
- Durée : 16,166667 secondes ; 485 images ; une piste vidéo et une piste audio.
- Vidéo de démonstration web avec trois actions sur une liste de tâches ; le projet d'origine V5 reste inchangé.

## Contrôles automatiques exécutés

- Décodage FFmpeg intégral du MP4 : PASS.
- Trois cues SRT non chevauchants, 2,55–5,37 s ; 6,65–10,52 s ; 11,20–15,695 s : PASS.
- Contenu des cues SRT identique à la transcription texte : PASS.
- Empreinte PCM stéréo 48 kHz de l'audio du nouveau rendu identique à celle de la V5 témoin : PASS. Cela garantit une absence de changement de l'audio décodé entre les deux versions, **pas** la qualité vocale.
- Le rendu nominal et le refus de modifications interdites ont été testés dans REPORT.md.

## Transcription et déroulé attendu

**2,55–5,37 s** : « Une première tâche apparaît dans la liste. »

**6,65–10,52 s** : « Une deuxième tâche apparaît. Les deux tâches sont visibles. »

**11,20–15,695 s** : « La première tâche est cochée et barrée. La deuxième reste à faire. »

Les résultats visuels décrits sont ceux attendus de la composition et de la capture de référence. Cette fiche n'affirme pas qu'un humain a vérifié chaque image du nouveau rendu.

## Questions pour la recette humaine

1. En écoutant le film sans regarder l'image, les trois résultats sont-ils compréhensibles ?
2. La voix Kokoro française est-elle intelligible et les prononciations acceptables ?
3. Les silences, les changements de scène et le rythme sont-ils adaptés ?
4. Les sous-titres sont-ils lisibles à l'écran sans masquer une action essentielle ?
5. Le recadrage de la capture permet-il de voir les gestes et les résultats ?

Pour chaque défaut : préciser le moment, la correction attendue et si le défaut bloque une approbation éditoriale. **Ne pas confondre validation de l'écoute et autorisation de diffusion.**

## Limites

Aucune écoute humaine complète du nouveau MP4 ni recette perceptive des trois scènes n'a été constatée. Aucun contrôle exhaustif de confidentialité, de droits ou de lecteur cible n'a été exécuté ici. La référence de correction est une fixture de test, pas une autorité d'approbation externe. Le chemin npm contrôlé ne protège pas les appels directs à HyperFrames.

**Décision : garder le film DRAFT et FF-10 ouvert.** Ne pas créer une validation humaine fictive, ne pas publier de média.
