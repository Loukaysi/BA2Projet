from abc import abstractmethod
from arcade import Sprite
from enum import Enum, auto
import math
import random
from map import Map
from subsprite import SubSprite

WALLS = ("full_grass","half_grass","box","gate")

SLIME_CAN_GO=("full_grass","half_grass")
SPIDER_CAN_GO=("full_grass","half_grass","box","lava")

SPIDER_SPEED = 3
SPRITE_SIZE = 64

BAT_CIRCLE_SCOPE = 40

class Monster(SubSprite):
    """
    Abstract class to represent the different monsters : 
    ``Slime`` and ``Bat``
    """

    def __init__(self,sprite:Sprite)->None:
        super().__init__(sprite)
        
    @abstractmethod
    def move(self)-> None:
        pass


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
        super().__init__(slime_sprite)
        self.change_x = -1

    def move(self)->None:
        self.update()
        if isinstance(self.boundary_right,float) and isinstance(self.boundary_left,float):
            if self.center_x <= self.boundary_left:
                self.change_x = 1
                self.texture = self.texture.flip_horizontally()
            if self.center_x >= self.boundary_right:
                self.change_x = -1
                self.texture = self.texture.flip_horizontally()


class Bat(Monster):
    """Deal with the bat movements"""

    initial_position: tuple[float|int,float|int]

    def __init__(self, sprite: Sprite)-> None:
        super().__init__(sprite)
        self.initial_position = sprite.position
    
    def move(self) -> None:
        # define the relative position of bat from the initial position
        relative_bat_position_x = self.right - self.initial_position[0]
        relative_bat_position_y = self.bottom - self.initial_position[1]
        # define the angle of movement of the bat
        move_angle = math.atan2(self.change_y, self.change_x) * 180 / math.pi
        # find the relative angle between the speed orientation and the relative position
        relative_angle = math.atan2(relative_bat_position_x, relative_bat_position_y) - move_angle
        
        # test if the vector size is bigger than the scope of action
        if math.sqrt(relative_bat_position_x**2 + relative_bat_position_y**2) >= BAT_CIRCLE_SCOPE :
            # test if the relative_angle is aligned with the angle of relative vector
            # turn the direction of movement if this is right
            move_angle += 3
            if (relative_angle) <= -90 and (relative_angle) >= 90 :
                self.angle += 3
        else :
            # Change the orientation of bat randomly with an angle between -5 and 5
            move_angle += random.uniform(-5, 5)
        # Change the speed of bat with a speed constant (=1) in its orientation
        self.change_y = math.sin(move_angle * math.pi / 180)*1
        self.change_x = math.cos(move_angle * math.pi / 180)*1
        # Change the position of bat
        self.center_x += self.change_x*1
        self.center_y += self.change_y*1

        # Change the orientation of the sprite randomly, between -10 and 10 degrees
        self.angle += random.uniform(-3, 3)
        if (self.angle < -10) :
            self.angle += random.uniform(0, 1)
        if (self.angle > 10) :
            self.angle += random.uniform(-1, 0)

class SPIDER_DIRECTION(Enum):
    RIGHT = auto()
    UP = auto()
    LEFT = auto()
    DOWN = auto()

position_float_type = tuple[float,float]
position_int_type = tuple[int,int]

