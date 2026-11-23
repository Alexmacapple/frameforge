# FF-10 — Test de non-régression sur une correction approuvée (FF-12)

23 novembre 2026. Protocole figé AVANT toute modification.

## Hypothèse

Le retour utilisateur sur FF-12 confirme que les sous-titres français s'affichent et correspondent à la narration dans QuickTime. Nous utilisons le **sous-titre 2** comme témoin humain positivement évalué. Cette validation ne signifie pas que l'utilisateur a approuvé chaque caractère ni qu'il a verrouillé le plan.

Modifier **uniquement la mise en ligne du sous-titre 1** dans une copie de FF-12, interrompre un premier remux, relancer intégralement et vérifier :
- sous-titre 2 : texte, timecodes et ordre des lignes **strictement identiques** dans les sources ;
- vidéo et audio : flux copiés sans réencodage ; SHA-256 des flux élémentaires inchangés ;
- sous-titre 1 : même texte lu sans retour à la ligne, présentation modifiée ;
- MP4 final décodable et sous-titres extractibles ;
- aucun changement de la source FF-12 ni publication des médias.

## Verdicts séparés

PASS technique possible sur préservation des octets, correction localisée et relance après interruption. Ce test ne prouve **pas** la reprise incrémentale, ni la protection contre un agent qui écraserait volontairement la correction, ni une validation humaine du nouvel habillage. Si le premier remux est trop rapide pour une interruption vérifiable, déclarer NOT TESTED pour l'interruption.

Aucun nouveau cache, moteur ni orchestrateur.
