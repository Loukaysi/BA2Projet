## Semaine 1 : 
Pas de question, il s'agit du début du projet.


## Semaine 2 :
Pas de question, il s'agit du début du projet.


## Semaine 3 :

### "Comment avez-vous conçu la lecture du fichier ? Comment l’avez-vous structurée de sorte à pouvoir la tester de manière efficace ?"
Pour tester la lecture de fichier, nous avons commencé par simplement afficher tous les caractères présent dans ce dernier puis il a fallu diviser l'analyse de ce dernier en 2 parties : Les paramètres puis la carte en elle-même. Pour simplifier l'utilisation de ce dernier, la lecture s'effectue une seule fois puis les données sont sotckées dans des listes adaptées.

### "Comment avez-vous adapté vos tests existants au fait que la carte ne soit plus la même qu’au départ ? Est-ce que vos tests résisteront à d’autres changements dans le futur ? Si oui, pourquoi ? Si non, que pensez-vous faire plus tard ?"
Nous avons choisit de créé une liste de string dans chaque fichier test qui copie le format des "map.txt" et crée un fichier temporaire pour être lu normalement. Ainsi nos tests sont indépendants des modifications des maps du jeu, donc ils résisteront à d’autres changements dans le futur.

### "Le code qui gère la lave ressemble-t-il plus à celui de l’herbe, des pièces, ou des blobs ? Expliquez votre réponse."
Il ressemble plus au code des pièces car on cherche une collision entre le joueur et la lave.

### "Comment détectez-vous les conditions dans lesquelles les blobs doivent changer de direction ?"
Pour les collisions avec les murs, on utilise la même méthode que pour les collisions entre les pièces et le joueur. Pour savoir s'il existe du sol là où le blob veut avancer, on crée un "sprite temporaire" et on regarde s'il est en collisions avec du sol au pied du blob.


## Semaine 4 :

### Quelles formules utilisez-vous exactement pour l’épée ? Comment passez-vous des coordonnées écran aux coordonnées monde ?
Si on considère, la position absolue du joueur P, la position absolue du centre de l'écran C, les dimensions de l'écran h et w, et la position relative du clic S, On calcule d'abord le clic relativement au joueur V := S + C - P - (w/2,h/2) et on utilise alors la fonction atan2 de la librairie math sur les coordonnées Vx et Vy.
Pour l'affichage, on décale en plus un peu l'épée mais ces alignements sont "à l'oeil" alors il n'y a pas de formules formelles.

### Comment testez-vous l’épée ? Comment testez-vous que son orientation est importante pour déterminer si elle touche un monstre ?

*A remplir après le test de l'épée*

### Comment transférez-vous le score de la joueuse d’un niveau à l’autre ?
Il s'agit d'un atribut de Gameview qui n'est pas remis à 0 quand on utilise la méthode pour charger la carte.

### Où le remettez-vous à zéro ? Avez-vous du code dupliqué entre les cas où la joueuse perd parce qu’elle a touché un ou monstre ou de la lave ?
Cela se fait dans la fonction Setup, donc il n'y a pas de duplication de code.

### Comment modélisez-vous la “next-map” ? Où la stockez-vous, et comment la traitez-vous quand la joueuse atteint le point E ?
Nous avons créé une classe "Map" qui se charge de la lecture des fichiers, notamment, de sauvegarder les paramètres de cette dernière donc nous pouvons aller chercher cette information dans cette liste. De fait, il nous suffit de rappeler la méthode qui lit le fichier "suivant" pour charger une nouvelle carte.

### Que se passe-t-il si la joueuse atteint le E mais la carte n’a pas de next-map ?
Pour l'instant, la joueuse est déplacée vers la droite de quelques pixels mais, à long temre, ceci peut-être changé sans problèmes car c'est une situation que nous détectons.


## Semaine 5 :

### Quelles formules utilisez-vous exactement pour l’arc et les flèches ?
Pour l'arc, la formule est la même que pour l'épée, elle est orientée en direction de la souris et décalée à l'oeuil.
Pour la flèche, elle commence à une vitesse définie d'avance, dans la direction de la souris. A chaque tic, la gravité décrémente d'une valeure constante la vitesse verticale la flèche (comme pour la joueuse) et sa position est mise à jour.

### Quelles formules utilisez-vous exactement pour le déplacement des chauves-souris (champ d’action, changements de direction, etc.) ?
Nous définisons un champ d'action circulaire, centré sur la position initiale de la chauve-souris.
Dans cette zone intérieure, la chauve souris se déplace à vitesse constante, elle change de direction aléatoirement (entre -5 et 5 degré) à chaque tic avec une faible variation entre son orientation actuelle et la nouvelle.
Quant elle sort de la zone intérieure, sa direction change à chaque tic toujours dans le même sens (de +3 degré ou +6 degré selon si elle s'éloigne ou se raproche du champ d'action) ce qui la fait rapidement revenir dans la zone. Ainsi, la réelle zone du champ d’action est légèrment plus grande (mais clairement définie par les constante choisies) que celle définie au début.
Le sprite chauve souris ne tourne pas avec la direction de son mouvement, mais il change aléatoirment (entre +10 et -10 degré) par rapport à l'orientation d'origine.

### Comment avez-vous structuré votre programme pour que les flèches puissent poursuivre leur vol ?
Nous avons créer une liste contenant les flèches actives, elle est vide au départ, une flèche y apparait quant un arc est utilisé et elle disparait quant elle détecte une colision avec un monstre ou un bloc.