class Spider(Monster):

    path_sprite_pos:list[tuple[position_float_type,SPIDER_DIRECTION]] # final x coord, final y coord, direction until final coord
    path_map_pos:list[tuple[position_int_type,SPIDER_DIRECTION]]
    step: int = 0

    def __init__(self,spider_pos:position_int_type, game_map:Map, spider_sprite: Sprite)->None:
        super().__init__(spider_sprite)
        self.__change_direction__(SPIDER_DIRECTION.RIGHT)
        self.path_sprite_pos = []
        self.path_map_pos = []
        (path_over,direction) = self.__continue_path__(spider_pos,SPIDER_DIRECTION.RIGHT,game_map)
        while not path_over :
            (path_over,direction)=self.__continue_path__(self.path_map_pos[-1][0],direction,game_map)
        self.__build_path_coord__()

    def __continue_path__(self,pos:position_int_type,direction:SPIDER_DIRECTION,map:Map)->tuple[bool,SPIDER_DIRECTION]:
        current_pos = pos
        while not self.__bloc_in_front__(current_pos,direction,map,False) and self.__bloc_in_front__(current_pos,direction,map,True):
            current_pos = self.__move_to__(current_pos,direction)
        
        if self.__bloc_in_front__(current_pos,direction,map,False):
            new_dir = self.__perp__(direction)
        else: 
            new_dir = self.__perp__(direction,up = False)
            current_pos = self.__move_to__(current_pos,direction)

        if len(self.path_map_pos) > 0:
            if current_pos == self.path_map_pos[0][0] and direction == SPIDER_DIRECTION.RIGHT: return (True,new_dir)
        self.path_map_pos.append((current_pos,direction))
        return (False,new_dir)

    def __bloc_in_front__(self,pos:position_int_type,dir:SPIDER_DIRECTION ,map:Map, bellow:bool)->bool:
        if bellow:offset = -1
        else: offset = 0

        match dir:
            case SPIDER_DIRECTION.RIGHT:need_to_look = (pos[0]+1,pos[1]+offset)
            case SPIDER_DIRECTION.UP:need_to_look = (pos[0]-offset,pos[1]+1)
            case SPIDER_DIRECTION.LEFT:need_to_look = (pos[0]-1,pos[1]-offset)
            case SPIDER_DIRECTION.DOWN: need_to_look = (pos[0]+offset,pos[1]-1)
        caracter = map.ShowPosition(need_to_look)
        if caracter in map.caracters:
            if map.caracters[map.ShowPosition(need_to_look)] in SPIDER_CAN_GO: return True
        return False

    def __close_enough__(self,pos1:position_float_type, pos2:position_float_type)->bool:
        return (abs(pos1[1]-pos2[1]) < SPIDER_SPEED and abs(pos1[0]-pos2[0]) < SPIDER_SPEED)

    def move(self)->None:
        self.update()
        pos = (self.center_x,self.center_y)
        end = (self.path_sprite_pos[self.step][0][0],self.path_sprite_pos[self.step][0][1])
        if self.__close_enough__(pos,end):
            self.step = (self.step + 1) % len(self.path_sprite_pos)
            self.__change_direction__(self.path_sprite_pos[self.step][1])

    def __build_path_coord__(self)->None:
        segment_amount = len(self.path_map_pos)
        for i in range(segment_amount):
            segment = self.path_map_pos[i]
            self.path_sprite_pos.append(self.__convert_to_coord__(
                segment[0],segment[1],self.__is_perp__(segment[1],self.path_map_pos[(i+1)%segment_amount][1])))

    def __perp__(self,dir:SPIDER_DIRECTION,up:bool=True)->SPIDER_DIRECTION:
        if up:
            match dir:
                case SPIDER_DIRECTION.RIGHT: return SPIDER_DIRECTION.UP
                case SPIDER_DIRECTION.UP: return SPIDER_DIRECTION.LEFT
                case SPIDER_DIRECTION.LEFT: return SPIDER_DIRECTION.DOWN
                case SPIDER_DIRECTION.DOWN: return SPIDER_DIRECTION.RIGHT 
        else:
            match dir:
                case SPIDER_DIRECTION.RIGHT: return SPIDER_DIRECTION.DOWN
                case SPIDER_DIRECTION.UP: return SPIDER_DIRECTION.RIGHT
                case SPIDER_DIRECTION.LEFT: return SPIDER_DIRECTION.UP
                case SPIDER_DIRECTION.DOWN: return SPIDER_DIRECTION.LEFT

    def __is_perp__(self,dir:SPIDER_DIRECTION,dir_to_check:SPIDER_DIRECTION,up:bool=True)->bool:
        return dir_to_check == self.__perp__(dir,up=up)        

    def __move_to__(self,pos:position_int_type,dir:SPIDER_DIRECTION)->position_int_type:
        match dir:
            case SPIDER_DIRECTION.RIGHT: return(pos[0]+1,pos[1])
            case SPIDER_DIRECTION.UP: return (pos[0],pos[1]+1)
            case SPIDER_DIRECTION.LEFT: return (pos[0]-1,pos[1])
            case SPIDER_DIRECTION.DOWN: return (pos[0],pos[1]-1)

    def __convert_to_coord__(self,pos:position_int_type,dir:SPIDER_DIRECTION, go_up:bool = True)->tuple[position_float_type,SPIDER_DIRECTION]:
        dist_from_wall = self.height/2
        up_factor = SPRITE_SIZE/2 - dist_from_wall
        if not go_up:up_factor = -up_factor

        match dir:
            case SPIDER_DIRECTION.RIGHT: return((SPRITE_SIZE*(1/2+pos[0])+up_factor,SPRITE_SIZE*pos[1]+dist_from_wall),dir)
            case SPIDER_DIRECTION.UP: return((SPRITE_SIZE*(1+pos[0])-dist_from_wall,SPRITE_SIZE*(1/2+pos[1])+up_factor),dir)
            case SPIDER_DIRECTION.LEFT: return((SPRITE_SIZE*(1/2 + pos[0])-up_factor,SPRITE_SIZE*(1+pos[1])-dist_from_wall),dir)
            case SPIDER_DIRECTION.DOWN: return((SPRITE_SIZE*pos[0]+dist_from_wall,SPRITE_SIZE*(1/2+pos[1])-up_factor),dir)

    def __change_direction__(self,new_direction:SPIDER_DIRECTION)->None:
        speed_and_angle:tuple[int,int,int]
        match new_direction:
            case SPIDER_DIRECTION.RIGHT: speed_and_angle = (SPIDER_SPEED,0,0)
            case SPIDER_DIRECTION.UP: speed_and_angle =    (0,SPIDER_SPEED,-90)
            case SPIDER_DIRECTION.LEFT: speed_and_angle =  (-SPIDER_SPEED,0,180)
            case SPIDER_DIRECTION.DOWN: speed_and_angle =  (0,-SPIDER_SPEED,90)
        (self.change_x, self.change_y, self.angle) = speed_and_angle     
