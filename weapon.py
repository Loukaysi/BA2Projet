import math
from enum import IntEnum, auto
from arcade import Sprite
from common_types import pos_float_int

ARROW_BASE_SPEED = 20
ARROW_GRAVITY = 0.5

TRUE_SCALE = 0.5
RELATIVE_SCALE = 0.7*TRUE_SCALE

class Weapon(Sprite):
    """
    Abstract class used to represent every type of `Weapon` (namely `Sword`, `Bow` and `Arrow` ) 

    Holds the different parameter used to display the Sprites correctly according to their sprite

    Every attribute reprensents a different offset that needs to be adjusted, this attribute depends on the
    type of `Weapon`, see them seperately to see or adjust the offsets

    Also handles the movement of the weapons that are meant to be "held" (`Bow` and `Sword`) the movement of
    `Arrow` is handled seperately (see `Arrow`)

    Note : the player is left-handed and the offsets have been set "visually" so they aren't determined in any scientific way

    list of attributes

        `aiming_position` type (`pos_float_int`) : the vector which should be followed by the weapon

        `offset_position` type (`pos_float_int`) : the offset from the player position to the position where the weapon should be "held"

        `offset_angle` type (`float`) : the distance between the center of the sprite and the point where it should be "held"

        `offset_sprite_angle` type (`float`) : the offset needed for the weapon to be horizontal (i.e. if the sword is pointed upwards, it has an angle of pi/2)

    required files
        `weapon.py`
        `common_typs`

    required librabry
        `arcade`
        `enum`
    """
    aiming_position:pos_float_int
    offset_position:pos_float_int
    offset_angle:float
    offset_sprite_angle:float

    def __init__(self, player_position:pos_float_int,relative_to_player:pos_float_int, texture:str, scale:float=1)->None:
        """
        Aims the weapon with the given parameters
        """

        # find the vector which the weapon should follow
        vect_player_click_x = relative_to_player[0] -player_position[0] - self.offset_position[0]
        vect_player_click_y = relative_to_player[1] -player_position[1] - self.offset_position[1]
        self.aiming_position = (vect_player_click_x,vect_player_click_y)

        weapon_angle = math.atan2(self.aiming_position[1],self.aiming_position[0])
        # aim the weapon according to the scale
        super().__init__(texture,scale=RELATIVE_SCALE*scale,
                        center_x=player_position[0] + scale*(self.offset_position[0] + math.cos(self.offset_sprite_angle-weapon_angle)*self.offset_angle),
                        center_y=player_position[1] + scale*(self.offset_position[1] + math.sin(self.offset_sprite_angle-weapon_angle)*self.offset_angle)
                        )
        self.radians = self.offset_sprite_angle-weapon_angle

    def move(self, position:pos_float_int = (0,0))->None:
        """
        Move the weapon according to the player's position
        """
        player_position = position
        angle_offset = (math.cos(self.offset_sprite_angle-self.radians)*self.offset_angle,
                        math.sin(self.offset_sprite_angle-self.radians)*self.offset_angle)
        self.center_x=player_position[0] + self.scale[0]/RELATIVE_SCALE*(self.offset_position[0] + angle_offset[0])
        self.center_y=player_position[1] + self.scale[1]/RELATIVE_SCALE*(self.offset_position[1] + angle_offset[1]) 

class Sword(Weapon):
    """
    Subclass of ``Weapon`` used to define the offsets to aim the player's sword
    Adjust position relative to the player over time by using the ``move`` method
    """

    def __init__(self, player_position:pos_float_int, aiming_to:pos_float_int, scale:float = 1)-> None:
        """
        Calls ``Weapon.init`` with the different values to aim the sword "correctly"
        """
        self.offset_position = (13,-22)
        self.offset_angle = 18
        self.offset_sprite_angle = math.pi/4
        texture = "assets/kenney-voxel-items-png/sword_silver.png"

        super().__init__(player_position,aiming_to,texture, scale=scale,)

class Bow(Weapon):
    """
    Subclass of ``Weapon`` used to define the offsets to aim the player's bow
    Adjust position relative to the player over time by using the ``move()`` method
    """

    def __init__(self, player_position:pos_float_int, aiming_to:pos_float_int,scale:float = 1)-> None:
        """
        Calls ``Weapon.init()`` with the different values to aim the bow "correctly"
        """
        self.offset_position = (13,-22)
        self.offset_angle = 0
        self.offset_sprite_angle = -math.pi/4
        texture = "assets/kenney-voxel-items-png/bow.png"

        super().__init__(player_position,aiming_to,texture,scale = scale)
        

class Arrow(Weapon):
    """
    Subclass of ``Weapon`` used to create arrows

    Automatically follows a parabollic trajctory as if it was falling when using the ``move`` method

    The Sprite is also adjusted throughout the whole trajectory to seem "realistic"
    """

    def __init__(self, player_position:pos_float_int, aiming_to:pos_float_int,scale:float = 1)-> None:
        """
        Automaticaly calls ``Weapon.init()`` with the different values to aim the arrow "correctly"
        """
        self.offset_position = (13,-22)
        self.offset_angle = 0
        self.offset_sprite_angle = math.pi/4
        texture = "assets/kenney-voxel-items-png/arrow.png"

        super().__init__(player_position,aiming_to,texture,scale=scale)

        self.change_x=ARROW_BASE_SPEED*math.cos(self.offset_sprite_angle-self.radians)
        self.change_y=ARROW_BASE_SPEED*math.sin(self.offset_sprite_angle-self.radians)

    def move(self, position:pos_float_int = (0,0))->None:
        """
        Moves the arrow to form a parabollic trajectory overall
        The sprite is automatically aimed to follow the course of the trajectory  
        """
        self.position = (self.position[0]+self.change_x,self.position[1]+self.change_y)
        self.change_y-=ARROW_GRAVITY

        # makes sure that the arrow's angle can be calculated using the arctan() function
        if self.change_x!= 0: self.radians = self.offset_sprite_angle - math.atan2(self.change_y,self.change_x)
        else: self.radians = self.offset_sprite_angle

class Weapon_index(IntEnum):
    """
    Class to order the different held weapons

    It is a IntEnum to have an actual numerotation if needed
    """
    SWORD = auto()
    BOW = auto()