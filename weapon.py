import arcade
import math
from enum import IntEnum, auto

ARROW_BASE_SPEED = 20
ARROW_GRAVITY = 0.5

class Weapon:
    """
    Abstract class for the weapons
    Refer to ``Sword``, ``Bow`` and ``Arrow`` for actual use
    """
    weapon_sprite: arcade.Sprite
    texture:arcade.Texture
    aiming_position:tuple[float|int,float|int]
    offset_position:tuple[float|int,float|int]
    offset_angle:int
    offset_sprite_angle:float

    def __init__(self, player_position:tuple[float|int,float|int],camera:arcade.camera.Camera2D, aiming_to:tuple[float|int,float|int])->None:
        """
        Aims the weapon with the given parameters
        """
        # Aim the weapon
        vect_player_click_x = aiming_to[0] + camera.position[0] -player_position[0] - self.offset_position[0] - camera.width/2
        vect_player_click_y = aiming_to[1] + camera.position[1] -player_position[1] - self.offset_position[1] - camera.height/2
        self.aiming_position = (vect_player_click_x,vect_player_click_y)

        weapon_angle = math.atan2(self.aiming_position[1],self.aiming_position[0])
        self.weapon_sprite = arcade.Sprite(self.texture,
                                          center_x=player_position[0] + self.offset_position[0] + math.cos(self.offset_sprite_angle-weapon_angle)*self.offset_angle,
                                          center_y=player_position[1] + self.offset_position[1] + math.sin(self.offset_sprite_angle-weapon_angle)*self.offset_angle,
                                           scale=0.5*0.7)
        self.weapon_sprite.radians = self.offset_sprite_angle-weapon_angle

    def move(self, position:tuple[float|int,float|int] = (0,0))->None:
        """
        Move the weapon according to the player's position
        """
        player_position = position
        self.weapon_sprite.center_x=player_position[0] + self.offset_position[0] + math.cos(self.offset_sprite_angle-self.weapon_sprite.radians)*self.offset_angle
        self.weapon_sprite.center_y=player_position[1] + self.offset_position[1] + math.sin(self.offset_sprite_angle-self.weapon_sprite.radians)*self.offset_angle 

    def hit(self, collision_with:arcade.SpriteList[arcade.Sprite])->arcade.SpriteList[arcade.Sprite]:
        return arcade.check_for_collision_with_list(self.weapon_sprite,collision_with)

class Sword(Weapon):
    """
    Subclass of ``Weapon`` used to define the offsets to aim the player's sword
    Adjust position relative to the player overtime by using the ``move()`` method
    """

    def __init__(self, player_position:tuple[float|int,float|int], camera:arcade.camera.Camera2D, aiming_to:tuple[float|int,float|int])-> None:
        """
        Automaticaly calls ``Weapon.init()`` with the different values to aim the sword "correctly"
        """
        self.offset_position = (13,-22)
        self.offset_angle = 18
        self.offset_sprite_angle = math.pi/4
        self.texture = arcade.load_texture("assets/kenney-voxel-items-png/sword_silver.png")

        super().__init__(player_position,camera,aiming_to)

class Bow(Weapon):
    """
    Subclass of ``Weapon`` used to define the offsets to aim the player's bow
    Adjust position relative to the player overtime by using the ``move()`` method
    """

    def __init__(self, player_position:tuple[float|int,float|int], camera:arcade.camera.Camera2D, aiming_to:tuple[float|int,float|int])-> None:
        """
        Automaticaly calls ``Weapon.init()`` with the different values to aim the bow "correctly"
        """
        self.offset_position = (13,-22)
        self.offset_angle = 0
        self.offset_sprite_angle = -math.pi/4
        self.texture = arcade.load_texture("assets/kenney-voxel-items-png/bow.png")

        super().__init__(player_position,camera,aiming_to)
        

class Arrow(Weapon):
    """
    Subclass of ``Weapon`` used to create arrows
    Automatically follows a parabollic trajctory as if it was fallaing when using the ``move()`` method
    The ``move()`` method also requires the list of walls to know when the sprite should disappear
    """

    def __init__(self, player_position:tuple[float|int,float|int], camera:arcade.camera.Camera2D, aiming_to:tuple[float|int,float|int])-> None:
        """
        Automaticaly calls ``Weapon.init()`` with the different values to aim the arrow "correctly"
        """
        self.offset_position = (13,-22)
        self.offset_angle = 0
        self.offset_sprite_angle = math.pi/4
        self.texture = arcade.load_texture("assets/kenney-voxel-items-png/arrow.png")

        super().__init__(player_position,camera,aiming_to)

        Vector = ARROW_BASE_SPEED

        self.weapon_sprite.change_x=Vector*math.cos(self.offset_sprite_angle-self.weapon_sprite.radians)
        self.weapon_sprite.change_y=Vector*math.sin(self.offset_sprite_angle-self.weapon_sprite.radians)

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
        self.weapon_sprite.position = (self.weapon_sprite.position[0]+self.weapon_sprite.change_x,self.weapon_sprite.position[1]+self.weapon_sprite.change_y)
        self.weapon_sprite.change_y-=ARROW_GRAVITY

        if self.weapon_sprite.change_x!= 0: # makes sure that the arrow's angle can be calculated using the arctan() function
            self.weapon_sprite.radians = self.offset_sprite_angle - math.atan2(self.weapon_sprite.change_y,self.weapon_sprite.change_x)
        else:
            self.weapon_sprite.radians = self.offset_sprite_angle

        if self.weapon_sprite.position[1] < 0: # check if we are bellow the screen
           self.weapon_sprite.kill()

class Weapon_index(IntEnum):
    """
    Class to find an "order" on the weapon arsenal of the player
    """
    SWORD = auto()
    BOW = auto()