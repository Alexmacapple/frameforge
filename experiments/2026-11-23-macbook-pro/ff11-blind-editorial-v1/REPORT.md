# FF-11 — Pilote sur nouveau corpus NASA, résultat limité

Date : 23 novembre 2026. **Verdict : PASS technique, PARTIAL éditorial, INDEPENDENCE NOT TESTED.**

## Protocole préenregistré

Brief inédit et trois titres NASA fixés dans PROTOCOL.md au commit c6dc76a, avant téléchargement et visionnage. Choix des passages, fondés sur les images de précontrôle, figés dans SELECTION-BEFORE-RENDER.md au commit 9c44356, avant rendu.

- Brief : expliquer une éclipse solaire, puis montrer une observation réelle ; écarter le hors-sujet.
- Retenu : The Moon's Role in a Solar Eclipse, **5–11 s**. Animation de l'alignement Terre–Lune–Soleil et du disque solaire occulté.
- Retenu : An EPIC View of the 2017 Total Solar Eclipse, **2–8 s**. Terre vue de loin avec une zone sombre ; l'identification comme observation de l'éclipse repose aussi sur la provenance NASA, pas sur les seules images.
- Écarté : NASA Calls on Gamers, Citizen Scientists to Help Map World's Coral, sujet corail hors du brief.
- Chaque intervalle retenu a été inspecté sur **six images** à une seconde d'écart. Le corpus était neuf pour ce pilote, mais les titres ont été choisis par le même assistant, et les sources étaient identifiées avant visionnage.

## Exécution et preuves

- NASA Image and Video Library API : sources et SHA-256 dans SOURCE-MANIFEST.json. Les vidéos sont conservées uniquement en local dans local/.
- FFmpeg : extraits normalisés, audio original supprimé volontairement faute de revue des commentaires et des droits.
- HyperFrames 0.8.33 : montage local local/eclipse-12s-draft.mp4.
- Contrôle FFmpeg : **12,000 s, 360 images, H.264, décodage intégral PASS**.
- **Aucune piste audio** : film muet. Il ne faut pas déclarer que la voix ou les sous-titres ont été validés.
- SHA-256 MP4 : 8e462bc5372cb67776bb75deae9ee0f479205d32072421245b3743670a5b2bfd.
- Images post-rendu échantillonnées aux secondes 2, 5, 7 et 10 dans le dossier local ; aucune revue humaine complète.

## Verdicts

| Critère | Verdict |
| --- | --- |
| Brief fixé avant inspection | PASS, commit c6dc76a |
| Décisions d'intervalles figées avant rendu | PASS, commit 9c44356 |
| Deux plans et exclusion du hors-sujet | PASS structurel |
| Précontrôle des images avant rendu | PASS sur six échantillons par passage |
| Rendu MP4 12 s décodable | PASS |
| Deuxième plan = observation réelle d'éclipse | PARTIAL : provenance NASA, mais preuve visuelle et éditoriale non indépendante |
| Son, narration et sous-titres | NOT DONE : film muet |
| Recette perceptive et accessibilité | UNVERIFIED |
| Droits de diffusion | UNVERIFIED |
| Choix autonome de sources inconnues | NOT DEMONSTRATED |
| Évaluation indépendante des décisions | NOT DONE |

## Décision et prochain test

**REUSE_EXISTING, ne pas ajouter d'architecture.** Le pipeline sait sélectionner des intervalles après précontrôle et assembler deux sources nouvelles. Il ne démontre pas un réalisateur autonome ni une sélection à l'aveugle : l'assistant a contrôlé lui-même ses décisions, et l'échantillonnage n'est pas une preuve de qualité globale.

Pour évaluer l'autonomie, confier le même brief et les trois sources à **un évaluateur réellement distinct**, sans lui transmettre les choix ni les rapports de ce pilote. Demander sa sélection, ses preuves temporelles, son classement des erreurs et son jugement de qualité. Comparer ensuite avec le plan figé ; ne pas confondre cette contre-revue avec la simple relecture du présent rapport. FF-11 reste ouvert.

Les fichiers NASA et le MP4 ne sont pas poussés dans Git.
