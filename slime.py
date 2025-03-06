import arcade

class Slime():
    Speed:float
    Sprite:arcade.Sprite

    def __init__(self,sprite:arcade.Sprite, speed:float):
        self.speed = speed
        self.Sprite = sprite
    
    def Collision(self) -> None:
        self.speed = -self.speed

    def Move(self) -> None:
        self.Sprite.position = (self.Sprite.position[0] + self.speed, self.Sprite.position[1])