# FrameForge — comparaison de voix masculines françaises

Date : 23 novembre 2026. **Expérience locale, sans cloud, sans installation de nouveau moteur.**

## Motif
Retour de revue humaine FF-08 : la voix `Thomas` de la V4 est jugée **trop robotique**. C'est un défaut de qualité éditoriale ; cela ne démontre pas une erreur de prononciation ou de synchronisation.

## Échantillons
Trois voix présentes dans macOS, à débit demandé identique (`say -r 185`), avec exactement le texte de la V4 dans `narration.txt` :

- `thomas.m4a` : Thomas (fr_FR), **témoin** ;
- `jacques.m4a` : Jacques (fr_FR), candidat ;
- `eddy.m4a` : Eddy (Français (France), fr_FR), candidat.

Génération `say -v <voix> -r 185 -f narration.txt -o <fichier.aiff>`, conversion AAC FFmpeg. Les trois pistes sont autonomes ; elles ne remplacent pas les segments de voix ni les timings de la V4.

Durées mesurées : Thomas **9,112 s** ; Jacques **9,198 s** ; Eddy **9,198 s**. La similitude des durées ne prouve pas la naturalité ni l'intelligibilité.

## Protocole d'écoute

Écouter les trois fichiers à volume égal, de préférence dans un ordre masqué, sans regarder le nom du fichier. Évaluer **naturalité**, **prononciation française**, **intelligibilité sans image**, **rythme** et **fatigue d'écoute**. Donner le choix retenu ou indiquer qu'aucune voix ne convient. La V4 actuelle reste le témoin et n'est pas modifiée.

## Décision

**UNVERIFIED — choix de voix en attente de l'écoute humaine.** Aucun échantillon n'est déclaré meilleur sans écoute. Si aucun ne convient, étudier une solution TTS neuronale locale, mais vérifier d'abord les solutions et modèles déjà présents sur la machine. Ne pas installer de moteur ou dépendance sans bénéfice démontré et accord.
