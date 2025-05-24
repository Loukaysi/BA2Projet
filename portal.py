from arcade import Sprite
from player import Player
from enum import Enum,auto
from subsprite import SubSprite

size_values = tuple[float, float, float, float] # In order : gravity / size / jump_speed / horizontal_speed

class Size(Enum):
    """
    Smaller class used to differentiate the different sizes to which the portal can scale the player

    It only has one method `size_values` which is used to choose how the attributes of the player will be modified based on the size 

    This class should not have to be used outside of this file, it is only used by the class `Portal`
    """
    VERY_BIG=auto()
    BIG=auto()
    NORMAL=auto()
    SMALL=auto()
    VERY_SMALL=auto()

    def size_values(self)->size_values:
        match self: 
            # Handpicked values, not meant to represent anything
            # In order : gravity / size / jump_speed / horizontal_speed
            # And of course as we all know, falling speed is directly proportiannal to mass...
            case Size.VERY_BIG:return(0.5,2,18,4)
            case Size.BIG:return(0.75,1.5,18,5)
            case Size.NORMAL:return(1,1,20,6)
            case Size.SMALL:return(0.4,0.75,9,8)
            case Size.VERY_SMALL:return(0.3,0.5,7,10)
            case _: raise Exception("Error with the Size class, should not happen")


class Portal(SubSprite):
    """
    Class used to handle the portals which scale the player and his attributes

    There are 4 different sizes available : very_big, big, small, very_small

    The size of the player will go back to normal if they go through the a similar portal (i.e. if he his big and goes through a big portal, he will go back to normal)

    Note : The actual sprite is not handled by this class, should any sprite be different (for example a different color for each size) it should be handled outside of this class

    list of attributes

        `size_to` type ('Size') : used to know which size the player should be scales to    
    
    required files
        `player.py`
        `subsprite.py`

    required librabry
        `arcade`
        `enum`
    """
    size_to:Size

    def __init__(self,sprite:Sprite,size:str)->None:
        """
        Sets the portal size to 4 different possibilities

        Note : the size is passed as a string which as to be one of the following 

            `very_big`, `big`, `small` or `very_small`
        
        If the given ``str`` is not one of those 4 values, this method will raise an `Exception`
        """
        self.sprite = sprite
        super().__init__(sprite)
        match size:
            case "very_big": self.size_to = Size.VERY_BIG
            case "big": self.size_to = Size.BIG
            case "small": self.size_to = Size.SMALL
            case "very_small": self.size_to = Size.VERY_SMALL
            case _: raise Exception(f"excpected size (very_big,big,small,very_small) but received {size}")

    def resize_player(self,player:Player)->None:
        """
        This method should be called whenever there is a collision between a `Player` and a portal to handle size modification

        To know which size it should scale the player to, this method compares the attributes of the player to the ones it would be set to, if the
        arguments match, the player will be set back to "normal" size  

        Note : The player will first be moved to the right or the left based of which side they "entered" from to ensure that they don't hit the portal twice
        """
        # Move the player to ensure that it doesn't hit the portal again (100 is based on observation)
        if player.sprite.center_x > self.center_x : player.sprite.center_x = self.left - 100
        else: player.sprite.center_x = self.right + 100
        
        # Test if we should make the player a different size or normal
        if self.__compare_values__(player):self.__size_player__(player,Size.NORMAL)
        else: self.__size_player__(player,self.size_to)

    def __size_player__(self,player:Player,size:Size)->None:
        """
        Size the ``Player`` to the given `Size`

        Note : this method "can" be used outside of this class but it is advised to use `resize_player` instead as this method alone does not 
        handle the player touching the `Portal` multiple times OR the fact that the player should be sized back to normal
        """
        (gravity,scale,jump_speed,horizontal_speed) = size.size_values()
        player.gravity = gravity
        player.scale = scale
        player.jump_speed = jump_speed
        player.horizontal_speed = horizontal_speed

    def __compare_values__(self,player:Player)->bool:
        """
        Used to find if the player is already scaled to the size the `Portal` would have set them to

        It can be used outside of this class but note that is already being handled in `resize_player`
        """
        (gravity,scale,jump_speed,horizontal_speed) = self.size_to.size_values()
        gravity_ok = gravity == player.gravity
        scale_ok = scale == player.scale
        jump_ok = jump_speed == player.jump_speed
        horizontal_ok = horizontal_speed == player.horizontal_speed
        return gravity_ok and scale_ok and jump_ok and horizontal_ok