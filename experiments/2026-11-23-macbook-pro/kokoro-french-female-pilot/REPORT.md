# FrameForge — pilote Kokoro voix française féminine

Date : 23 novembre 2026.

## Objet
Tester une alternative locale aux voix masculines macOS jugées trop synthétiques, avec accent inadapté et débit insatisfaisant. L'utilisateur accepte une voix féminine.

## Exécution
- Environnement **isolé** : `/tmp/frameforge-kokoro-pilot-20261123/.venv`, Python 3.12, installation `uv pip install kokoro soundfile`. **Aucune dépendance ajoutée au projet FrameForge**.
- Modèle téléchargé : `hexgrad/Kokoro-82M` via Hugging Face, voix `ff_siwis`, pipeline français `lang_code='f'`, vitesse `1.0`.
- Texte identique à la narration V4 ; échantillon autonome, **pas de nouvelle V5**.
- Sortie : `siwis.m4a` (AAC), durée source WAV **9,85 s**.
- Le modèle a été téléchargé depuis un service externe ; **la génération et la synthèse du texte ont été exécutées localement**. Aucun appel à une API de synthèse vocale distante.
- Code de génération archivé dans `generate.py`. Les poids du modèle restent dans le cache local et ne sont pas copiés dans Git.

## Vérifications et limites
- **PASS technique** : le modèle a produit une piste audio décodable.
- **UNVERIFIED** : naturalité, accent, rythme, intelligibilité, prononciation, comparaison à l'écoute et adéquation au film.
- Le texte de V4 est traité comme un seul segment ; des pauses éditoriales explicites pourront être étudiées après le retour d'écoute.
- **Aucune validation de voix ni modification de V4**. Ne pas intégrer Kokoro au pipeline avant une décision humaine.
