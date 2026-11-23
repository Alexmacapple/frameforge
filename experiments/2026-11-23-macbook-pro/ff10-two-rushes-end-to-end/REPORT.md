# FF-10 — Deux rushes, correction protégée, rendu HyperFrames

23 novembre 2026. Protocole gelé avant exécution, commit 929f36c. **Verdict : PASS technique sur fixture ; validation humaine réelle UNVERIFIED.**

## Scénario

Réutilisation de FF-11 : deux mires vidéo expérimentales, rush A silencieux et rush B avec son témoin, composition 9 secondes. La référence de test modifie le libellé B de « son témoin » en « audio témoin » ; cette modification constitue une **correction simulée**, et non une approbation humaine constatée. Le libellé B et la transition sont protégés. Le changement ciblé autorisé porte sur la couleur de fond du libellé A, #101010 vers #222222.

La référence est épinglée par SHA-256 7d1dabfca5304d74929532fdeedc48684705024ce81e17b6d1674b1f2b748890. Ce pin est défini dans le test ; il ne représente pas une autorité humaine indépendante.

## Tests et rendu

- Quatre tests unitaires PASS : modification autorisée, modification du bloc B rejetée, substitution de référence rejetée, présence des deux rushes.
- Le wrapper HyperFrames V2 a été **paramétré**, non dupliqué, pour recevoir un contrôle de pré-rendu et une liste explicite de médias/configuration propres à FF-11.
- HyperFrames 0.8.33 a produit un MP4 local à partir d'une copie isolée des entrées. Décodage FFmpeg intégral sans erreur effectué par le wrapper.
- SHA-256 du MP4 : fbd342181790dfdbe1bb145785ad8598680d4f974344c86c79e0556459235dea.
- ffprobe : voir ffprobe.json.
- Empreintes des deux rushes inchangées : input-hashes.json.

## Limites et décision

**PASS** pour le contrôle technique ciblé sur deux rushes et un rendu HyperFrames réel.

**UNVERIFIED** pour une correction réellement formulée et approuvée par un humain, pour la recette perceptive du nouveau film et pour le caractère obligatoire du chemin contrôlé dans FrameForge.

Le test ne constitue pas un film narratif prêt à diffuser. Ne pas clore FF-10 sur cette seule preuve. Conserver le wrapper comme expérimentation, sans ajout d'orchestrateur ou de moteur. Aucun média publié.
