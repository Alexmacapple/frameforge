# FrameForge — instrumentation DOM non intrusive, même prise

23 novembre 2026, MacBook Pro Apple M2 Max, agent-browser 0.31.1, TodoMVC React public avec données fictives.

## Protocole

Démarrer `agent-browser record start`, puis installer dans la page un `MutationObserver` qui mémorise chaque état des tâches avec `performance.now()` relatif à l'installation de l'observateur. Exécuter trois actions et vérifier leur résultat avec les commandes `agent-browser eval`. Récupérer le journal DOM **avant** `record stop`. Aucun bandeau de couleur n'est injecté : il s'agit d'une **prise propre**.

## Résultats

- WebM VP8 de **4,7 s**, 47 images natives à 10 images/s, 89049 octets.
- États DOM journalisés à environ **0,983 s**, **2,859 s**, **4,734 s** après installation de l'observateur : une tâche, deux tâches, puis première tâche terminée.
- Trois assertions DOM positives également renvoyées par les commandes agent-browser.
- Différences d'images dominantes approximatives : **0,7 s**, **1,8 s**, **3,3 s** et **4,5 s**. La première et la dernière variation ne sont pas qualifiées indépendamment. Les différences ne prouvent pas seules la cause du changement.

## Limite déterminante

La dernière observation DOM est datée **4,734 s après l'installation de l'observateur**, tandis que la durée totale du WebM est **4,7 s**. Les origines et cadences des horloges sont différentes. Il serait donc **incorrect** d'utiliser directement les valeurs `performance.now()` comme temps vidéo. Une correction d'offset unique n'a pas été démontrée.

La prise propre établit le succès métier mais **pas** une synchronisation action-image à 100 ms. Le fait qu'un résultat soit visible dans les images et observé dans le DOM ne garantit pas une correspondance temporelle exacte.

## Décision

**PASS** pour la collecte non intrusive d'états DOM et pour la capture propre. **UNVERIFIED** pour la conversion de ces temps en repères vidéo exacts. **NO-GO** pour valider FF-06 et FF-08 ou annoncer une V4 parfaitement synchronisée.

La prochaine expérience discriminante doit obtenir les timestamps des frames depuis le mécanisme de capture lui-même (ou un protocole d'étalonnage vérifié dans la même prise) et comparer l'horloge DOM à celle du média. Si cette capacité n'existe pas nativement, envisager un petit adaptateur de preuve avec test de non-régression, **pas** un skill ni un nouvel orchestrateur. Éviter de répéter des prises qui ne peuvent pas résoudre cette question.