### Comment gérez-vous le fait que vous avez maintenant deux types de monstres, et deux types d’armes ? Comment faites-vous pour ne pas dupliquer du code entre ceux-ci ?
Nous avons (entre la semaine 5 et 6) créé une classe abstraite monster et weapon pour les éléments communs aux deux types de monstres et d'armes. Chaque monstres et armes héritent donc de leurs propriétés et ont chacun leurs méthodes particulières (pour se dépacer, et autre).


## Semaine 6:
Semaine sans nouvelle question.


## Semaine 7:
Semaine sans nouvelle question.


## Semaine 8:

### Quel algorithme utilisez-vous pour identifier tous les blocs d’une plateformes, et leurs limites de déplacement ?
On part de la map dont on connait le type des éléments qui le compose (Flèche, Bloc, Autre) pour chaque coordonnée. Bloc contient tous les types d'éléments qui sont déplaçables selon les règles.
L'algorithme qui sort une liste de plateforme et les positions de départ et d'arrivée est le suivant :
1) On vérifie qu'avant chaque flèche on a une flèche ou un bloc (sinon on renvoie une erreur).
2) On garde en mémoire les blocs présents avant les flèches, appelés "need_to_look".
3) On crée une grille temporaire dont toutes les positions sont inconnues.
4) On itère sur les "need_to_look" de la façon suivant :
    (a) Le "need_to_look" est dévoilé (s'il l'était déjà il disparait car on l'a déjà traité), noté comme bloc dans la grille temporaire et comme élément d'une "bloc_list".
    (b) En itérant sur la "bloc_list", on dévoile les voisins de chaque éléments (de inconnues, on dévoiles leur type), pour chaqu'un :
    - si c'est un bloc ils sont enregistrés dans la "bloc_list"
    - si c'est la première flèche d'une série (et que l'élément avant est déjà dévoilé), on compte le nombre de flèche qui suit, on l'enregistre dans un "dict_dir" contenant les 4 directions et on dévoile les flèches observées.
    - sinon on ne fait rien.
5) L'ensemble de ("bloc_list" et "dict_dir") forment nos plateformes, il ne reste plus qu'à transformer notre "dict_dir" en position de départ (position du bloc need_to_look - flèches_gauche - flèches_bas) et en position d'arrivée (position du bloc need_to_look + flèches_droite + flèches_haut)

6) Le mouvement que font nos plateformes à une vitesse constante et fait des allers-retours entre la position de départ et d'arrivée. Ainsi, il est possible que le mouvement soit en diagonale, c'est volontaire pour ajouter du game-play (nous aurions pu vérifié que dans chaque "dict_dir" on a que des valeurs différentes de 0 en x ou en y).

### Sur quelle structure travaille cet algorithme ? Quels sont les avantages et inconvénients de votre choix ?
L'algorithme travaille au niveau de la grille d'un niveau, les coordonnées sont des tuples de int, ce qui permet une gestion plus simple et abstraite lors de la création des plateformes.

### Quelle bibliothèque utilisez-vous pour lire les instructions des interrupteurs ? Dites en une ou deux phrases pourquoi vous avez choisi celle-là.
La bibliothèque utilisée est "pyyaml>=6.0.2", c'est la première qui nous a été présentée lors de nos recherches et elle est très adaptée à notre usage.

#### Comment votre design général évolue-t-il pour tenir compte des interrupteurs et des portails ?
Les types interrupteur et portail sont ajoutés et avec ça leurs sprite et leurs caractère spécial de la map.
De plus, la façon dont on chargeait les éléments à du évoluer :
Avant, quand les sprites étaient chargés, leur élément était assigné à la liste corespondant à son type.
Mais les interupteurs dépendent des portails et les platformes bougeables forcent à placer nos éléments dans plusieurs listes ce qui n'était pas encore possible.
Maintenant, les sprites sont chargées, puis les listes appèlent les éléments dont elles ont besoin. Par exemple ici, la liste des portails est crée, puis la liste des switch est crée aux dépends des portails.
De plus, les leviers peuvent aussi se retrouver dans la liste des plateformes qui bougent quand elle est créée.

## Semaine 9:
Semaine sans nouvelle question.


## Semaine 10:
Semaine sans nouvelle question.


## Semaine 11:

### Nos nouvelles features :

#### Araignée (Spider)
Nouveau monstre : Les araignées
Elles se déplacent sur tout le contour des plateformes pour en faire le tour. Elles commencent posées sur un bloc et partant vèrs la droite, à vitesse constante. Leur comportement est largement symilaire à celui des blobs, elle tue la joueuse s'il y a une collision, se fait tuée par l'épée et les flèches, n'est pas supposée être sur une plateforme qui bouge et passe à travers les blobs.

#### Portails de taille (Portal)
Nouveau type de bloc : Les portails de taille
Ces nouveaux types de bloc sont répartis en 2 catégories : Les "plus" et les "moins"
Les "plus" font doubler la taille de notre personnage de 1 bloc de haut à 2 bloc de haut (ou de 1/2 à 1 s'il était petit).
Les "moins" font diviser par 2 la taille de notre personnage de 1 bloc de haut à 1/2 bloc de haut (ou de 2 à 1 s'il était grand).
Avant et après le portail une zone de 2x2 blocs est laissée vide (pour éviter les collisions ; On ne le détecte pas, mais nos niveaux et tests le vérifient toutes)
Leur comportement est le suivant : Lorsque le personnage détecte une collision avec un portail par la gauche (resp. par la droite), il est téléporté à sa droite (resp. à sa gauche) et est 2x plus grand / 2x plus petit dans la limite de 2 max. et 1/2 min.

## Semaine 12:
Fin des séries d'instructions

