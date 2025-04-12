from abc import abstractmethod
import arcade
import math

ARROW_BASE_SPEED = 20
ARROW_GRAVITY = 0.5

class Weapon:
    """Every weapon type
    abstract class for the weapons
    """
    weapon_sprite: arcade.Sprite
    texture:arcade.Texture
    aiming_position:tuple[float|int,float|int]
    offset_position:tuple[float|int,float|int]
    offset_angle:int
    offset_sprite_angle:float

    def __init__(self, player_position:tuple[float|int,float|int])->None:
        # Aim the weapon
        weapon_angle = math.atan2(self.aiming_position[1],self.aiming_position[0])
        self.weapon_sprite = arcade.Sprite(self.texture,
                                          center_x=player_position[0] + self.offset_position[0] + math.cos(self.offset_sprite_angle-weapon_angle)*self.offset_angle,
                                          center_y=player_position[1] + self.offset_position[1] + math.sin(self.offset_sprite_angle-weapon_angle)*self.offset_angle,
                                           scale=0.5*0.7)
        self.weapon_sprite.radians = self.offset_sprite_angle-weapon_angle


    @abstractmethod 
    def move(self, *positions:tuple[float|int,float|int],**collision:arcade.SpriteList[arcade.Sprite])->None:
        pass

class Sword(Weapon):
    """Player's Sword"""

    def __init__(self, player_position:tuple[float|int,float|int], camera:arcade.camera.Camera2D, aiming_to:tuple[float|int,float|int])-> None:
        self.offset_position = (13,-22)
        self.offset_angle = 18
        self.offset_sprite_angle = math.pi/4
        self.texture = arcade.load_texture("assets/kenney-voxel-items-png/sword_silver.png")

        vect_player_click_x = aiming_to[0] + camera.position[0] - player_position[0] - self.offset_position[0] - camera.width/2
        vect_player_click_y = aiming_to[1] + camera.position[1] - player_position[1] - self.offset_position[1] - camera.height/2
        self.aiming_position = (vect_player_click_x,vect_player_click_y)

        super().__init__(player_position)

    def move(self, *positions:tuple[float|int,float|int], **walls:arcade.SpriteList[arcade.Sprite])->None:
        player_position = positions[0]
        self.weapon_sprite.center_x=player_position[0] + self.offset_position[0] + math.cos(self.offset_sprite_angle-self.weapon_sprite.radians)*self.offset_angle
        self.weapon_sprite.center_y=player_position[1] + self.offset_position[1] + math.sin(self.offset_sprite_angle-self.weapon_sprite.radians)*self.offset_angle 

class Bow(Weapon):
    """Player's bow"""

    def __init__(self, player_position:tuple[float|int,float|int], camera:arcade.camera.Camera2D, aiming_to:tuple[float|int,float|int])-> None:
        self.offset_position = (13,-22)
        self.offset_angle = 0
        self.offset_sprite_angle = -math.pi/4
        self.texture = arcade.load_texture("assets/kenney-voxel-items-png/bow.png")

        vect_player_click_x = aiming_to[0] + camera.position[0] -player_position[0] - self.offset_position[0] - camera.width/2
        vect_player_click_y = aiming_to[1] + camera.position[1] -player_position[1] - self.offset_position[1] - camera.height/2
        self.aiming_position = (vect_player_click_x,vect_player_click_y)

        super().__init__(player_position)

    def move(self, *positions:tuple[float|int,float|int],**walls:arcade.SpriteList[arcade.Sprite])->None:
        player_position = positions[0]
        self.weapon_sprite.center_x=player_position[0] + self.offset_position[0] + math.cos(self.offset_sprite_angle-self.weapon_sprite.radians)*self.offset_angle
        self.weapon_sprite.center_y=player_position[1] + self.offset_position[1] + math.sin(self.offset_sprite_angle-self.weapon_sprite.radians)*self.offset_angle 

class Arrow(Weapon):
    """Arrows from the bow"""

    def __init__(self, player_position:tuple[float|int,float|int], camera:arcade.camera.Camera2D, aiming_to:tuple[float|int,float|int])-> None:
        self.offset_position = (13,-22)
        self.offset_angle = 0
        self.offset_sprite_angle = math.pi/4
        self.texture = arcade.load_texture("assets/kenney-voxel-items-png/arrow.png")

        vect_player_click_x = aiming_to[0] + camera.position[0] -player_position[0] - self.offset_position[0] - camera.width/2
        vect_player_click_y = aiming_to[1] + camera.position[1] -player_position[1] - self.offset_position[1] - camera.height/2
        self.aiming_position = (vect_player_click_x,vect_player_click_y)

        super().__init__(player_position)

        Vector = ARROW_BASE_SPEED

        self.weapon_sprite.change_x=Vector*math.cos(self.offset_sprite_angle-self.weapon_sprite.radians)
        self.weapon_sprite.change_y=Vector*math.sin(self.offset_sprite_angle-self.weapon_sprite.radians)

    def move(self, *positions:tuple[float|int,float|int], **walls:arcade.SpriteList[arcade.Sprite])->None:
        self.weapon_sprite.position = (self.weapon_sprite.position[0]+self.weapon_sprite.change_x,self.weapon_sprite.position[1]+self.weapon_sprite.change_y)
        self.weapon_sprite.change_y-=ARROW_GRAVITY

        if self.weapon_sprite.change_x!= 0:
            self.weapon_sprite.radians = self.offset_sprite_angle - math.atan2(self.weapon_sprite.change_y,self.weapon_sprite.change_x)
        else:
            self.weapon_sprite.radians = self.offset_sprite_angle

        if self.weapon_sprite.position[1] < 0:
           self.weapon_sprite.kill()
           del self

        else:
            for wall in walls:
                try:
                    if len(arcade.check_for_collision_with_list(self.weapon_sprite,walls[wall])):
                        self.weapon_sprite.kill()
                        del self
                except:
                    pass