# FF-10 — Essai adversarial de protection d'un sous-titre

Date : 23 novembre 2026. Protocole figé avant exécution : PROTOCOL.md, commit e9312e4.

## Hypothèse et témoin

Référence : sous-titre 2 du film FF-12 dont l'utilisateur avait confirmé l'affichage et la synchronisation dans QuickTime. Il s'agit d'un **témoin évalué positivement**, pas d'un verrou formel existant dans FrameForge. Le sous-titre 1 peut être reformaté, mais les mots et timecodes doivent rester inchangés.

## Exécution

Un contrôle Python **temporaire et externe au produit** compare les blocs SRT normalisés en fins de ligne. Il vérifie la présence de deux blocs, l'identité exacte du bloc 2 (numéro, timecodes, texte et retours à la ligne), et l'identité des mots et timecodes du bloc 1 hors retours à la ligne. En cas d'acceptation seulement, FFmpeg remuxe la vidéo et l'audio existants avec le nouveau SRT.

- **Scénario autorisé :** modification du retour à la ligne du bloc 1 uniquement. Contrôle accepté ; MP4 local produit.
- **Scénario adversarial :** même modification du bloc 1 plus remplacement non autorisé de « Terre » par « planète » dans le bloc 2. Contrôle rejeté avec motif protected_cue_2_changed ; **aucun MP4 adversarial produit**.
- Le SRT de référence et le MP4 FF-12 source conservent leur SHA-256 avant/après. Résultats structurés dans RESULTS.json.

## Verdict

| Garantie | Résultat |
| --- | --- |
| Rejeter une modification non autorisée du bloc protégé | PASS pour ce cas |
| Accepter une modification autorisée ailleurs | PASS pour ce cas |
| Empêcher la production après rejet | PASS dans ce script conditionnel |
| Préserver référence et média approuvé | PASS par empreintes |
| Verrou humain intégré à FrameForge | **NOT DEMONSTRATED** : contrôle externe |
| Résistance à des modifications hors SRT, à la concurrence ou à un agent contournant le contrôle | NOT TESTED |
| Reprise incrémentale | NOT TESTED |
| Qualité du nouveau MP4 | UNVERIFIED perceptivement |

## Décision

**EXTRACT_ONLY + REUSE_EXISTING.** Le contrôle déterministe de pré-rendu est une méthode réutilisable, sans nouveau moteur. Ne pas présenter cet essai comme un verrou produit ni clôturer FF-10 sur cette seule base. Pour obtenir la garantie réelle, intégrer le contrôle dans le chemin de rendu existant avec un test qui démontre qu'un agent ne peut pas le contourner, sans créer d'orchestrateur ni de nouveau format de projet.

Médias et SRT locaux seulement ; aucune vidéo NASA publiée.
