# FF-10 — Contre-exemples interruption et concurrence

23 novembre 2026. Protocole gelé avant essai : INTERRUPTION-CONCURRENCY-PROTOCOL.md, commit 67a130f. Deux projets de test sont des copies locales de la composition FF-10 ; aucune source approuvée modifiée.

## Résultats

### A. Interruption réelle

Le processus Python guarded_hyperframes.py est lancé avec une commande HyperFrames 0.8.33. Après huit secondes, SIGTERM est envoyé au groupe du processus de contrôle. Retour du contrôleur : -15. **À cet instant**, aucun MP4 final n'est présent, mais des images intermédiaires et un répertoire de travail HyperFrames subsistent.

**Vérification différée décisive :** un processus HyperFrames enfant a continué et a créé le MP4 result.mp4, décodable, SHA-256 07e8dd7d237877a5c80d8210f6c69a2cb1ac1ceb56c139e7da93dae149e20324. Le journal indique 485 images et un rendu terminé après 25,4 secondes. Une tentative ultérieure de relance par le contrôleur a été refusée avec output_already_exists.

**Verdict : FAIL pour l'arrêt contrôlé et la reprise garantie.** L'absence immédiate de fichier final ne prouve pas l'arrêt du rendu enfant. Le test de relance n'a pas produit un nouveau MP4.

### B. Modification concurrente transitoire

Pendant le rendu d'une autre copie, le texte du sous-titre HTML protégé caption2 est temporairement modifié, puis rétabli avant la fin. Le contrôle de pré-rendu et de fin n'a pas détecté cette altération transitoire. Le rendu a terminé avec code 0 et un MP4 dont le SHA-256 est identique au rendu de référence.

**Verdict : FAIL pour la garantie de détection des mutations transitoires.** L'égalité des empreintes du film est une observation rassurante sur ce cas, mais ne prouve ni l'absence de lecture concurrente ni l'intégrité de tous les rendus possibles.

## Causes probables et limites

- Le processus enfant n'est pas terminé par la stratégie de signalisation actuelle ; les sous-processus ou descendants du lanceur n'ont pas été correctement supervisés. Le contrôle n'a pas garanti la maîtrise du cycle de vie.
- HyperFrames lit les fichiers de projet accessibles en écriture pendant le rendu ; le contrôle SHA-256 avant/après ne constitue pas une isolation transactionnelle.
- Le MP4 n'est pas vérifié contre une version humaine immuable au niveau perceptif.

## Décision

**NE PAS PROMOUVOIR** ce wrapper comme point d'entrée officiel. Corriger de façon minimale : isoler une copie de projet immuable pendant le rendu ; contrôler l'arrêt et l'attente des descendants du moteur ; publier la sortie seulement après vérification complète, dans un emplacement neuf. Rejouer les deux contre-exemples avant tout PASS.

Le prototype FFmpeg protégé et les expériences précédentes ne sont pas invalidés par ces résultats ; la lacune porte sur l'intégration HyperFrames. Aucun média diffusé. FF-10 reste ouvert.
