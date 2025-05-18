import arcade
import math
from enum import IntEnum, auto
from arcade import Sprite, SpriteList, SpriteSequence

ARROW_BASE_SPEED = 20
ARROW_GRAVITY = 0.5

TRUE_SCALE = 0.5
RELATIVE_SCALE = 0.7*TRUE_SCALE

class Weapon(Sprite):
    """
    Abstract class for the weapons
    Refer to ``Sword``, ``Bow`` and ``Arrow`` for actual use
    """
    weapon_sprite:Sprite
    texture:arcade.Texture
    aiming_position:tuple[float|int,float|int]
    offset_position:tuple[float|int,float|int]
    offset_angle:int
    offset_sprite_angle:float

    def __init__(self, player_position:tuple[float|int,float|int],relative_to_player:tuple[float|int,float|int], texture:str, scale:float=1)->None:
        """
        Aims the weapon with the given parameters
        """

        # Aim the weapon
        vect_player_click_x = relative_to_player[0] -player_position[0] - self.offset_position[0]
        vect_player_click_y = relative_to_player[1] -player_position[1] - self.offset_position[1]
        self.aiming_position = (vect_player_click_x,vect_player_click_y)

        weapon_angle = math.atan2(self.aiming_position[1],self.aiming_position[0])
        super().__init__(texture,scale=RELATIVE_SCALE*scale,
                        center_x=player_position[0] + scale*(self.offset_position[0] + math.cos(self.offset_sprite_angle-weapon_angle)*self.offset_angle),
                        center_y=player_position[1] + scale*(self.offset_position[1] + math.sin(self.offset_sprite_angle-weapon_angle)*self.offset_angle)
                        )
        self.radians = self.offset_sprite_angle-weapon_angle

    def move(self, position:tuple[float|int,float|int] = (0,0))->None:
        """
        Move the weapon according to the player's position
        """
        player_position = position
        self.center_x=player_position[0] + self.scale[0]/RELATIVE_SCALE*(self.offset_position[0] + math.cos(self.offset_sprite_angle-self.radians)*self.offset_angle)
        self.center_y=player_position[1] + self.scale[1]/RELATIVE_SCALE*(self.offset_position[1] + math.sin(self.offset_sprite_angle-self.radians)*self.offset_angle) 

class Sword(Weapon):
    """
    Subclass of ``Weapon`` used to define the offsets to aim the player's sword
    Adjust position relative to the player overtime by using the ``move()`` method
    """

    def __init__(self, player_position:tuple[float|int,float|int], aiming_to:tuple[float|int,float|int], scale:float = 1)-> None:
        """
        Automaticaly calls ``Weapon.init()`` with the different values to aim the sword "correctly"
        """
        self.offset_position = (13,-22)
        self.offset_angle = 18
        self.offset_sprite_angle = math.pi/4
        texture = "assets/kenney-voxel-items-png/sword_silver.png"

        super().__init__(player_position,aiming_to,texture, scale=scale,)

class Bow(Weapon):
    """
    Subclass of ``Weapon`` used to define the offsets to aim the player's bow
    Adjust position relative to the player overtime by using the ``move()`` method
    """

    def __init__(self, player_position:tuple[float|int,float|int], aiming_to:tuple[float|int,float|int],scale:float = 1)-> None:
        """
        Automaticaly calls ``Weapon.init()`` with the different values to aim the bow "correctly"
        """
        self.offset_position = (13,-22)
        self.offset_angle = 0
        self.offset_sprite_angle = -math.pi/4
        texture = "assets/kenney-voxel-items-png/bow.png"

        super().__init__(player_position,aiming_to,texture,scale = scale)
        

class Arrow(Weapon):
    """
    Subclass of ``Weapon`` used to create arrows
    Automatically follows a parabollic trajctory as if it was fallaing when using the ``move()`` method
    The ``move()`` method also requires the list of walls to know when the sprite should disappear
    """

    def __init__(self, player_position:tuple[float|int,float|int], aiming_to:tuple[float|int,float|int],scale:float = 1)-> None:
        """
        Automaticaly calls ``Weapon.init()`` with the different values to aim the arrow "correctly"
        """
        self.offset_position = (13,-22)
        self.offset_angle = 0
        self.offset_sprite_angle = math.pi/4
        texture = "assets/kenney-voxel-items-png/arrow.png"

        super().__init__(player_position,aiming_to,texture,scale=scale)

        Vector = ARROW_BASE_SPEED

        self.change_x=Vector*math.cos(self.offset_sprite_angle-self.radians)
        self.change_y=Vector*math.sin(self.offset_sprite_angle-self.radians)

    def move(self, position:tuple[float|int,float|int] = (0,0))->None:
        """
        Moves the arrow to form a parabollic trajectory overall
        The sprite is automatically aimed to follow the course of the trajectory  

        SpriteLists can also be given as an optionnal argument. 
        The arrow will be destroyed when hitting any of them 

        !! 
        Caution : There is no return value regardless of the state of the arrow (if it hit a wall or not)
        It is up to the user to check if the sprite still exists or not
        !!
        """
        self.position = (self.position[0]+self.change_x,self.position[1]+self.change_y)
        self.change_y-=ARROW_GRAVITY

        # makes sure that the arrow's angle can be calculated using the arctan() function
        if self.change_x!= 0: self.radians = self.offset_sprite_angle - math.atan2(self.change_y,self.change_x)
        else: self.radians = self.offset_sprite_angle

class Weapon_index(IntEnum):
    """
    Class to find an "order" on the weapon arsenal of the player
    """
    SWORD = auto()
    BOW = auto()