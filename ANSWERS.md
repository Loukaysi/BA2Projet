## Semaine 1 : 
Pas de question, il s'agit du début du projet

## Semaine 2 :
Pas de question, il s'agit du début du projet

## Semaine 3 :
### "Comment avez-vous conçu la lecture du fichier ? Comment l’avez-vous structurée de sorte à pouvoir la tester de manière efficace ?"
Pour tester la lecture de fichier, nous avons commencé par simplement afficher tous les caractères présent dans ce dernier puis il a fallu diviser l'analyse de ce dernier 2 parties : Les paramètres puis la carte en elle-même. Pour simplifier l'utilisation de ce dernier, la lecture s'effectue une seule fois puis les données sotckées dans des listes adaptées.
### "Comment avez-vous adapté vos tests existants au fait que la carte ne soit plus la même qu’au départ ? Est-ce que vos tests résisteront à d’autres changements dans le futur ? Si oui, pourquoi ? Si non, que pensez-vous faire plus tard ?"
Nous avons créé une map de test pour tester toutes les options séparément (par exemple, lave, slime, pièces), donc les tests resisteront aux futurs changements car la carte de test de changera pas 
### "Le code qui gère la lave ressemble-t-il plus à celui de l’herbe, des pièces, ou des blobs ? Expliquez votre réponse."
Il ressemble plus au code des pièces car on cherche une collision entre le joueur et la lave
### "Comment détectez-vous les conditions dans lesquelles les blobs doivent changer de direction ?"
Pour les collisions avec les murs, on utilise la même méthode que pour les collisions entre les pièces et le joueur. Pour savoir s'il existe du sol là où le blob veut avancer, on crée un "sprite temporaire" et on regarde s'il est en collisions avec du sol au pied du blob.

## Semaine 4 :
### Quelles formules utilisez-vous exactement pour l’épée ? Comment passez-vous des coordonnées écran aux coordonnées monde ?
Si on considère, la position absolue du joueur P, la position absolue du centre de l'écran C, les dimensions de l'écran h et w, et la position relative du clic S, On calcule d'abord le clic relativement au joueur V := S + C - P - (w/2,h/2) et on utilise alors la fonction atan2 de la librairie math sur les coordonnées Vx et Vy.
Pour l'affichage, on décale en plus un peu l'épée mais ces alignements sont "à l'oeil" alors il n'y a pas de formules formelles.
### Comment testez-vous l’épée ? Comment testez-vous que son orientation est importante pour déterminer si elle touche un monstre ?

### Comment transférez-vous le score de la joueuse d’un niveau à l’autre ?
Il s'agit d'un atribut de Gameview qui n'est pas remis à 0 quand on utilise la méthode pour charger la carte
### Où le remettez-vous à zéro ? Avez-vous du code dupliqué entre les cas où la joueuse perd parce qu’elle a touché un ou monstre ou de la lave ?
Cela se fait dans la fonction Setup alors il n'y a pas de code en double
### Comment modélisez-vous la “next-map” ? Où la stockez-vous, et comment la traitez-vous quand la joueuse atteint le point E ?
Nous avons créé une classe "Map" qui se charge de la lecture des fichiers, notamment, de sauvegarder les paramètres de cette dernière alors nous pouvons aller chercher cette information dans cette liste. De fait, il nous suffit de rappeler la méthode qui lit le fichier "suivant" pour charger une nouvelle carte
### Que se passe-t-il si la joueuse atteint le E mais la carte n’a pas de next-map ?
Pour l'instant, la joueuse est déplacée vers la droite de quelques pixels mais, à long temre, ceci peut-être changé sans problèmes car c'est une situation que nous détectons.

## Semaine 5 :
... A remplir la semaine 7

## Semaine 6:
...

## Semaine 7:
...

## Semaine 8:
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