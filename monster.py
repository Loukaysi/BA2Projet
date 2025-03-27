from abc import abstractmethod
import arcade
import math
import random

class Monster:
    """All kind of enemies in the game
    This is an abstract class to deal with all the enemies
    """
    monster_sprite: arcade.Sprite

    @abstractmethod
    def move(self, *k)-> None:
        pass

    def __del__(self)->None:
        self.monster_sprite.kill()


class Slime(Monster):
    """Deal with the slimes movements"""

    def __init__(self, sprite: arcade.Sprite)-> None:
        self.monster_sprite = sprite

    def move(self, walls:arcade.SpriteList[arcade.Sprite],
             collision_sprite:arcade.Sprite=arcade.Sprite(":resources:/images/enemies/slimeBlue.png", scale=0.0001)
             )->None:
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

    initial_position: tuple

    def __init__(self, sprite: arcade.Sprite)-> None:
        self.monster_sprite = sprite
        self.initial_position = sprite.position
    
    def move(self, walls:arcade.SpriteList[arcade.Sprite]) -> None:
        # define the relative position of bat in function of the initial position
        relative_bat_position_x = self.monster_sprite.right - self.initial_position[0]
        relative_bat_position_y = self.monster_sprite.bottom - self.initial_position[1]
        # define the relative angle of bat in function of the orientation of sprite
        if (self.monster_sprite.angle < -180) :
            self.monster_sprite.angle += 360
        elif (self.monster_sprite.angle > 180) :
            self.monster_sprite.angle -= 360
        relative_angle = math.atan2(relative_bat_position_x, relative_bat_position_y) - self.monster_sprite.angle
        print(relative_angle)
        # test if the vector size is bigger than the scope of action
        if math.sqrt(relative_bat_position_x**2 + relative_bat_position_y**2) >= 40 :
            # test if the orientation of the bat is aligned with the angle of relative vector
            # turn the direction of movement if this is right
            if (relative_angle) <= 180 and (relative_angle) >= -180 :
                self.monster_sprite.angle += 5
        
        # Change the orientation of bat randomly with an angle between -5 and 5
        self.monster_sprite.turn_right(random.uniform(-5, 5))
        # Move the bat with a speed constant (=1) in its orientation 
        self.monster_sprite.strafe(1)


