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
Types monstres :
- Blobs
- Chauves-souris
Types Armes :
- Epée
- Arc
...

