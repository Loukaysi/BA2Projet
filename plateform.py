from typing import Final
from arcade import Sprite, SpriteList
from enum import Enum, auto
from map import Map

class Direction(Enum):
    X = auto()
    Y = auto()

class Around(Enum):
    UP=auto()
    LEFT=auto()
    DOWN=auto()
    RIGHT=auto()

class Plateform:
    blocs:Final[SpriteList[Sprite]]

    max_steps:dict[Direction,int]
    current_steps:dict[Direction,int]
    direction:dict[Direction,int]

    def __init__(self,blocs:SpriteList[Sprite],max_steps:tuple[int,int],current_steps:tuple[int,int])->None:
        self.blocs = blocs
        self.max_steps[Direction.X] = max_steps[0]
        self.max_steps[Direction.Y] = max_steps[1] 
        self.current_steps[Direction.X]=current_steps[0]
        self.current_steps[Direction.Y]=current_steps[1]
        self.direction = {Direction.X:1,Direction.Y:1}

    def move(self)->None:
        for pos,dir in enumerate(self.current_steps):
            if pos == self.max_steps[dir]:
                self.change_direction(dir)
            self.current_steps[dir]+=self.direction[dir]

    def change_direction(self,direction:Direction)->None:
        self.direction[direction]-=self.direction[direction]
        match direction:
            case Direction.X: 
                for bloc in self.blocs:
                    bloc.change_x -= bloc.change_x
            case Direction.Y: 
                for bloc in self.blocs:
                    bloc.change_y -= bloc.change_y

def find_plateforms(game_map:Map)->list[Plateform]:
    try:
        create_plateform(game_map,start_pos)
    except:
        raise("Wrong arrow positioning")

def create_plateform(game_map:Map,start_pos:tuple[int,int])->Plateform:
    vertical_max:int=-1
    vertical_min:int=-1
    horizontal_max:int=-1
    horizontal_min:int=-1

def look_around(game_map:Map,around_pos:tuple[int,int],look_at:Around)->str:
    