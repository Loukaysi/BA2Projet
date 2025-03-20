import arcade
import arcade.sprite
from map import Map
from monster import Slime
from monster import Bat
import math

PLAYER_MOVEMENT_SPEED = 7
# Lateral speed of the player, in pixels per frame.

PLAYER_GRAVITY = 1
# Gravity applied to the player, in pixels per frame.

PLAYER_JUMP_SPEED = 21
# Instant vertical speed for jumping, in pixels per frame.

ARROW_BASE_SPEED = 20
ARROW_GRAVITY = 5
# Constants for the arrow's trajectory

DISTANCE_FROM_UPPER_CAM = 300
DISTANCE_FROM_LOWER_CAM = 200
DISTANCE_FROM_RIGHT_CAM = 550
DISTANCE_FROM_LEFT_CAM = 550
# Minimum distance between camera and player in all directions

WEAPON_INDEX_SWORD = 0
WEAPON_INDEX_BOW = 1
# Values associated with each weapon

WEAPON_OFFSET_INDEX_X = 0
WEAPON_OFFSET_INDEX_Y = 1
WEAPON_OFFSET_INDEX_ANGLE = 2
WEAPON_OFFSET_INDEX_SPRITE_ANGLE = 3
# Index for the adjustements of the sprites

SPRITE_SIZE = 64
# Size of each sprite for the map

