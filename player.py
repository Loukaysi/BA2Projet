import arcade
from arcade import Sprite, SpriteList
from weapon import Weapon, Weapon_index
from weapon import Sword, Bow, Arrow

class Player:
    sprite:Sprite
    scale:float

    active_weapon:Weapon_index
    weapon:Weapon
    arrow_list:list[Arrow]

    arrow_sprite_list:SpriteList[Sprite]
    weapon_sprite_list:SpriteList[Sprite]
    sprites_to_draw:SpriteList[Sprite]

    gravity:float
    jump_speed:float
    horizontal_speed:float

    score:int

    def __init__(self,scale:float=1,active_weapon:Weapon_index=Weapon_index.SWORD,
                 gravity:float=1,jump_speed:float=21,horizontal_speed:float=5,score:int=0)->None:
        self.scale = scale
        self.active_weapon = active_weapon
        self. gravity = gravity
        self.jump_speed = jump_speed
        self.horizontal_speed = horizontal_speed
        self.score = score
        self.weapon_sprite_list = SpriteList(use_spatial_hash=True)
        self.sprites_to_draw = SpriteList(use_spatial_hash=True)
        self.arrow_sprite_list = SpriteList(use_spatial_hash=True)
        self.arrow_list = []

    def jump(self)->None:
        self.sprite.change_y = self.jump_speed

    def horizontal_stop(self)->None:
        self.sprite.change_x = 0

    def move_right(self)->None:
        self.sprite.change_x = self.horizontal_speed

    def move_left(self)->None:
        self.sprite.change_x = -self.horizontal_speed

    def move_weapon(self)->None:
        try:
            self.weapon.move()
        except:
            pass

        for arrow in self.arrow_list:
            arrow.move()

    def weapon_hit(self,collision_with:SpriteList[Sprite])->SpriteList:
        return arcade.check_for_collision_with_list

    def shoot_arrow(self,arrow:Arrow)->None:
        self.arrow_list.append(arrow)
        self.arrow_sprite_list.append(arrow.weapon_sprite)

    def toggle_weapon(self)->None:
        match self.active_weapon:
            case Weapon_index.SWORD:
                self.active_weapon = Weapon_index.BOW # Switch to the bow
            case Weapon_index.BOW:
                self.active_weapon = Weapon_index.SWORD # Swicth to the sword

    def cheat(self)->None:
        self.sprites_to_draw.append(self.sprite)

    def draw(self)->None:
        self.sprites_to_draw.draw()

