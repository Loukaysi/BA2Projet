import arcade

PLAYER_MOVEMENT_SPEED = 5
"""Lateral speed of the player, in pixels per frame."""

PLAYER_GRAVITY = 1
"""Gravity applied to the player, in pixels per frame."""

PLAYER_JUMP_SPEED = 18
"""Instant vertical speed for jumping, in pixels per frame."""

class GameView(arcade.View):
    """Main in-game view."""

    player_sprite: arcade.Sprite
    player_sprite_list: arcade.SpriteList[arcade.Sprite]
    wall_list: arcade.SpriteList[arcade.Sprite]
    coin_list: arcade.SpriteList[arcade.Sprite]
    physics_engine: arcade.PhysicsEnginePlatformer
    camera: arcade.camera.Camera2D
    held_keys_list: list[int]

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

        # Setup de la caméra
        self.camera = arcade.camera.Camera2D()

        # Créé la liste des touches appuyées vide
        self.held_keys_list = []

        
    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""

        # Retient que la touche a été pressée
        self.held_keys_list.append(key)

        match key:
            case arcade.key.UP:
                # jump by giving an initial vertical speed
                self.player_sprite.change_y = PLAYER_JUMP_SPEED  
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
            case arcade.key.H:
                # Désactive les Hitbox
                self.hitbox_on = False

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

        Coins_Touched_List : list[arcade.Sprite]

        self.physics_engine.update()

        # Gère le déplacement de la caméra :
        if self.player_sprite.position[0] - self.camera.position.x > 500:
            self.camera.position += (PLAYER_MOVEMENT_SPEED,0)
        elif self.player_sprite.position[0] - self.camera.position.x < -500:
            self.camera.position -= (PLAYER_MOVEMENT_SPEED,0)
        if self.player_sprite.position[1] - self.camera.position.y > 300:
            self.camera.position += (0,PLAYER_MOVEMENT_SPEED)
        elif self.player_sprite.position[1] - self.camera.position.y < -300:
            self.camera.position -= (0,PLAYER_MOVEMENT_SPEED)

        print(self.player_sprite.position[0] - self.camera.position.x)
        # Waiting for a new version of mypy with https://github.com/python/mypy/pull/18510
        #self.camera.position = self.player_sprite.position # type: ignore

        # Check for collisions with coins
        Coins_Touched_List = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Remove touched coins
        for coin in Coins_Touched_List:
            coin.remove_from_sprite_lists()


    def on_draw(self) -> None:
        """Render the screen."""
        self.clear() # always start with self.clear()

        # Affiche les éléments de à l'écran
        with self.camera.activate():
            self.player_sprite_list.draw()
            self.wall_list.draw()
            self.coin_list.draw()

            # Affiche les hitbox si on appuie sur H
            if arcade.key.H in self.held_keys_list:
                self.player_sprite_list.draw_hit_boxes()
                self.wall_list.draw_hit_boxes()
                self.coin_list.draw_hit_boxes()