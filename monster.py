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