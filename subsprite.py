from arcade import Sprite

class SubSprite(Sprite):
    """
    Subclass of Sprite to avoid the "sub object of an object cannot be transformed into sub object" problem

    I.e. this class should only be used for the `init` method which takes a sprite and creates an exact copy of the sprite to then be extended to have more attributes

    
    required librabry
        `arcade`
    """
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
