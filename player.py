from arcade import Sprite, SpriteList, SpriteSequence
from weapon import Weapon, Weapon_index
from weapon import Sword, Bow, Arrow
import arcade

TRUE_SCALE = 0.5

class Player:
    sprite:Sprite
    scale:float

    active_weapon:Weapon_index
    weapon:Weapon
    arrow_list:list[Arrow]

    sprites_to_draw:SpriteList[Sprite]

    gravity:float
    jump_speed:float
    horizontal_speed:float

    score:int

    def __init__(self,scale:float=1,active_weapon:Weapon_index=Weapon_index.SWORD,
                 gravity:float=1,jump_speed:float=20,horizontal_speed:float=5,score:int=0)->None:
        self.scale = scale
        self.active_weapon = active_weapon
        self.gravity = gravity
        self.jump_speed = jump_speed
        self.horizontal_speed = horizontal_speed
        self.score = score
        self.sprites_to_draw = SpriteList(use_spatial_hash=True)
        self.arrow_list = []

    def jump(self)->None:
        self.sprite.change_y = self.jump_speed

    def horizontal_stop(self)->None:
        self.sprite.change_x = 0

    def move_right(self)->None:
        self.sprite.change_x = self.horizontal_speed

    def move_left(self)->None:
        self.sprite.change_x = -self.horizontal_speed

    def create_weapon(self,relative_aim:tuple[float|int,float|int])->None:
        match self.active_weapon:
            case Weapon_index.SWORD:self.weapon = Sword(self.sprite.position,relative_aim,scale=self.scale)
            case Weapon_index.BOW:
                self.weapon = Bow(self.sprite.position,relative_aim,scale=self.scale)
                self.shoot_arrow(Arrow(self.sprite.position,relative_aim,scale=self.scale))
        self.sprites_to_draw.append(self.weapon)

    def move_weapon(self)->None:
        if hasattr(self,'weapon') : self.weapon.move(position=self.sprite.position)

        for arrow in self.arrow_list:
            arrow.move()
            if arrow.position[1]< 0: self.__remove_arrow__(arrow)

    def arrows_hit(self,collision_with:SpriteSequence[Sprite])->list[Sprite]:
        total_hits:list[Sprite] = []
        for arrow in self.arrow_list:
            arrow_hits = arcade.check_for_collision_with_list(arrow,collision_with)
            if len(arrow_hits) > 0: self.__remove_arrow__(arrow)
            total_hits.extend(arrow_hits)  
        return total_hits

    def __remove_arrow__(self,arrow:Arrow)->None:
        if arrow in self.arrow_list: self.arrow_list.remove(arrow)
        arrow.kill()

    def shoot_arrow(self,arrow:Arrow)->None:
        self.arrow_list.append(arrow)
        self.sprites_to_draw.append(arrow)

    def toggle_weapon(self)->None:
        match self.active_weapon:
            case Weapon_index.SWORD: self.active_weapon = Weapon_index.BOW # Switch to the bow
            case Weapon_index.BOW: self.active_weapon = Weapon_index.SWORD # Swicth to the sword

    def assign_sprite(self,sprite:Sprite)->None:
        self.sprite = sprite
        self.sprite.scale = (self.scale*TRUE_SCALE,self.scale*TRUE_SCALE)
        self.sprites_to_draw.append(sprite)

    def draw(self)->None:
        self.sprites_to_draw.draw()

