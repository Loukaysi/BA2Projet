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
...

### Sur quelle structure travaille cet algorithme ? Quels sont les avantages et inconvénients de votre choix ?
...

### Quelle bibliothèque utilisez-vous pour lire les instructions des interrupteurs ? Dites en une ou deux phrases pourquoi vous avez choisi celle-là.
...

#### Comment votre design général évolue-t-il pour tenir compte des interrupteurs et des portails ?
...


## Semaine 9:
...

## Semaine 10:
...

## Semaine 11:
...

## Semaine 12:
...

## Semaine 13:
...

## Semaine 14:
...