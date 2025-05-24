from arcade import Sprite, SpriteList, SpriteSequence
from weapon import Weapon, Weapon_index
from weapon import Sword, Bow, Arrow
import arcade

from common_types import pos_float_int

TRUE_SCALE = 0.5 # Reference for the scale

class Player:
    """
    class used to hold everything that is linked directly to the player

    Some arguments are used by this class to move the player, such as ``jump_speed``, `horizontal_speed`, and so on

    Note that this class has a `draw`  method that can be used to display the player and their weapons
    The sprites that have to be drawn this way are all stored in `__sprites_to_draw` which should not 
    have to be interracted with in any way

    list of attributes

    ``active_weapon`` type (`Weapon`) : does not have to be referenced outside in anyways, the weapon is toggled by `toggle_weapon` so it switches between `Sword` and `Bow` types

    `scale` type (`float`) : used to scale everything (mainly the Weapons) to the size of the player

    `gravity` type (`float`) : storing the gravity assigned to a ``Player`` object, not used in this classshould be used with ``arcade``'s `PhysicsEngine`

    `jump_speed` type (`float`) : used to set the vertical speed upon using the `jump` method

    `horizontal_speed` type (`float`) : used to set the horizontal_speed upon using the 'move_right' or `move_left` method

    required files
        `weapon.py`
        `common_types.py`

    required librabry
        `arcade`
    """
    __sprite:Sprite
    __sprites_to_draw:SpriteList[Sprite]

    __scale:float

    active_weapon:Weapon_index
    __weapon:Weapon
    __arrow_list:list[Arrow]

    gravity:float
    jump_speed:float
    horizontal_speed:float

    score:int

    def __init__(self,scale:float=1,active_weapon:Weapon_index=Weapon_index.SWORD,
                 gravity:float=1,jump_speed:float=20,horizontal_speed:float=6,score:int=0)->None:
        self.__scale = scale
        self.active_weapon = active_weapon
        self.gravity = gravity
        self.jump_speed = jump_speed
        self.horizontal_speed = horizontal_speed
        self.score = score
        self.__sprites_to_draw = SpriteList(use_spatial_hash=True)
        self.__arrow_list = []

    @property
    def scale(self)->float:
        return self.__scale
    
    @scale.setter
    def scale(self,scale:float)->None:
        """
        Makes sure to scale the size of the sprite at the same time as the size of the player
        """
        self.__scale = scale
        if hasattr(self,'sprite'):self.__sprite.scale = (scale*TRUE_SCALE,scale*TRUE_SCALE)

    @property
    def sprite(self)->Sprite:
        return self.__sprite
    
    @sprite.setter
    def sprite(self,sprite:Sprite)->None:
        """
        Assigns the sprite scale it and prepare it for display
        """
        self.__sprite = sprite
        self.__sprite.scale = (self.__scale*TRUE_SCALE,self.__scale*TRUE_SCALE)
        self.__sprites_to_draw.append(sprite)

    def jump(self)->None:
        """
        set the vertical speed to `jump_speed`
        """
        self.__sprite.change_y = self.jump_speed

    def horizontal_stop(self)->None:
        """
        set the horizontal speed to 0
        """
        self.__sprite.change_x = 0

    def move_right(self)->None:
        """
        set the horizontal speed to `horizontal_speed`
        """
        self.__sprite.change_x = self.horizontal_speed

    def move_left(self)->None:
        """
        set the horizontal speed to -`horizontal_speed`
        """
        self.__sprite.change_x = -self.horizontal_speed

    def create_weapon(self,relative_aim:pos_float_int)->None:
        """
        creates the weapon assigned to `current_weapon`

        if the weapon is `WEAPON_INDEX.Bow` then an arrow is shot automatically
        """
        match self.active_weapon:
            case Weapon_index.SWORD:self.__weapon = Sword(self.__sprite.position,relative_aim,scale=self.__scale)
            case Weapon_index.BOW:
                self.__weapon = Bow(self.__sprite.position,relative_aim,scale=self.__scale)
                self.__shoot_arrow(Arrow(self.__sprite.position,relative_aim,scale=self.__scale))
        
        self.__weapon.move(self.__sprite.position) # move the weapon to make sure it's in the right place
        self.__sprites_to_draw.append(self.__weapon)

    def move_weapon(self)->None:
        """
        Moves the `Weapon` (`Bow` or `Sword`) if it exists and moves every `Arrow` 

        this method should be called every time the player moves but it is up to the user to decide 

        Please refer to `Weapon.move` for any insight on the movement of the weapons

        Note : any arrow that has a negative y coordinate is automatically deleted
        """
        # check if the weapon exists before moving it
        if hasattr(self,'_Player__weapon') : self.__weapon.move(position=self.__sprite.position)

        for arrow in self.__arrow_list:
            arrow.move()
            if arrow.position[1]< 0: self.__remove_arrow__(arrow)

    def remove_weapon(self)->None:
        """
        Removes the `Weapon` (`Bow` or `Sword`) if it exists
        """
        if hasattr(self,'_Player__weapon') : 
            self.__weapon.kill()
            del self.__weapon

    def weapon_hit[SubSprite:Sprite](self,collision_with:SpriteSequence[SubSprite])->list[SubSprite]:
        """
        Returns the list of `SubSprite` in `collision_with` that touch the weapon of the player where
        `SubSprite` is a subclass of `Sprite`

        Warning ! This method also works even if `weapon` is a `Bow` type of `Weapon` which may not be
        a wanted result
        """
        return arcade.check_for_collision_with_list(self.__weapon,collision_with)

    def arrows_hit[SubSprite:Sprite](self,collision_with:SpriteSequence[SubSprite])->list[SubSprite]:
        """
        Returns the list of `SubSprite` in `collision_with` that touch any `Arrow` object shot by the player where
        `SubSprite` is a subclass of `Sprite`

        This also deletes any arrow that hit anything
        """
        total_hits:list[SubSprite] = []
        for arrow in self.__arrow_list:
            arrow_hits = arcade.check_for_collision_with_list(arrow,collision_with)
            if len(arrow_hits) > 0: self.__remove_arrow__(arrow) # check if the arrow hit anything
            total_hits.extend(arrow_hits)  
        return total_hits

    def __remove_arrow__(self,arrow:Arrow)->None:
        """
        Safely removes any arrow from the `__arrow_list` 
        """
        if arrow in self.__arrow_list: self.__arrow_list.remove(arrow)
        arrow.kill()

    def __shoot_arrow(self,arrow:Arrow)->None:
        """
        Spawns an arrow at the `Player` position so that it follows a parabollic trajectory
        """
        self.__arrow_list.append(arrow)
        self.__sprites_to_draw.append(arrow)

    def toggle_weapon(self)->None:
        """
        Toggles which ``Weapon`` will be spawned upon using `create_weapon` 
        """
        match self.active_weapon:
            case Weapon_index.SWORD: self.active_weapon = Weapon_index.BOW # Switch to the bow
            case Weapon_index.BOW: self.active_weapon = Weapon_index.SWORD # Swicth to the sword

    def draw(self)->None:
        """
        Draws every sprite associated to the player, this includes 
            The sprite of the player itself
            The sprite of the held weapon if it exists
            The sprite of any arrow that may be flying
        """
        self.__sprites_to_draw.draw()