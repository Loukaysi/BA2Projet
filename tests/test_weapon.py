from map import Map
import tempfile
import os
import arcade
from gameview import GameView

SPRITE_SIZE = 64
# Size of each sprite for the map

def test_weapon(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)

    view.game_map = Map()
    with tempfile.NamedTemporaryFile(mode="w+",delete=False) as file:
        file.writelines([
            "width: 10\r", 
            "height: 2\r",
            "next-map: testmap.txt\r"  
            "---\r",
            "S  xox    \r",
            "----------\r"
        ])
        file_name = file.name
        
    try:
        with open(file_name, mode="r") as file:
            view.game_map.ReadFile(file)
    finally:
        os.remove(file_name)

    view.Load_Map()

    assert(len(view.monster_list)==1)
    view.player_sprite.position=((3+1/2)*SPRITE_SIZE,(3+1/2)*SPRITE_SIZE)

    # Hit
    x:int= int(view.player_sprite.position[0]-view.camera.position[0]) + 1000
    y:int= int(view.player_sprite.position[1]-view.camera.position[1])

    view.on_mouse_press(x,y,arcade.MOUSE_BUTTON_LEFT, 0)
    window.test(120)
    view.on_mouse_release(x,y,arcade.MOUSE_BUTTON_LEFT, 0)
    