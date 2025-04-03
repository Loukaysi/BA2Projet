from map import Map
import tempfile
import os
import arcade
from gameview import GameView

SPRITE_SIZE = 64
# Size of each sprite for the map

def test_load_walls(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)

    view.game_map = Map()
    with tempfile.NamedTemporaryFile(mode="w+",delete=False) as file:
        file.writelines([
            "width: 10\r", 
            "height: 5\r",
            "next-map: testmap.txt\r"  
            "---\r",
            "xxxxxxxxxx\r",
            "          \r",
            "==========\r",
            "    S     \r",
            "----------\r"
        ])
        file_name = file.name
        
    try:
        with open(file_name, mode="r") as file:
            view.game_map.ReadFile(file)
    finally:
        os.remove(file_name)

    view.Load_Map()

    for i in range (30): # Use the player to test for collision with every wall
        view.player_sprite.position = ((i%10 + 1/2)*SPRITE_SIZE,(2*(i//10) + 1/2)*SPRITE_SIZE)
        assert(len(arcade.check_for_collision_with_list(view.player_sprite,view.wall_sprite_list))!=0)
    
    for i in range (30): # Use the player to test for empty spaces
        view.player_sprite.position = ((i%10 + 1/2)*SPRITE_SIZE,(2*(i//10) + 3/2)*SPRITE_SIZE)
        assert(len(arcade.check_for_collision_with_list(view.player_sprite,view.wall_sprite_list))==0)