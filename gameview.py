import arcade
from map import Map
from monster import Monster
from monster import Slime
from monster import Bat
import weapon


PLAYER_MOVEMENT_SPEED = 7
# Lateral speed of the player, in pixels per frame.

PLAYER_GRAVITY = 1
# Gravity applied to the player, in pixels per frame.

PLAYER_JUMP_SPEED = 21
# Instant vertical speed for jumping, in pixels per frame.

DISTANCE_FROM_UPPER_CAM = 300   # Nombres
DISTANCE_FROM_LOWER_CAM = 200   # Bizzares
DISTANCE_FROM_RIGHT_CAM = 10    # A
DISTANCE_FROM_LEFT_CAM = 200    # Modifier
# Minimum distance between camera and player in all directions

WEAPON_INDEX_SWORD = 0
WEAPON_INDEX_BOW = 1
# Values associated with each weapon

SPRITE_SIZE = 64
# Size of each sprite for the map

class GameView(arcade.View):
    """Main in-game view."""

    player_sprite: arcade.Sprite
    player_weapon:weapon.Weapon
    player_sprite_list: arcade.SpriteList[arcade.Sprite]

    arrow_sprite_list: arcade.SpriteList[arcade.Sprite]
    arrow_list: list[weapon.Arrow]
    active_weapon: int
    displayed_weapon_sprite: arcade.Sprite

    camera: arcade.camera.Camera2D
    display_camera: arcade.camera.Camera2D
    display_sprite_list: arcade.SpriteList[arcade.Sprite]

    wall_sprite_list: arcade.SpriteList[arcade.Sprite]
    no_go_sprite_list: arcade.SpriteList[arcade.Sprite]
    coin_sprite_list: arcade.SpriteList[arcade.Sprite]
    ext_sprite_list: arcade.SpriteList[arcade.Sprite]

    monster_sprite_list: arcade.SpriteList[arcade.Sprite]
    monster_list: list[Monster]

    held_keys_list: list[int]
    physics_engine: arcade.PhysicsEnginePlatformer
    
    error_message:str
    text_error:arcade.Text

    score: int
    text_score:arcade.Text
    sound_dict: dict[str,arcade.Sound]
    game_map: Map


    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Setup our game
        self.setup()

    def setup(self) -> None:
        """Set up the game here."""

        self.choose_map("map2.txt")

        # Setup of cameras
        self.camera = arcade.camera.Camera2D()
        self.display_camera = arcade.camera.Camera2D()

        # Creates the list of pressed keys
        self.held_keys_list = []

        # Loads all sounds that should be played
        Coincollected = arcade.load_sound(":resources:sounds/coin1.wav")
        PlayerJumped = arcade.load_sound(":resources:sounds/jump1.wav")
        GameOver = arcade.load_sound(":resources:sounds/gameover1.wav")
        SlimeKilled = arcade.load_sound(":resources:sounds/hurt3.wav")
        BatKilled = arcade.load_sound(":resources:sounds/hurt2.wav") # Pas le meilleur son
        NextLevel = arcade.load_sound(":resources:sounds/upgrade1.wav")

        # 
        self.sound_dict = {}
        self.sound_dict["Coin"]=Coincollected
        self.sound_dict["Jump"]=PlayerJumped
        self.sound_dict["Game_Over"]=GameOver
        self.sound_dict["Slime killed"] = SlimeKilled
        self.sound_dict["Bat killed"] = BatKilled
        self.sound_dict["Next_level"]=NextLevel

        # 
        self.score = 0
        self.text_score = arcade.Text(f"coins : {self.score}",x=5,y=self.camera.height-30,color=arcade.color.RED_ORANGE,font_size=25)
        self.text_error = arcade.Text(self.error_message,x=150,y=self.camera.height/2,color=arcade.color.RED_DEVIL,font_size=50)
        # Defined the arrow list
        self.arrow_sprite_list = arcade.SpriteList(use_spatial_hash=True)
        self.arrow_list = []

        # 
        self.active_weapon = WEAPON_INDEX_SWORD
        self.displayed_weapon_sprite = arcade.Sprite("assets/kenney-voxel-items-png/sword_silver.png", center_x=35, center_y=self.camera.height - 65, scale=0.6)
        self.displayed_weapon_sprite.append_texture(arcade.load_texture("assets/kenney-voxel-items-png/bow.png"))

        self.display_sprite_list = arcade.SpriteList(use_spatial_hash=True)
        self.display_sprite_list.append(self.displayed_weapon_sprite)

    def choose_map(self, chosen_map:str)-> None:
        # Initialize the map
        self.game_map = Map()
        if self.game_map.ReadMap(chosen_map):
            # Sets no problem with the game
            self.error_message = ""
        else:
            self.error_message = "Something is wrong with the map"
            self.game_map = Map()
            self.game_map.ReadMap("debug_map.txt")
        self.Load_Map()

    def Load_Map(self)->None:
        # Creating player
        self.player_sprite=self.load_elements(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png","S")[0]
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        # Creating the list of walls
        self.wall_sprite_list = arcade.SpriteList(use_spatial_hash=True)
        # Creating of ground
        self.wall_sprite_list.extend(self.load_elements(":resources:images/tiles/grassMid.png","="))
        # Creating of box
        self.wall_sprite_list.extend(self.load_elements(":resources:images/tiles/boxCrate_double.png","x"))
        # Creating of platforms
        self.wall_sprite_list.extend(self.load_elements(":resources:images/tiles/grassHalf_mid.png","-"))
        
        # Creating the list of no_go
        self.no_go_sprite_list = arcade.SpriteList(use_spatial_hash=True)
        # Creating of lava
        self.no_go_sprite_list.extend(self.load_elements(":resources:images/tiles/lava.png","£"))

        # Creating of coins
        self.coin_sprite_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_sprite_list.extend(self.load_elements(":resources:images/items/coinGold.png","*"))

        # Creating of exit sign
        self.ext_sprite_list = arcade.SpriteList(use_spatial_hash=True)
        self.ext_sprite_list.extend(self.load_elements(":resources:images/tiles/signExit.png","E"))

        # Creating of Slime ant Bat :
        self.slime_sprite_list:arcade.SpriteList[arcade.Sprite] = arcade.SpriteList(use_spatial_hash=True)
        self.bat_sprite_list:arcade.SpriteList[arcade.Sprite] = arcade.SpriteList(use_spatial_hash=True)
        self.slime_sprite_list.extend(self.load_elements(":resources:images/enemies/slimeBlue.png","o"))
        self.bat_sprite_list.extend(self.load_elements("assets/kenney-extended-enemies-png/bat.png","v"))
        self.monster_sprite_list= arcade.SpriteList(use_spatial_hash=True)
        self.monster_list = []

        for slime in self.slime_sprite_list:
            self.monster_list.append(Slime(slime))
            slime.change_x= -1
            self.monster_sprite_list.append(slime)
        for bat in self.bat_sprite_list:
            self.monster_list.append(Bat(bat))
            self.monster_sprite_list.append(bat)

        # Creating movement physics and collisions
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.wall_sprite_list,
            gravity_constant=PLAYER_GRAVITY
        )

        # Disables multiple jumps
        self.physics_engine.disable_multi_jump(); 


    def load_elements(self, sprite:str,element:str) -> arcade.SpriteList[arcade.Sprite]:
        Position = self.game_map.FindElement(element)
        Sprite_List: arcade.SpriteList[arcade.Sprite]
        Sprite_List = arcade.SpriteList(use_spatial_hash=True)
        for Pos in Position:
            Sprite_List.append(arcade.Sprite(
                sprite,
                center_x= SPRITE_SIZE/2+Pos[1]*SPRITE_SIZE,
                center_y= SPRITE_SIZE/2+Pos[0]*SPRITE_SIZE,
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
                    arcade.play_sound(self.sound_dict["Jump"])
            case arcade.key.ESCAPE:
                # Restart the game
                self.setup()

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""
    
        # Remembers that the key has been released
        try:
            self.held_keys_list.remove(key)
        except:
            pass

        match key:
            case arcade.key.RIGHT | arcade.key.LEFT:
                # stop lateral movement
                self.player_sprite.change_x = 0

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """Called when the user presses a mouse button"""

        # Remembers that the mouse button being held
        self.held_keys_list.append(button)

        match button:
            case arcade.MOUSE_BUTTON_LEFT:
                # Aim the weapon
                match self.active_weapon:
                    case 0: # Case for the sword, using a global variable produces an error
                        self.player_weapon = weapon.Sword(self.player_sprite.position,self.camera,(x,y))
                        # check to kill monsters
                        Monster_Touched : list[arcade.Sprite]
                        Monster_Touched = arcade.check_for_collision_with_list(self.player_weapon.weapon_sprite, self.monster_sprite_list)
                        for slime in Monster_Touched:
                            arcade.play_sound(self.sound_dict["Slime killed"])
                            slime.kill()
                    case 1: # Case for the bow
                        self.player_weapon = weapon.Bow(self.player_sprite.position,self.camera,(x,y))
                        arrow = weapon.Arrow(self.player_sprite.position,self.camera,(x,y))
                        self.arrow_list.append(arrow)
                        self.arrow_sprite_list.append(arrow.weapon_sprite)
                
                self.player_sprite_list.append(self.player_weapon.weapon_sprite)

                

            case arcade.MOUSE_BUTTON_RIGHT:
                match self.active_weapon:
                    case 0: # Sword case, produces an error if the global variable is used
                        self.active_weapon = WEAPON_INDEX_BOW
                    case 1: # Bow case, produces an error if the global variable is used
                        self.active_weapon = WEAPON_INDEX_SWORD
                self.displayed_weapon_sprite.set_texture(self.active_weapon)
                            

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        """Calles when the user releases a mouse button"""

        # Remembers that the mouse button is released
        try:
            self.held_keys_list.remove(button)
        except:
            pass
        
        match button:
            case arcade.MOUSE_BUTTON_LEFT:
                try:
                    self.player_weapon.weapon_sprite.kill()
                    del self.player_weapon
                except:
                    pass


    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances", or "ticks".
        """

        # Refreshes pressed keys
        for key in self.held_keys_list:
            match key:
                case arcade.key.RIGHT:
                    # start moving to the right
                    self.player_sprite.change_x = +PLAYER_MOVEMENT_SPEED
                case arcade.key.LEFT:
                    # start moving to the left
                    self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

        self.physics_engine.update()

        # Find the distance to each edge and move the camera if necessary
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

        # Move the weapon around
        try: 
            self.player_weapon.move(self.player_sprite.position)
        except:
            pass

        # move the arrows
        for arrow in self.arrow_list:
            arrow.move((0,0),wall = self.wall_sprite_list,no_go =self.no_go_sprite_list)
            try:
                for enemy in arcade.check_for_collision_with_list(arrow.weapon_sprite,self.monster_sprite_list):
                    enemy.kill()
                    arrow.weapon_sprite.kill()
                    del arrow
            except:
                pass

        # Check for collisions with coins
        Coins_Touched_List : list[arcade.Sprite]
        Coins_Touched_List = arcade.check_for_collision_with_list(self.player_sprite, self.coin_sprite_list)

        # Remove touched coins and play the sound
        for coin in Coins_Touched_List:
            self.score += 1
            self.text_score.text = f"coins : {self.score}"
            arcade.play_sound(self.sound_dict["Coin"])
            coin.remove_from_sprite_lists()

        # Check if collision with no_go (Lava)
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.no_go_sprite_list)) != 0:
            arcade.play_sound(self.sound_dict["Game_Over"])
            self.setup()

        # Check for end of level
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.ext_sprite_list)) != 0:
            arcade.play_sound(self.sound_dict["Next_level"])
            # Check if there is a next map
            if "next-map" in self.game_map.MapConfig:
                self.choose_map(self.game_map.MapConfig["next-map"])
            else:
                # Intended : if there is no next map, the player is moved forward, used for debugging purposes
                self.player_sprite.position = (self.player_sprite.position[0]+100,self.player_sprite.position[1])

        # Move the monsters
        for monster in self.monster_list:
            if(monster.monster_sprite in self.monster_sprite_list):
                monster.move(self.wall_sprite_list)
            else:
                self.monster_list.remove(monster)
                del monster

        # Check for collisions with slime
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.monster_sprite_list)) != 0:
            arcade.play_sound(self.sound_dict["Game_Over"])
            self.setup()

    def on_draw(self) -> None:
        """Render the screen."""
        self.clear() # always start with self.clear()

        # Displays items on screen
        with self.camera.activate():
            self.player_sprite_list.draw()
            self.wall_sprite_list.draw()
            self.no_go_sprite_list.draw()
            self.coin_sprite_list.draw()
            self.ext_sprite_list.draw()
            self.monster_sprite_list.draw()
            self.arrow_sprite_list.draw()
            # Affiche les hitbox si on appuie sur H
            if arcade.key.H in self.held_keys_list:
                self.player_sprite_list.draw_hit_boxes()
                self.wall_sprite_list.draw_hit_boxes()
                self.no_go_sprite_list.draw_hit_boxes()
                self.coin_sprite_list.draw_hit_boxes()
                self.ext_sprite_list.draw_hit_boxes()
                self.monster_sprite_list.draw_hit_boxes()
                self.arrow_sprite_list.draw_hit_boxes()

        with self.display_camera.activate():
            self.text_score.draw()
            self.display_sprite_list.draw()
            self.text_error.draw()
    