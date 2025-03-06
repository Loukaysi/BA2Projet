import arcade
from map import Map
from slime import Slime

PLAYER_MOVEMENT_SPEED = 5
#Lateral speed of the player, in pixels per frame.

PLAYER_GRAVITY = 1
#Gravity applied to the player, in pixels per frame.

PLAYER_JUMP_SPEED = 18
#Instant vertical speed for jumping, in pixels per frame.

DISTANCE_FROM_UPPER_CAM = 300
DISTANCE_FROM_LOWER_CAM = 200
DISTANCE_FROM_RIGHT_CAM = 550
DISTANCE_FROM_LEFT_CAM = 550
#Minimum distance between camera and player in all directions

SPRITE_SIZE = 64
#Size of each sprite for the map

class GameView(arcade.View):
    """Main in-game view."""

    player_sprite: arcade.Sprite
    player_sprite_list: arcade.SpriteList[arcade.Sprite]
    wall_list: arcade.SpriteList[arcade.Sprite]
    coin_list: arcade.SpriteList[arcade.Sprite]
    slime_list: arcade.SpriteList[arcade.Sprite]
    slime_moves: list[Slime]
    physics_engine: arcade.PhysicsEnginePlatformer
    camera: arcade.camera.Camera2D
    held_keys_list: list[int]
    Sounds: dict
    GameMap: Map

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Setup our game
        self.setup()

    def setup(self) -> None:
        """Set up the game here."""

        # Initialize the map
        self.GameMap = Map()
        self.GameMap.ReadMap("map/map1.txt")

        # Creating player
        self.player_sprite=self.load_elements(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png","S")[0]
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        # Creating the list of walls
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        # Creating of ground
        self.wall_list.extend(self.load_elements(":resources:images/tiles/grassMid.png","="))
        # Creating of box
        self.wall_list.extend(self.load_elements(":resources:images/tiles/boxCrate_double.png","x"))
        # Creation of platforms
        self.wall_list.extend(self.load_elements(":resources:images/tiles/grassHalf_mid.png","-"))
        
        # Creation of coins
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list.extend(self.load_elements(":resources:images/items/coinGold.png","*"))

        # Creation of enemies
        self.slime_list = arcade.SpriteList(use_spatial_hash=True)
        self.slime_list.extend(self.load_elements(":resources:/images/enemies/slimeBlue.png","o"))
        self.slime_moves = []
        for slime in self.slime_list:
            self.slime_moves.append(Slime(slime,1))
            slime.velocity = (1,0)


        # Creating movement physics and collisions
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.wall_list,
            gravity_constant=PLAYER_GRAVITY
        )

        # Disables multiple jumps
        self.physics_engine.disable_multi_jump(); 

        # Setup of camera
        self.camera = arcade.camera.Camera2D()

        # Centers the camera on the player
        # Waiting for a new version of mypy with https://github.com/python/mypy/pull/18510
        # self.camera.position = self.player_sprite.position # type: ignore

        # Creates the list of pressed keys
        self.held_keys_list = []

        # Loads all sounds that should be played
        Coincollected = arcade.load_sound(":resources:sounds/coin1.wav")
        PlayerJumped = arcade.load_sound(":resources:sounds/jump1.wav")

        self.Sounds = {}
        self.Sounds["Coin"]=Coincollected
        self.Sounds["Jump"]=PlayerJumped

    def load_elements(self, sprite:str,element:str) -> arcade.SpriteList:
        Position = self.GameMap.FindElement(element)
        Sprite_List: arcade.SpriteList
        Sprite_List = arcade.SpriteList(use_spatial_hash=True)
        for Pos in Position:
            Sprite_List.append(arcade.Sprite(
                sprite,
                center_x= 32+Pos[1]*64,
                center_y= 32+Pos[0]*64,
                scale= 0.5
            ))
        return Sprite_List
        
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""

        # Remembers that the key was pressed
        self.held_keys_list.append(key)

        match key:
            case arcade.key.UP:
                # Checks that the player can jump
                if self.physics_engine.can_jump():
                    # jump by giving an initial vertical speed
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED  
                    arcade.play_sound(self.Sounds["Jump"])
            case arcade.key.ESCAPE:
                # Restart the game
                self.setup()


    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""
    
        # Remembers that the key has been released
        self.held_keys_list.remove(key)

        match key:
            case arcade.key.RIGHT | arcade.key.LEFT:
                # stop lateral movement
                self.player_sprite.change_x = 0

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances", or "ticks".
        """

        # Actualise les touches pressée
        for key in self.held_keys_list:
            match key:
                case arcade.key.RIGHT:
                    # start moving to the right
                    self.player_sprite.change_x = +PLAYER_MOVEMENT_SPEED
                case arcade.key.LEFT:
                    # start moving to the left
                    self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

        self.physics_engine.update()

        # Trouve la distance à chaque bord et déplace la caméra si besoin :
        x = self.player_sprite.position[0] - self.camera.position.x
        y = self.player_sprite.position[1] - self.camera.position.y
        if x > DISTANCE_FROM_RIGHT_CAM:
            self.camera.position += (x-DISTANCE_FROM_RIGHT_CAM,0)
        elif x < -DISTANCE_FROM_LEFT_CAM:
            self.camera.position += (x+DISTANCE_FROM_LEFT_CAM,0)
        if y > DISTANCE_FROM_UPPER_CAM:
            self.camera.position += (0,y-DISTANCE_FROM_UPPER_CAM)
        elif y < -DISTANCE_FROM_LOWER_CAM:
            self.camera.position += (0,y+DISTANCE_FROM_LOWER_CAM)

        # Check for collisions with coins
        Coins_Touched_List : list[arcade.Sprite]
        Coins_Touched_List = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Remove touched coins and play the sound
        for coin in Coins_Touched_List:
            arcade.play_sound(self.Sounds["Coin"])
            coin.remove_from_sprite_lists()
        
        # Move the slimes

        for slime in self.slime_moves:
            # Check if the slime encountered a wall and if so, change his speed
            if len(arcade.check_for_collision_with_list(slime.Sprite, self.wall_list)) != 0:
                slime.Collision()
            slime.Move()

        # Check for collisions with slimes
        Slimes_Touched_List : list[arcade.Sprite]
        Slimes_Touched_List = arcade.check_for_collision_with_list(self.player_sprite, self.slime_list)

        if len(Slimes_Touched_List) != 0:
            self.setup()


    def on_draw(self) -> None:
        """Render the screen."""
        self.clear() # always start with self.clear()

        # Affiche les éléments à l'écran
        with self.camera.activate():
            self.player_sprite_list.draw()
            self.wall_list.draw()
            self.coin_list.draw()
            self.slime_list.draw()
            # Affiche les hitbox si on appuie sur H
            if arcade.key.H in self.held_keys_list:
                self.player_sprite_list.draw_hit_boxes()
                self.wall_list.draw_hit_boxes()
                self.coin_list.draw_hit_boxes()
                self.slime_list.draw_hit_boxes()
    