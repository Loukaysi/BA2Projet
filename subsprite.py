from arcade import Sprite

class SubSprite(Sprite):
    def __init__(self,sprite:Sprite)->None:
        super().__init__(sprite.texture)
        self.scale = sprite.scale
        self.center_x = sprite.center_x
        self.center_y = sprite.center_y
        self.change_x = sprite.change_x
        self.change_y = sprite.change_y
        self.boundary_left = sprite.boundary_left
        self.boundary_right = sprite.boundary_right
        self.boundary_top = sprite.boundary_top
        self.boundary_bottom = sprite.boundary_bottom
        self.textures = sprite.textures
