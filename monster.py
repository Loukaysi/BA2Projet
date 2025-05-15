from abc import abstractmethod
from arcade import Sprite
from enum import Enum, auto
import math
import random
from map import Map

WALLS = ("full_grass","half_grass","box","gate")

SLIME_CAN_GO=("full_grass","half_grass")
SPIDER_CAN_GO=("full_grass","half_grass","box","lava")


SPRITE_SIZE = 64

BAT_CIRCLE_SCOPE = 40

class Monster:
    """
    Abstract class to represent the different monsters : 
    ``Slime`` and ``Bat``
    """
    monster_speed: int
    monster_sprite: Sprite
    initial_position: tuple[float|int,float|int]

    @abstractmethod
    def move(self)-> None:
        pass

    def __del__(self)->None:
        self.monster_sprite.kill()


class Slime(Monster):
    """
    Monster type that moves while staying on the ground
    """

    def __init__(self, slime_pos:tuple[int,int], game_map:Map, slime_sprite: Sprite)-> None:
        check_pos_x = slime_pos[0]
        distance = 0
        start = 0
        while (game_map.caracters.get(game_map.ShowPosition((check_pos_x,slime_pos[1]-1)),"") in SLIME_CAN_GO
                and game_map.caracters.get(game_map.ShowPosition((check_pos_x,slime_pos[1])),"") not in WALLS):
            check_pos_x -= 1
            start += 1
        check_pos_x+=1
        while (game_map.caracters.get(game_map.ShowPosition((check_pos_x,slime_pos[1]-1)),"") in SLIME_CAN_GO
                and game_map.caracters.get(game_map.ShowPosition((check_pos_x,slime_pos[1])),"") not in WALLS):
            check_pos_x += 1
            distance += 1
        slime_sprite.boundary_left = slime_sprite.center_x - SPRITE_SIZE * (start-1) - slime_sprite.rect.width/4
        slime_sprite.boundary_right = slime_sprite.center_x + SPRITE_SIZE * (distance - start) + slime_sprite.rect.width/4
        self.monster_sprite = slime_sprite
        self.monster_speed = -1

    def move(self)->None:
        self.monster_sprite.strafe(self.monster_speed)
        if isinstance(self.monster_sprite.boundary_right,float) and isinstance(self.monster_sprite.boundary_left,float):
            if self.monster_sprite.center_x <= self.monster_sprite.boundary_left:
                self.monster_speed = 1
                self.monster_sprite.texture = self.monster_sprite.texture.flip_horizontally()
            if self.monster_sprite.center_x >= self.monster_sprite.boundary_right:
                self.monster_speed = -1
                self.monster_sprite.texture = self.monster_sprite.texture.flip_horizontally()


class Bat(Monster):
    """Deal with the bat movements"""

    def __init__(self, sprite: Sprite)-> None:
        self.monster_sprite = sprite
        self.initial_position = sprite.position
    
    def move(self) -> None:
        # define the relative position of bat from the initial position
        relative_bat_position_x = self.monster_sprite.right - self.initial_position[0]
        relative_bat_position_y = self.monster_sprite.bottom - self.initial_position[1]
        # define the angle of movement of the bat
        move_angle = math.atan2(self.monster_sprite.change_y, self.monster_sprite.change_x) * 180 / math.pi
        # find the relative angle between the speed orientation and the relative position
        relative_angle = math.atan2(relative_bat_position_x, relative_bat_position_y) - move_angle
        
        # test if the vector size is bigger than the scope of action
        if math.sqrt(relative_bat_position_x**2 + relative_bat_position_y**2) >= BAT_CIRCLE_SCOPE :
            # test if the relative_angle is aligned with the angle of relative vector
            # turn the direction of movement if this is right
            move_angle += 3
            if (relative_angle) <= -90 and (relative_angle) >= 90 :
                self.monster_sprite.angle += 3
        else :
            # Change the orientation of bat randomly with an angle between -5 and 5
            move_angle += random.uniform(-5, 5)
        # Change the speed of bat with a speed constant (=1) in its orientation
        self.monster_sprite.change_y = math.sin(move_angle * math.pi / 180)*1
        self.monster_sprite.change_x = math.cos(move_angle * math.pi / 180)*1
        # Change the position of bat
        self.monster_sprite.center_x += self.monster_sprite.change_x*1
        self.monster_sprite.center_y += self.monster_sprite.change_y*1

        # Change the orientation of the sprite randomly, between -10 and 10 degrees
        self.monster_sprite.angle += random.uniform(-3, 3)
        if (self.monster_sprite.angle < -10) :
            self.monster_sprite.angle += random.uniform(0, 1)
        if (self.monster_sprite.angle > 10) :
            self.monster_sprite.angle += random.uniform(-1, 0)

