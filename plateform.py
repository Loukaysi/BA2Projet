from __future__ import annotations

from typing import Final
from enum import Enum, auto
from map import Map

TICK_PER_CASE = 200
CHARACTERS_PLATEFORM = ("=","-","x","£","E","^")
CHARACTERS_ARROW = ("→","↑","←","↓")

class Side(Enum):
    UP=auto()
    LEFT=auto()
    DOWN=auto()
    RIGHT=auto()
    
def match_arrow(arrow:str, before:bool=False)->Side:
    if not before:
        match arrow:
            case "↓":return Side.DOWN
            case "→":return Side.RIGHT
            case "↑":return Side.UP
            case "←":return Side.LEFT
    else :
        match arrow:
            case "↓":return Side.UP
            case "→":return Side.LEFT
            case "↑":return Side.DOWN
            case "←":return Side.RIGHT
    raise ValueError("Trying to match a caracter that is not an arrow")

class Characters(Enum):
    PLATEFORM=auto()
    ARROWS=auto()
    OTHER=auto()
    UNKNOWN=auto()

class Plateform:

    blocs:Final[list[tuple[int,int]]]
    pos_max:Final[tuple[int,int]]
    pos_start:Final[tuple[int,int]]

    def __init__(self,blocs:list[tuple[int,int]],max_steps:tuple[int,int],current_steps:tuple[int,int])->None:
        self.blocs = blocs
        self.pos_max = max_steps
        self.pos_start = current_steps

def create_plateforms(game_map:Map)->list[Plateform]:
    plateform_list:list[Plateform] = []
    current_map:list[list[Characters]] = [[Characters.UNKNOWN for i in range(game_map.height+1)] for j in range(game_map.width+1)]

    arrows_list:list[tuple[tuple[int,int],str]]= []
    arrows_list.extend([(pos,"→")for pos in game_map.FindElement("→")])
    arrows_list.extend([(pos,"↑")for pos in game_map.FindElement("↑")])
    arrows_list.extend([(pos,"←")for pos in game_map.FindElement("←")])
    arrows_list.extend([(pos,"↓")for pos in game_map.FindElement("↓")])
    need_to_look:list[tuple[int,int]]=[]

    for arrow in arrows_list:
        if look_at_arrow(game_map,arrow[0],arrow[1],before=True) not in CHARACTERS_ARROW:
            need_to_look.append(pos_at_arrow(arrow[0],arrow[1],before=True))
        elif look_at_arrow(game_map,arrow[0],arrow[1],before=True) != arrow[1]:
            raise Exception("Invalid arrow placement")

    if any(game_map.ShowPosition(pos) not in CHARACTERS_PLATEFORM for pos in need_to_look):
        raise Exception("Invalid arrow placement")

    for interesting_pos in need_to_look:
        if current_map[interesting_pos[0]][interesting_pos[1]] == Characters.UNKNOWN:
            bloc_list:list[tuple[int,int]]=[]
            max_dist:dict[Side,int]={}
            (bloc_list,max_dist,current_map) = plateform_limit(game_map,bloc_list,max_dist,current_map,interesting_pos)
            plateform_list.append(create_plateform(bloc_list,max_dist))
    return plateform_list

def plateform_limit(game_map:Map, bloc_list:list[tuple[int,int]], max_dist:dict[Side,int], current_map:list[list[Characters]],current_pos:tuple[int,int])->tuple[
        list[tuple[int,int]],dict[Side,int],list[list[Characters]]
]: # Output : bloc_list, max_dist, current_map
    current_caracter = game_map.ShowPosition(current_pos)
    if current_caracter in CHARACTERS_PLATEFORM:
        current_map[current_pos[0]][current_pos[1]] = Characters.PLATEFORM
        bloc_list.append(current_pos)
        for side in Side:
            next_pos = pos_at_side(current_pos,side)
            if current_map[next_pos[0]][next_pos[1]] == Characters.UNKNOWN:
                (bloc_list,max_dist,current_map) = plateform_limit(game_map,bloc_list,max_dist,current_map,pos_at_side(current_pos,side))
    elif current_caracter in CHARACTERS_ARROW:
        last_pos = pos_at_arrow(current_pos,current_caracter,before=True)
        if current_map[last_pos[0]][last_pos[1]] != Characters.UNKNOWN:
            side = match_arrow(current_caracter)
            current_map[current_pos[0]][current_pos[1]] = Characters.ARROWS
            if current_map[last_pos[0]][last_pos[1]] == Characters.PLATEFORM:
                if side in max_dist:
                    raise Exception("Multiple arrows on one bloc")
                max_dist[side]=1
            else:
                max_dist[side]+=1
            if look_around_side(game_map,current_pos,side) in CHARACTERS_ARROW:
                return plateform_limit(game_map,bloc_list,max_dist,current_map,pos_at_side(current_pos,side))
    else:
        if current_caracter != "":
            current_map[current_pos[0]][current_pos[1]] = Characters.OTHER
    return (bloc_list,max_dist,current_map)

def create_plateform(bloc_list:list[tuple[int,int]],max_dist:dict[Side,int])->Plateform:
    horizontal_steps = max_dist.get(Side.LEFT, 0) + max_dist.get(Side.RIGHT, 0)
    vertical_steps = max_dist.get(Side.UP, 0) + max_dist.get(Side.DOWN, 0)
    return Plateform(bloc_list, (horizontal_steps,vertical_steps),
                     (max_dist.get(Side.LEFT,0),max_dist.get(Side.DOWN, 0)))

def pos_at_side(side_pos:tuple[int,int],look_at:Side)->tuple[int,int]:
    match look_at:    
        case Side.UP:return (side_pos[0],side_pos[1]+1)
        case Side.LEFT:return (side_pos[0]-1,side_pos[1])
        case Side.DOWN:return (side_pos[0],side_pos[1]-1)
        case Side.RIGHT:return (side_pos[0]+1,side_pos[1])

def look_around_side(game_map:Map,around_pos:tuple[int,int],look_at:Side)->str:
    return game_map.ShowPosition(pos_at_side(around_pos,look_at))

def pos_at_arrow(arrow_pos:tuple[int,int],arrow:str,before:bool=False)->tuple[int,int]:
    return pos_at_side(arrow_pos,match_arrow(arrow,before))

def look_at_arrow(game_map:Map,around_pos:tuple[int,int],arrow:str,before:bool=False)->str:
    return game_map.ShowPosition(pos_at_arrow(around_pos,arrow,before))