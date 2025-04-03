from map import Map
import tempfile
import os
import arcade
from gameview import GameView

def test_load_coins(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)

    view.game_map = Map()
    with tempfile.NamedTemporaryFile(mode="w+",delete=False) as file:
        file.writelines([
            "width: 10\r", 
            "height: 2\r",
            "next-map: testmap.txt\r"  
            "---\r",
            "S  **  ***\r",
            "----------\r"
        ])
        file_name = file.name
        
    try:
        with open(file_name, mode="r") as file:
            view.game_map.ReadFile(file)
    finally:
        os.remove(file_name)

    view.Load_Map()

    assert(view.score==0)
    assert(len(view.coin_sprite_list)==5)

    # Collect coins
    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(35)
    view.on_key_release(arcade.key.RIGHT, 0)
    assert(len(view.coin_sprite_list)==3)
    assert(view.score==2)

    view.on_key_press(arcade.key.RIGHT, 0)
    window.test(50)
    view.on_key_release(arcade.key.RIGHT, 0)
    assert(len(view.coin_sprite_list)==0)
    assert(view.score==5)