class SPIDER_DIRECTION(Enum):
    RIGHT = auto()
    UP = auto()
    LEFT = auto()
    DOWN = auto()


class Spider(Monster):

    path:list[tuple[float,float,SPIDER_DIRECTION]] # final x coord, final y coord, direction until final coord
    step: int = 0

    def __init__(self,spider_pos:tuple[int,int], game_map:Map, spider_sprite: Sprite)->None:
        self.monster_sprite = spider_sprite
        self.__change_direction__(SPIDER_DIRECTION.RIGHT)
        self.path = [self.__convert_to_coord__(spider_pos,SPIDER_DIRECTION.RIGHT)]

    def __continue_path__(self,)->None:
        pass
        """(start,direction) = self.path[-1][0]
        need_to_look:tuple[tuple[int,int],tuple[int,int]]
        match direction:
            case SPIDER_DIRECTION.RIGHT:need_to_look = ((1,1),(1,0))
            case SPIDER_DIRECTION.UP:need_to_look = (0,1)
            case SPIDER_DIRECTION.LEFT:need_to_look = (-1,0)
            case SPIDER_DIRECTION.DOWN: need_to_look = (0,1)
        walk_lenght = 0"""



    def __convert_to_coord__(self,pos:tuple[int,int],dir:SPIDER_DIRECTION)->tuple[float,float,SPIDER_DIRECTION]:
        dist_from_Wall = self.monster_sprite.height/2
        match dir:
            case SPIDER_DIRECTION.RIGHT: return(SPRITE_SIZE*(1+pos[0])-dist_from_Wall,SPRITE_SIZE*pos[1]+dist_from_Wall,dir)
            case SPIDER_DIRECTION.UP: return(SPRITE_SIZE*(1+pos[0])-dist_from_Wall,SPRITE_SIZE*(1+pos[1])-dist_from_Wall,dir)
            case SPIDER_DIRECTION.LEFT: return(SPRITE_SIZE*pos[0]+dist_from_Wall,SPRITE_SIZE*(1+pos[1])-dist_from_Wall,dir)
            case SPIDER_DIRECTION.DOWN: return(SPRITE_SIZE*pos[0]+dist_from_Wall,SPRITE_SIZE*pos[1]+dist_from_Wall,dir)

    def __close_enough__(self,pos1:tuple[float,float],pos2:tuple[float,float])->bool:
        return (abs(pos1[1]-pos2[1]) < 1 and abs(pos1[0]-pos2[0]) < 1)

    def move(self)->None:
        self.monster_sprite.update()
        pos = (self.monster_sprite.center_x,self.monster_sprite.center_y)
        end = (self.path[self.step][0],self.path[self.step][1])
        if self.__close_enough__(pos,end):
            self.step = (self.step + 1) % len(self.path)
            self.__change_direction__(self.path[self.step][2])

    def __change_direction__(self,new_direction:SPIDER_DIRECTION)->None:
        speed_and_angle:tuple[int,int,int]
        match new_direction:
            case SPIDER_DIRECTION.RIGHT: speed_and_angle = (1,0,0)
            case SPIDER_DIRECTION.UP: speed_and_angle =    (0,1,-90)
            case SPIDER_DIRECTION.LEFT: speed_and_angle =  (-1,0,180)
            case SPIDER_DIRECTION.DOWN: speed_and_angle =  (0,-1,90)
        (self.monster_sprite.change_x, self.monster_sprite.change_y, self.monster_sprite.angle) = speed_and_angle     
