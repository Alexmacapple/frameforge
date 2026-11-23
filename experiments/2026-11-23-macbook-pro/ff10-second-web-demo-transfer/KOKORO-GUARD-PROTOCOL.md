# Kokoro FF-10 — Protocole de finalisation gardée

23 novembre 2026. Référence approuvée : form-kokoro-review.mp4, SHA-256 f4552189c24758879f60a87c0a0a369dbd49a8e3a333c683eac0b42057ecefad.

Objectif limité : conserver le garde V2 sur le rendu des images et des entrées, puis effectuer dans un espace temporaire un remplacement de piste audio par la piste Kokoro déjà approuvée. L'empreinte de cette piste doit être figée. La sortie finale ne peut être déposée que si elle a exactement l'empreinte du film approuvé, et si son flux vidéo est identique au rendu gardé. Les échecs doivent laisser le nom final absent. Tester la piste audio modifiée et le cas nominal.

Cette stratégie réutilise un rendu gardé avec la voix Thomas comme intermédiaire : ce n'est PAS une synthèse Kokoro native dans HyperFrames. Le modèle Kokoro n'est pas relancé et aucune nouvelle interprétation vocale n'est acceptée implicitement.
