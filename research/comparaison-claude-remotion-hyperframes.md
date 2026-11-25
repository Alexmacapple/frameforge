# Animations graphiques avec Claude : comparaison Claude seul, Remotion, HyperFrames

**Date :** 25 novembre 2026  
**Statut :** note de source externe, transcrite et restructurée. Rien n'a été reproduit ni mesuré par FrameForge.  
**Source :** vidéo YouTube « La meilleure façon de créer des animations graphiques avec Claude AI », <https://www.youtube.com/watch?v=HfOZNVyXbM0>, d'après un résumé fourni par Alex, non revu face à la vidéo.  
**Outils comparés :** Claude seul, [Remotion](https://github.com/remotion-dev/remotion), [HyperFrames](https://github.com/heygen-com/hyperframes).  
**Usage prévu :** matière à exploiter plus tard (voir la section 8).

## 1. Objet du test

L'auteur passe la même requête à trois approches pour créer une animation de motion design générée par IA. Il compare les résultats, le temps de génération et la qualité.

- **Contexte :** depuis la sortie d'Opus 5.5, des animations de motion design circulent sur X ; elles auraient été générées en 15 minutes avec un seul prompt.
- **Principe :** Claude ne génère pas de vidéo. Il écrit le code de chaque image, puis rend les images à la suite pour assembler la vidéo.
- **Cible :** une animation de 15 secondes pour Hammy, application de cyclisme en intérieur (<https://hammycycling.app/>).
- **Conditions égales :** les trois méthodes reçoivent les mêmes ressources (site web, logo officiel, maquettes de l'interface) et le même prompt.

## 2. Le prompt

- Élaboré avec l'aide de ChatGPT. Version anglaise : <https://pastebin.com/WsyMad79>. Version française en annexe.
- Il fixe la vision, les références, les ressources disponibles et la structure de l'animation.
- **Contrainte créative majeure :** un seul plan continu, sans coupe, où chaque forme naît par morphing d'une forme existante (par exemple une lettre qui devient le cercle du graphique suivant). « Rien n'apparaît. Tout se transforme. »

## 3. Méthode 1 : Claude seul

- **Mise en œuvre :** directement dans le terminal, modèle Opus 5.5, effort maximal.
- **Ce que fait l'agent :** il lit les ressources, analyse le site et l'artefact de design, puis installe lui-même les dépendances nécessaires (FFmpeg) pour le son et l'image.
- **Durée :** 35 minutes sans interruption.
- **Livrables :** deux MP4 (avec et sans son) et une explication du concept.
- **Analyse visuelle :**
  - tout part d'un seul point crème, rien n'apparaît en fondu ;
  - la roue se transforme de façon très fluide en profil d'entraînement ;
  - « 2 riders, 1 subscription » est représenté visuellement de façon efficace ;
  - les profils, lignes et cercles fusionnent élégamment dans les éléments du logo.
- **Verdict intermédiaire :** impressionnant, digne d'une publication sur X.

## 4. Méthode 2 : Remotion

- **Mise en œuvre :** framework open source Remotion. Commande d'installation copiée depuis le dépôt GitHub officiel, modèle vierge (« blank »), installation des skills, puis consigne à Claude d'utiliser Remotion pour le rendu, avec le même prompt.
- **Durée :** 23 à 24 minutes, environ 10 minutes de moins que Claude seul.
- **Livrables :** un seul MP4, sans son, avec un tableau explicatif.
- **Analyse visuelle :**
  - départ semblable : fond et point blanc ;
  - le profil s'ouvre, une ligne devient l'indicateur de FTP (puissance) et s'élève ;
  - la ligne produit un autre point et se transforme pour revenir au logo ;
  - « 2 riders, 1 subscription » est écrit en texte au lieu d'être montré.
- **Verdict intermédiaire :** propre et de bonne qualité, mais sans son.

## 5. Méthode 3 : HyperFrames

- **Mise en œuvre :** installation d'un plugin pour Claude, nouvelle session, commande `/hyperframes` avec le même prompt.
- **Durée :** 30 minutes.
- **Livrable :** brouillon à 30 images par seconde, 15,5 secondes, visible sur un serveur local.
- **Analyse visuelle :**
  - concept annoncé : un hamster dans une roue, à partir d'un point jaune ;
  - réalisé : pas de hamster, mais une roue qui s'ouvre sur le profil, un graphique à barres pour la FTP, et deux cercles avec des lettres pour les deux cyclistes ;
  - animation fluide, avec un léger tremblement et un clignement au passage vers l'icône.
- **Verdict intermédiaire :** bon résultat technique, mais le choix créatif des deux cercles à lettres est le moins convaincant des trois.

### Retouche demandée à HyperFrames

- **Demandes :** supprimer le saut (« téléportation ») de l'indicateur circulaire au changement de hauteur ; mieux montrer les deux cyclistes que par des cercles à lettres.
- **Durée :** 8 minutes.
- **Résultat :** l'indicateur ne saute plus ; les cyclistes deviennent deux petites roues qui rebondissent ; un sound design est ajouté. Nettement mieux, mais la représentation des cyclistes reste perfectible sans consigne plus précise.

## 6. Verdict de la vidéo

- **Préférence de l'auteur :** Claude seul, malgré sa durée plus longue.
- **Qualité :** les trois résultats sont de très bonne qualité et publiables sur X à côté des animations virales.
- **Explication avancée :** la proximité des résultats vient du même modèle de base, Opus 5.5 en effort maximal, dans les trois cas.
- **Apport des frameworks :** les garde-fous de Remotion ou HyperFrames accélèrent un peu la génération, et les deux offrent un éditeur web, ce qui peut compter selon le projet. L'écart de qualité finale est minime.

## 7. Recommandation de la note d'origine

Cette partie suivait le résumé dans le texte fourni. Elle ne vient pas de la vidéo et la contredit sur le choix final : la vidéo préfère Claude seul, la note retient HyperFrames.

- **Remotion :** premier jet le plus rapide ; animation simple, sans retouche fine ni son ajouté après coup ; résultat sûr et propre, un peu moins créatif.
- **HyperFrames :** travail par itérations (base, puis corrections précises en quelques minutes) ; intégration dans l'environnement de code par le plugin et `/hyperframes` ; sound design produit sur simple demande.
- **Verdict de la note :** pour un usage régulier et professionnel, HyperFrames offrirait le meilleur équilibre ; son premier jet est un peu plus long, mais il intègre vite et bien les corrections.

## 8. Pour l'exploitation dans FrameForge

Points à garder en tête plus tard. Ce ne sont pas des conclusions.

- **Une seule observation :** un test, une requête, un juge (l'auteur), sur un autre type de film. Les durées ne sont ni répétées ni comparées sur la même machine.
- **Un autre type de film :** une publicité abstraite et générée, sans capture d'une action réelle. FrameForge produit des films dont chaque scène est observée et vérifiée. La contrainte « Rien n'apparaît. Tout se transforme. » y vaut pour l'habillage, pas pour la preuve.
- **Ce qui recoupe le ticket 56 :** la vitesse de retouche et le son ajouté à la demande concernent le flux de skills d'HyperFrames, que la contre-revue de #56 n'adopte pas. Le moteur seul est déjà utilisé.
- **Pistes réutilisables :** la retouche ciblée et chronométrée (8 minutes) comme mesure de la reprise ; un brief qui donne les références de marque et demande de signaler une ressource inaccessible plutôt que de l'inventer.
- **À vérifier avant tout usage :** les versions des outils utilisées dans la vidéo, la licence de Remotion pour un usage professionnel, et si le plugin HyperFrames active la télémétrie (coupée sur le MacBook Pro le 25 novembre 2026).

## 9. Écarts relevés dans le texte fourni

- Le plan de la vidéo nomme l'application « HEMI », le prompt « Hammy » ; le site cité est hammycycling.app. Retenu ici : Hammy.
- Le texte fourni contenait deux paragraphes de notes de traduction en anglais au milieu du prompt, et une fin de prompt en double : retirés.
- La conclusion de la vidéo (inviter à comparer les versions, commenter, s'abonner) n'est pas reprise.
- Chemin des logos dans le prompt : `/Volumes/Data/my-apps/Hammy/01-Brand/Logo/Current`, propre au poste de l'auteur de la vidéo.

## Annexe : prompt en français

Texte du prompt tel que fourni, sans les notes de traduction ni la fin dupliquée. La phrase publicitaire reste en anglais, comme elle doit apparaître à l'écran.

### Hammy — Publicité premium en motion design à morphing continu

Créez une publicité en motion design extraordinaire et visuellement saisissante pour Hammy, optimisée pour X (Twitter).

- Site web : <https://hammycycling.app/>
- Référence de l'interface de l'application : Hammy Screens v1 — Claude Design Artifact
- Logos officiels : `/Volumes/Data/my-apps/Hammy/01-Brand/Logo/Current`

#### Vision créative

Créez un chef-d'œuvre de motion design époustouflant d'environ 15 secondes, qui fasse preuve d'une vision créative, d'une maîtrise technique et d'une sophistication artistique exceptionnelles.

Abordez ce projet comme un motion designer de tout premier plan qui réalise la pièce maîtresse de son portfolio.

L'objectif n'est pas seulement de faire la publicité d'une application mobile. Il s'agit de créer une expérience visuelle inoubliable qui fasse penser au spectateur : « La personne qui a fait ça est un motion designer incroyable. »

Chaque mouvement doit témoigner d'intention, de précision, de créativité et d'un goût irréprochable.

L'ensemble de la publicité doit former une seule expérience visuelle continue et ininterrompue, où chaque forme évolue naturellement en une autre forme.

Rien n'apparaît. Tout se transforme.

Prenez la pleine maîtrise créative du concept, de la narration visuelle, de la chorégraphie, du rythme et des transitions. Ne suivez ni une structure de scènes rigide ni une séquence prédéterminée.

#### Documents de référence

Avant de développer l'animation, étudiez en profondeur les références disponibles.

**Site web.** Analysez le site pour comprendre la raison d'être de Hammy, sa proposition de valeur, ses fonctionnalités clés, son public cible, la personnalité de sa marque, sa typographie, ses couleurs et son langage visuel. Utilisez le site comme source principale pour comprendre ce qu'est Hammy, ce qu'il propose et quel message doit être transmis. La publicité doit transmettre clairement l'essence du produit, et pas seulement montrer du mouvement abstrait.

**Hammy Screens v1 — Claude Design Artifact.** Trouvez et examinez l'artefact Claude Design nommé Hammy Screens v1. Utilisez cet artefact avant tout comme une référence pour comprendre le produit, et non comme une obligation de reproduire ou de montrer directement ces écrans précis. Étudiez les écrans pour comprendre :

- ce que fait l'application ;
- les types de fonctionnalités et d'interactions qu'elle comporte ;
- l'expérience produit dans son ensemble ;
- le ton et la structure de l'interface ;
- la logique visuelle de l'application.

Cet artefact a pour but de vous aider à comprendre le produit assez profondément pour créer un motion design plus intelligent et plus porteur de sens. Vous n'avez pas besoin de montrer littéralement les écrans fournis ni de construire la publicité autour de reproductions directes d'écrans. Vous pouvez abstraire, réinterpréter, styliser ou évoquer sélectivement l'expérience de l'application, tant que la publicité reste fidèle à ce qu'est réellement Hammy.

**Logos officiels.** Accédez aux logos officiels de Hammy à l'emplacement indiqué plus haut. Examinez les fichiers disponibles et utilisez le bon logo officiel. Préservez sa géométrie, ses proportions, ses couleurs et son identité. Explorez comment les caractéristiques visuelles du logo peuvent inspirer le langage de mouvement de toute la publicité.

Si une référence est inaccessible, signalez la limite plutôt que d'en inventer le contenu.

#### Le principe fondamental du mouvement

UN SEUL PLAN CONTINU. AUCUNE COUPE. CHAQUE FORME A UNE ORIGINE.

Chaque élément doit naître d'une transformation visible de quelque chose qui existe déjà.

Explorez des techniques sophistiquées, notamment :

- le morphing complexe de tracés vectoriels ;
- l'interpolation de formes géométriques ;
- les transformations topologiques sans rupture ;
- la division, la fusion et la recombinaison de formes ;
- l'étirement et la déformation fluides ;
- le masquage avancé et les transformations d'espace négatif ;
- les transformations spatiales continues ;
- la typographie cinétique précise ;
- les transitions astucieuses par correspondance de formes (match-shape) ;
- des métamorphoses inattendues mais visuellement logiques.

Ces techniques ne doivent pas ressembler à une liste à cocher. Combinez-les de manière inventive en un langage de mouvement unifié.

Les transformations doivent être si bien conçues que le spectateur soit surpris par ce que devient une forme, tout en restant capable de suivre son évolution.

Évitez les transitions évidentes et répétitives. Cherchez des liens visuels inventifs qui démontrent une compétence exceptionnelle en motion design.

#### L'excellence en motion design

Traitez chaque image comme une occasion de démontrer votre maîtrise du motion design. Poussez la créativité et le savoir-faire bien au-delà d'une publicité d'application conventionnelle. Concentrez-vous sur :

- **Des transformations ingénieuses.** Trouvez des relations astucieuses et inattendues entre des éléments apparemment sans lien. Transformez une forme reconnaissable en quelque chose de surprenant, puis résolvez-la sans rupture en une autre forme visuelle porteuse de sens.
- **Des courbes d'animation exceptionnelles.** Utilisez un easing parfaitement maîtrisé, des accélérations et décélérations intentionnelles, un dépassement (overshoot) élégant, une anticipation subtile et une stabilisation précise. Le mouvement doit paraître physiquement convaincant sans être contraint par le réalisme.
- **Une chorégraphie visuelle parfaite.** Coordonnez plusieurs éléments avec un timing, un rythme, une hiérarchie et des relations spatiales sophistiqués. Même les transformations complexes doivent paraître naturelles et minutieusement orchestrées.
- **Un usage créatif de la géométrie.** Expérimentez avec l'espace négatif, la continuité des formes, les illusions visuelles, les transformations dimensionnelles et des relations géométriques inventives.
- **Une composition remarquable.** Utilisez délibérément le format 16:9. Explorez de belles dispositions, des relations spatiales dynamiques, une hiérarchie visuelle forte et des mouvements de caméra maîtrisés.
- **Une retenue raffinée.** Montrez votre sophistication par la précision, et non par l'ajout d'effets visuels superflus. Chaque animation doit servir un but. Rien ne doit paraître arbitraire, décoratif pour le simple plaisir ou généré mécaniquement.

Le résultat final doit donner l'impression d'une direction artistique image par image.

#### Narration visuelle

Construisez la publicité autour de ce qu'est réellement Hammy. Le motion design ne doit pas seulement être impressionnant : il doit aussi communiquer clairement le produit.

Utilisez le site web et l'artefact de design pour comprendre l'application suffisamment bien et représenter sa raison d'être de façon visuellement captivante. La publicité doit faire comprendre que Hammy est un vrai produit doté d'une proposition de valeur précise.

Au minimum, l'animation doit aussi inclure ou évoquer clairement le message :

« 2 riders, 1 subscription. »

Cette phrase doit être traitée comme un élément important de l'histoire du produit et intégrée avec élégance au motion design.

La publicité doit transmettre l'identité, la raison d'être et l'attrait de Hammy, tout en donnant la priorité à l'originalité et au savoir-faire du mouvement.

Vous n'avez pas à imposer des démonstrations littérales d'écrans de l'application si une approche visuelle plus forte sur le plan conceptuel communique mieux le produit.

Utilisez la typographie, les éléments de marque, un langage d'interface abstrait, des signes liés au cyclisme, la logique du produit et les transformations pour exprimer ce qu'est l'application et pourquoi elle compte.

Privilégiez la clarté et la mémorisation plutôt que de chercher à montrer trop de fonctionnalités.

Maintenez du début à la fin une typographie, des espacements, des alignements et un équilibre visuel remarquables.

#### Liberté créative

Vous disposez d'une totale liberté créative sur le concept visuel, la structure narrative, la composition, les techniques de transformation, les mouvements de caméra, la typographie et le rythme.

Ne découpez pas la vidéo en scènes imposées ni en intervalles de temps fixes. Développez plutôt un concept visuel original et laissez l'animation se dérouler de façon organique.

La durée d'environ 15 secondes est une contrainte créative, pas une chronologie imposée. Faites compter chaque seconde. Privilégiez quelques transformations extraordinaires plutôt que de nombreuses transformations ordinaires.

La publicité doit paraître dynamique et rigoureusement chorégraphiée, sans mouvement inutile, pause superflue ni séquence répétitive.

Mettez-vous au défi de créer des transitions qu'un motion designer très expérimenté trouverait impressionnantes.

#### Spécifications techniques

- Plateforme : X (Twitter)
- Format d'image : 16:9 (paysage)
- Résolution : 1920 × 1080
- Durée visée : environ 15 secondes
- Fréquence d'images : 60 i/s de préférence
- Format : une seule animation continue et ininterrompue
- Son : sound design premium facultatif, synchronisé avec les transformations
- Visionnage sans son : entièrement compréhensible sans audio

Concevez spécifiquement pour le format panoramique tout en préservant la lisibilité sur mobile.

#### Contraintes absolues

- Aucune coupe, aucun jump cut, aucune scène déconnectée.
- Chaque nouvelle forme doit visiblement évoluer à partir d'une forme existante.
- Aucune apparition ni disparition arbitraire d'objet.
- Aucun fondu enchaîné déguisé en morphing de forme.
- Aucune réinitialisation de caméra ni changement brutal de composition.
- Utiliser le logo officiel de Hammy.
- Rester fidèle au produit réel et à l'identité de marque.
- Ne pas inventer d'affirmations non fondées.
- Ne pas recourir à des templates génériques de motion design ni à des transitions prévisibles.
- Aucun effet excessif qui détourne l'attention de la qualité de l'animation.
- Ne pas sacrifier la continuité visuelle ni la lisibilité au profit de la complexité.
- Ne pas traiter l'artefact de design comme un storyboard obligatoire écran par écran : l'utiliser pour comprendre l'application, pas pour limiter le concept.

#### Défi créatif final

Imaginez que cette publicité sera jugée par certains des meilleurs motion designers du monde. Ils évalueront son originalité, ses principes d'animation, son ingéniosité géométrique, sa composition, son rythme, sa narration visuelle et son exécution technique.

Créez quelque chose qui les impressionne vraiment. Faites en sorte que chaque transformation paraisse à la fois surprenante et inévitable. Faites en sorte que chaque courbe, chaque mouvement et chaque transition paraissent délibérément façonnés.

Construisez une publicité convaincante sur le plan marketing, mais remarquable en tant que motion design. Elle doit communiquer clairement ce qu'est Hammy, intégrer avec élégance « 2 riders, 1 subscription » et donner malgré tout l'impression d'un chef-d'œuvre de portfolio de 15 secondes signé par un motion designer exceptionnel.

Par-dessus tout :

Rien n'apparaît. Tout se transforme.
