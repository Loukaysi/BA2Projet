from arcade import Sprite
from player import Player
from enum import Enum,auto
from subsprite import SubSprite

size_values = tuple[float, float, float, float] # In order : gravity / size / jump_speed / horizontal_speed

class Size(Enum):
    VERY_BIG=auto()
    BIG=auto()
    NORMAL=auto()
    SMALL=auto()
    VERY_SMALL=auto()

    def size_values(self)->size_values:
        match self: # Handpicked values, not meant to represent anything
            # In order : gravity / size / jump_speed / horizontal_speed
            # And of course as we all know, falling speed is directly proportiannal to mass
            case Size.VERY_BIG:return(0.5,2,18,4)
            case Size.BIG:return(0.75,1.5,18,5)
            case Size.NORMAL:return(1,1,20,6)
            case Size.SMALL:return(0.4,0.75,9,8)
            case Size.VERY_SMALL:return(0.3,0.5,7,10)
            case _: raise Exception("Error with the Size class, should not happen")


class Portal(SubSprite):
    size_to:Size

    def __init__(self,sprite:Sprite,size:str)->None:
        self.sprite = sprite
        super().__init__(sprite)
        match size:
            case "very_big": self.size_to = Size.VERY_BIG
            case "big": self.size_to = Size.BIG
            case "small": self.size_to = Size.SMALL
            case "very_small": self.size_to = Size.VERY_SMALL
            case _: raise Exception(f"excpected size (very_big,big,small,very_small) but received {size}")

    def resize_player(self,player:Player)->None:
        # Move the player to ensure that it doesn't hit the portal again
        if player.sprite.center_x > self.center_x : player.sprite.center_x = self.left - 100
        else: player.sprite.center_x = self.right + 100
        
        if self.__compare_values__(player):(gravity,scale,jump_speed,horizontal_speed) = Size.NORMAL.size_values()
        else: (gravity,scale,jump_speed,horizontal_speed) = self.size_to.size_values()

        player.gravity = gravity
        player.scale = scale
        player.jump_speed = jump_speed
        player.horizontal_speed = horizontal_speed

    def __compare_values__(self,player:Player)->bool:
        (gravity,scale,jump_speed,horizontal_speed) = self.size_to.size_values()
        gravity_ok = gravity == player.gravity
        scale_ok = scale == player.scale
        jump_ok = jump_speed == player.jump_speed
        horizontal_ok = horizontal_speed == player.horizontal_speed
        return gravity_ok and scale_ok and jump_ok and horizontal_ok