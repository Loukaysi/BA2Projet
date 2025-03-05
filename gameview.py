import arcade

PLAYER_MOVEMENT_SPEED = 5
"""Lateral speed of the player, in pixels per frame."""

PLAYER_GRAVITY = 1
"""Gravity applied to the player, in pixels per frame."""

PLAYER_JUMP_SPEED = 18
"""Instant vertical speed for jumping, in pixels per frame."""

DISTANCE_FROM_UPPER_CAM = 300
DISTANCE_FROM_LOWER_CAM = 200
DISTANCE_FROM_RIGHT_CAM = 550
DISTANCE_FROM_LEFT_CAM = 550
"""Distance minimiale entre la caméra et le joueur dans toutes les directions"""

class GameView(arcade.View):
    """Main in-game view."""

    player_sprite: arcade.Sprite
    player_sprite_list: arcade.SpriteList[arcade.Sprite]
    wall_list: arcade.SpriteList[arcade.Sprite]
    coin_list: arcade.SpriteList[arcade.Sprite]
    physics_engine: arcade.PhysicsEnginePlatformer
    camera: arcade.camera.Camera2D
    held_keys_list: list[int]
    Sounds: dict

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Setup our game
        self.setup()

    def setup(self) -> None:
        """Set up the game here."""

        # Création du joueur
        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
            center_x=64,
            center_y=128
        )
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        # Création du sol
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        for i in range (0,1250-63,64):
            self.wall_list.append(arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                center_x=i,
                center_y=32,
                scale=0.5,
                )  
            )
        
        # Création des boîtes
        for i in range (256,769,256):
            self.wall_list.append(arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png",
                center_x=i,
                center_y=96,
                scale=0.5,
                )  
            )

        # Création des pièces
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        for i in range (128,1251,256):
            self.coin_list.append(arcade.Sprite(
                ":resources:images/items/coinGold.png",
                center_x=i,
                center_y=96,
                scale=0.5,
                )  
            )

        # Création de la physique de déplacement et des collisions
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.wall_list,
            gravity_constant=PLAYER_GRAVITY
        )

        # Désactive les saut multiples
        self.physics_engine.disable_multi_jump(); 

        # Setup de la caméra
        self.camera = arcade.camera.Camera2D()

        # Centre la caméra sur le joueur
        # Waiting for a new version of mypy with https://github.com/python/mypy/pull/18510
        # self.camera.position = self.player_sprite.position # type: ignore

        # Créé la liste des touches appuyées
        self.held_keys_list = []

        #Charge tous les sons qui devront être joués
        Coincollected = arcade.load_sound(":resources:sounds/coin1.wav")
        PlayerJumped = arcade.load_sound(":resources:sounds/jump1.wav")

        self.Sounds = {}
        self.Sounds["Coin"]=Coincollected
        self.Sounds["Jump"]=PlayerJumped

        
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""

        # Retient que la touche a été pressée
        self.held_keys_list.append(key)

        match key:
            case arcade.key.UP:
                # Vérifie que le joueur peut sauter
                if self.physics_engine.can_jump():
                    # jump by giving an initial vertical speed
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED  
                    arcade.play_sound(self.Sounds["Jump"])
            case arcade.key.ESCAPE:
                # Restart the game
                self.setup()


    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""
    
        # Retient que la touche a été relâchée
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
        print(self.camera.viewport_right)
        print(self.camera.viewport_left)
        print(self.camera.viewport_width)
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


    def on_draw(self) -> None:
        """Render the screen."""
        self.clear() # always start with self.clear()

        # Affiche les éléments à l'écran
        with self.camera.activate():
            self.player_sprite_list.draw()
            self.wall_list.draw()
            self.coin_list.draw()
            # Affiche les hitbox si on appuie sur H
            if arcade.key.H in self.held_keys_list:
                self.player_sprite_list.draw_hit_boxes()
                self.wall_list.draw_hit_boxes()
                self.coin_list.draw_hit_boxes()