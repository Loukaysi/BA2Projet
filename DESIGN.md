# Design

Notre projet utilise la libraire "Arcade".

La principale classe est "GameView" (qui hérite de "arcade view") définie une fois au début, elle contient :
- Le personnage et ses caractéristiques
- La caméra et ses caractéristiques
- Les différents blocs, pièces, entrée et sortie du niveau en cours (map)
- Les monstres et armes
- Le physics_engine de arcade et autres spécificités de arcade
- Les sons, textes et score du jeu

Son initialisation est héritée de "arcade view".

Il a plein de méthodes à détailler :
...


- Lecture de fichier





La création des plateformes se fait de la façon suivante :
On part de la map dont on connait le type des éléments qui le compose (Flèche, Bloc, Autre) pour chaque coordonnée. Bloc contient tous les types d'éléments qui sont déplaçables selon les règles.
L'algorithme qui sort une liste de plateforme et les positions de départ et d'arrivée est le suivant :
1) On vérifie qu'avant chaque flèche on a une flèche ou un bloc (sinon on renvoie une erreur).
2) On garde en mémoire les blocs présents avant les flèches, appelés "need_to_look".
3) On crée une grille temporaire dont toutes les positions sont inconnues.
4) On itère sur les "need_to_look" de la façon suivant :
    (a) Le "need_to_look" est dévoilé (s'il l'était déjà il disparait car on l'a déjà traité), noté comme bloc dans la grille temporaire et comme élément d'une "bloc_list".
    (b) En itérant sur la "bloc_list", on dévoile les voisins de chaque éléments (de inconnues, on dévoiles leur type), pour chaqu'un :
    - si c'est un bloc ils sont enregistrés dans la "bloc_list"
    - et si c'est la première flèche d'une série on compte le nombre de flèche qui suit, on l'enregistre dans un "dict_dir" contenant les 4 directions et on dévoile les flèches observées.
    - sinon on ne fait rien.
5) L'ensemble de ("bloc_list" et "dict_dir") forment nos plateformes, il ne reste plus qu'à transformer notre "dict_dir" en position de départ (position du bloc need_to_look - flèches_gauche - flèches_bas) et en position d'arrivée (position du bloc need_to_look + flèches_droite + flèches_haut)

6) Le mouvement que font nos plateformes à une vitesse constante et fait des allers-retours entre la position de départ et d'arrivée. Ainsi, il est possible que le mouvement soit en diagonale, c'est volontaire pour ajouter du game-play (nous aurions pu vérifié que dans chaque "dict_dir" on a que des valeurs différentes de 0 en x ou en y).





Pour les armes, nous avons une classe abstraite Weapon et 3 classes enfants Sword, Bow et Arrow.
Weapon gère ...

Sword fait ...
Bow fait ...
Arrow fait ...

Pour les monstres, nous avons une classe abstraite Monster et 2 classes enfants Slime et Bat.
Monster gère ...

Slime fait ...
Bat fait ...





Features ajoutées :

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




Analyse de la complexité du chargement d’un niveau :
...


Analyse de la complexité du on_update :
...

