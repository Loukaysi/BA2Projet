from abc import abstractmethod
import arcade
import math
import random

class Monster:
    """All kind of enemies in the game
    This is an abstract class to deal with all the enemies
    """
    monster_sprite: arcade.Sprite
    initial_position: tuple         # used for bat only

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
             collision_sprite:arcade.Sprite=arcade.Sprite(":resources:/images/enemies/slimeBlue.png",scale=0.0001))->None:
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

# sprit chauve souris : "assets/kenney-extended-enemies-png/bat.png"
# caractère d'apparition sur map : v

class Bat(Monster):
    """Deal with the bat movements"""

    def __init__(self, sprite: arcade.Sprite, )-> None:
        self.monster_sprite = sprite
        self.monster_sprite.change_x = 1    # speed_x initial
        self.monster_sprite.change_x = 0    # speed_y initial

    def move(self)->None:
        relative_position = (self.monster_sprite.right,self.monster_sprite.bottom) - self.initial_position
            
        # checks the bat's distance from its initial position
        # if it is too far (50 = scope of action), the bat changes orientation
        if math.sqrt((relative_position.x)**2 + (relative_position.y)**2) >= 50 :
            relative_angle = self.monster_sprite.angle - math.atan2(relative_position.y,relative_position.x)
            if relative_angle < 90 and relative_angle > -90 :
                self.monster_sprite.turn_right(self, 180)
            
        # move the bat in the direction of orientation, with a constant speed = 1
        self.monster_sprite.strafe(1)

        # turn the sprite with a random angle between -2 and 2 degres
        self.monster_sprite.turn_right(self, random.uniform(-2, 2))

            