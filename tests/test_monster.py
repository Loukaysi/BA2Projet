from map import Map
import tempfile
import os
import arcade
from gameview import GameView
from monster import Slime
from monster import Bat
from monster import Monster
import math

SPRITE_SIZE = 64

def test_load_monster(window: arcade.Window) -> None:
    view = GameView()
    window.show_view(view)

    view.game_map = Map()
    with tempfile.NamedTemporaryFile(mode="w+",delete=False) as file:
        file.writelines([
            "width: 10\r", 
            "height: 6\r",
            "next-map: testmap.txt\r"  
            "---\r",
            "     S    \r",
            "----------\r",
            "          \r",
            "vvvvvvvvvv\r",
            "oooooooooo\r",
            "----------\r"
        ])
        file_name = file.name
        
    try:
        with open(file_name, mode="r") as file:
            view.game_map.ReadFile(file)
    finally:
        os.remove(file_name)

    view.Load_Map()

    assert(len(view.monster_list) == 20)

    count_slime:int = 0
    count_bat:int = 0

    for monster in view.monster_list:
        if IsSlime(monster):
            count_slime+=1
        elif IsBat(monster):
            count_bat+=1
        else:
            assert(False)
    
    assert(count_slime==10)
    assert(count_bat==10)

    # Only 1 loop for the time of the test as it takes a lot of time to execute 
    # NEED TO BE PUT BACK TO AT LEAST 24 TO MAKE SOME SLIMES GO BACK
    for i in range(24): # Check that all the slimes dans bats move within their scopes
        x:float|int
        y:float|int
        for monster in view.monster_list:
            x = monster.monster_sprite.position[0]
            y = monster.monster_sprite.position[1]
            if IsSlime(monster):
                assert(y == SPRITE_SIZE*3/2)
                assert(monster.monster_sprite.left>=0 and monster.monster_sprite.right<=SPRITE_SIZE*10) # Note : 10 is the edge of the right bloc
            if IsBat(monster):
                distance:float|int = math.sqrt((x-monster.initial_position[0])**2+(y-monster.initial_position[1])**2)
                assert(distance <= 100)
        window.test(30)

def IsSlime(monster:Monster)->bool:
    if isinstance(monster,Slime):
        return True
    else:
        return False
    
def IsBat(monster:Monster)->bool:
    if isinstance(monster,Bat):
        return True
    else:
        return False