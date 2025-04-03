from abc import abstractmethod
import arcade
import math
import random

BAT_CIRCLE_SCOPE = 40

class Monster:
    """All kind of enemies in the game
    This is an abstract class to deal with all the enemies
    """
    monster_sprite: arcade.Sprite
    initial_position: tuple[float|int,float|int]

    @abstractmethod
    def move(self, walls:arcade.SpriteList[arcade.Sprite])-> None:
        pass

    def __del__(self)->None:
        self.monster_sprite.kill()


class Slime(Monster):
    """Deal with the slimes movements"""

    def __init__(self, sprite: arcade.Sprite)-> None:
        self.monster_sprite = sprite

    def move(self, walls:arcade.SpriteList[arcade.Sprite])->None:
        collision_sprite:arcade.Sprite = arcade.Sprite(":resources:/images/enemies/slimeBlue.png", scale=0.0001)
        # Check if the slime encountered a wall and if so, change his speed
        if len(arcade.check_for_collision_with_list(self.monster_sprite, walls)) != 0:
            self.monster_sprite.change_x = -self.monster_sprite.change_x
            self.monster_sprite.texture = self.monster_sprite.texture.flip_horizontally()
        # Check for ground in front
        if self.monster_sprite.change_x > 0:
            collision_sprite.position = (self.monster_sprite.right+self.monster_sprite.change_x,self.monster_sprite.bottom)
        else:
            collision_sprite.position = (self.monster_sprite.left+self.monster_sprite.change_x,self.monster_sprite.bottom)
        if len(arcade.check_for_collision_with_list(collision_sprite, walls)) == 0:
            self.monster_sprite.change_x = -self.monster_sprite.change_x
            self.monster_sprite.texture = self.monster_sprite.texture.flip_horizontally()
        self.monster_sprite.strafe(self.monster_sprite.change_x)


class Bat(Monster):
    """Deal with the bat movements"""

    def __init__(self, sprite: arcade.Sprite)-> None:
        self.monster_sprite = sprite
        self.initial_position = sprite.position
    
    def move(self, walls:arcade.SpriteList[arcade.Sprite]) -> None:
        # define the relative position of bat in function of the initial position
        relative_bat_position_x = self.monster_sprite.right - self.initial_position[0]
        relative_bat_position_y = self.monster_sprite.bottom - self.initial_position[1]
        # define the angle of movement of bat
        move_angle = math.atan2(self.monster_sprite.change_y, self.monster_sprite.change_x) * 180 / math.pi
        # calcul of the relative angle between the speed orientation and the relative position
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