class GameView(arcade.View):
    """Main in-game view."""

    player_sprite: arcade.Sprite
    weapon_sprite: arcade.Sprite
    weapon_display_offsets: dict
    arrow_sprite_list: arcade.SpriteList[arcade.Sprite]
    player_sprite_list: arcade.SpriteList[arcade.Sprite]
    wall_list: arcade.SpriteList[arcade.Sprite]
    no_go_list: arcade.SpriteList[arcade.Sprite]
    coin_list: arcade.SpriteList[arcade.Sprite]
    exit_list: arcade.SpriteList[arcade.Sprite]
    slime_list: arcade.SpriteList[arcade.Sprite]
    slime_listaaa: list[Slime]
    physics_engine: arcade.PhysicsEnginePlatformer
    camera: arcade.camera.Camera2D
    display_camera: arcade.camera.Camera2D
    displayed_weapon_sprite: arcade.Sprite
    display_sprite_list: arcade.SpriteList[arcade.Sprite]
    held_keys_list: list[int]
    sounds: dict
    game_map: Map
    score: int
    text_score:arcade.Text
    active_weapon: int

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Setup our game
        self.setup()

    def setup(self) -> None:
        """Set up the game here."""

        self.load_map("map7.txt")
        #self.load_test()

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
        SlimeKilled = arcade.load_sound(":resources:sounds/hurt3.wav")
        NextLevel = arcade.load_sound(":resources:sounds/upgrade1.wav")

        # 
        self.sounds = {}
        self.sounds["Coin"]=Coincollected
        self.sounds["Jump"]=PlayerJumped
        self.sounds["Game_Over"]=GameOver
        self.sounds["Slime killed"] = SlimeKilled
        self.sounds["Next_level"]=NextLevel

        # 
        self.score = 0
        self.text_score = arcade.Text(f"coins : {self.score}",x=5,y=self.camera.height-30,color=arcade.color.RED_ORANGE,font_size=25)

        # 
        self.weapon_display_offsets = {}
        self.weapon_display_offsets[WEAPON_INDEX_SWORD] = [13,-22,18,math.pi/4]
        self.weapon_display_offsets[WEAPON_INDEX_BOW] = [13,-22,0,-math.pi/4]
        self.active_weapon = WEAPON_INDEX_SWORD
        self.displayed_weapon_sprite = arcade.Sprite("assets/kenney-voxel-items-png/sword_silver.png",
                                                     center_x=35,
                                                     center_y=self.camera.height - 65, 
                                                     scale=0.6
                                                     )
        self.displayed_weapon_sprite.append_texture(arcade.load_texture("assets/kenney-voxel-items-png/bow.png"))
        self.display_sprite_list = arcade.SpriteList(use_spatial_hash=True)
        self.display_sprite_list.append(self.displayed_weapon_sprite)

    def load_map(self, chosen_map):
        # Initialize the map
        self.game_map = Map()
        self.game_map.ReadMap(chosen_map)

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
        # Creating of platforms
        self.wall_list.extend(self.load_elements(":resources:images/tiles/grassHalf_mid.png","-"))
        
        # Creating the list of no_go
        self.no_go_list = arcade.SpriteList(use_spatial_hash=True)
        # Creating of lava
        self.no_go_list.extend(self.load_elements(":resources:images/tiles/lava.png","£"))

        # Creating of coins
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list.extend(self.load_elements(":resources:images/items/coinGold.png","*"))

        # Creating of exit sign
        self.exit_list = arcade.SpriteList(use_spatial_hash=True)
        self.exit_list.extend(self.load_elements(":resources:/images/tiles/signExit.png","E"))

        # Creating of enemies
        self.slime_list = arcade.SpriteList(use_spatial_hash=True)
        self.slime_list.extend(self.load_elements(":resources:/images/enemies/slimeBlue.png","o"))
        self.slime_listaaa = []
        for slime in self.slime_list:
            self.slime_listaaa.append(Slime(slime))
            slime.change_x= -1

        # Creating of arrow list
        self.arrow_sprite_list = arcade.SpriteList(use_spatial_hash=True)

        # Creating movement physics and collisions
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.wall_list,
            gravity_constant=PLAYER_GRAVITY
        )

        # Disables multiple jumps
        self.physics_engine.disable_multi_jump(); 


    def load_elements(self, sprite:str,element:str) -> arcade.SpriteList:
        Position = self.game_map.FindElement(element)
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

    def load_test(self) -> None:
        self.load_map("test_map.txt")

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
                    arcade.play_sound(self.sounds["Jump"])
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
                vect_player_click_x = x + self.camera.position[0] -self.player_sprite.position[0] - self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_X] - self.camera.width/2
                vect_player_click_y = y + self.camera.position[1] -self.player_sprite.position[1] - self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_Y] - self.camera.height/2
                weapon_angle = math.atan2(vect_player_click_y,vect_player_click_x)
                match self.active_weapon:
                    case 0: # Case for the sword, using a global variable produces an error
                        weapon = ("assets/kenney-voxel-items-png/sword_silver.png")
                    case 1: # Bow case
                        weapon = ("assets/kenney-voxel-items-png/bow.png")
                self.weapon_sprite = arcade.Sprite(weapon,
                                                  center_x=self.player_sprite.position[0] + self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_X] + math.cos(self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_SPRITE_ANGLE]-weapon_angle)*self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_ANGLE],
                                                  center_y=self.player_sprite.position[1] + self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_Y] + math.sin(self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_SPRITE_ANGLE]-weapon_angle)*self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_ANGLE],
                                                   scale=0.5*0.7)
                self.weapon_sprite.radians = self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_SPRITE_ANGLE]-weapon_angle
                self.player_sprite_list.append(self.weapon_sprite)


                # check to kill slimes
                Slimes_Touched_List : list[arcade.Sprite]
                Slimes_Touched_List = arcade.check_for_collision_with_list(self.weapon_sprite, self.slime_list)
                for slime in Slimes_Touched_List:
                    arcade.play_sound(self.sounds["Slime killed"])
                    slime.kill()
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
                    self.weapon_sprite.kill()
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

        # Move the sword
        try: 
            self.weapon_sprite.center_x=self.player_sprite.position[0] + self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_X] + math.cos(self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_SPRITE_ANGLE]-self.weapon_sprite.radians)*self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_ANGLE]
            self.weapon_sprite.center_y=self.player_sprite.position[1] + self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_Y] + math.sin(self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_SPRITE_ANGLE]-self.weapon_sprite.radians)*self.weapon_display_offsets[self.active_weapon][WEAPON_OFFSET_INDEX_ANGLE]
        except:
            pass

        # Check for collisions with coins
        Coins_Touched_List : list[arcade.Sprite]
        Coins_Touched_List = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Remove touched coins and play the sound
        for coin in Coins_Touched_List:
            self.score += 1
            self.text_score.text = f"coins : {self.score}"
            arcade.play_sound(self.sounds["Coin"])
            coin.remove_from_sprite_lists()

        # Check if collision with no_go (Lava)
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.no_go_list)) != 0:
            arcade.play_sound(self.sounds["Game_Over"])
            self.setup()

        # Check for end of level
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.exit_list)) != 0:
            arcade.play_sound(self.sounds["Next_level"])
            # Check if there is a next map
            if "next-map" in self.game_map.MapConfig:
                self.load_map(self.game_map.MapConfig["next-map"])
            else:
                # Intended : if there is no next map, the player is moved forward, used for debugging purposes
                self.player_sprite.position = (self.player_sprite.position[0]+100,self.player_sprite.position[1])

        # Move the slimes
        Collision_Sprite:arcade.Sprite
        Collision_Sprite = arcade.Sprite(":resources:/images/enemies/slimeBlue.png",scale=0.0001)
        print(len(self.slime_listaaa))
        for slime in self.slime_listaaa:
            if(slime.monster_sprite in self.slime_list):
                slime.move(self.wall_list,collision_sprite=Collision_Sprite)
            else:
                self.slime_listaaa.remove(slime)
                del slime
        Collision_Sprite.kill()

        # Check for collisions with slimes
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.slime_list)) != 0:
            arcade.play_sound(self.sounds["Game_Over"])
            # Veut-on vraiment ce son immonde ? (les 3 et 4 sons game_over sont un peu mieux) 
            # (Tu peux mettre celui que ton coeur préfère, ne te laisse pas influencer par la société)
            self.setup()


    def on_draw(self) -> None:
        """Render the screen."""
        self.clear() # always start with self.clear()

        # Displays items on screen
        with self.camera.activate():
            self.player_sprite_list.draw()
            self.wall_list.draw()
            self.no_go_list.draw()
            self.coin_list.draw()
            self.exit_list.draw()
            self.slime_list.draw()
            # Affiche les hitbox si on appuie sur H
            if arcade.key.H in self.held_keys_list:
                self.player_sprite_list.draw_hit_boxes()
                self.wall_list.draw_hit_boxes()
                self.no_go_list.draw_hit_boxes()
                self.coin_list.draw_hit_boxes()
                self.exit_list.draw_hit_boxes()
                self.slime_list.draw_hit_boxes()

        with self.display_camera.activate():
            self.text_score.draw()
            self.display_sprite_list.draw()
    