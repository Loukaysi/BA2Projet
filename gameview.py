import arcade
from arcade import Sprite, SpriteList
from map import Map
from monster import Monster, Slime, Bat
from weapon import Weapon, Weapon_index
from weapon import Sword, Bow, Arrow
from plateform import Plateform, create_plateforms

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

SPRITE_SIZE = 64
# Size of each sprite for the map

class GameView(arcade.View):
    """Main in-game view."""

    player_sprite:Sprite
    player_weapon:Weapon
    player_sprite_list: SpriteList[Sprite]

    arrow_sprite_list: SpriteList[Sprite]
    arrow_list: list[Arrow]
    active_weapon: Weapon_index
    displayed_weapon_sprite: Sprite

    camera: arcade.camera.Camera2D
    display_camera: arcade.camera.Camera2D
    display_sprite_list: SpriteList[Sprite]

    wall_sprite_list: SpriteList[Sprite]
    plateform_sprite_list: SpriteList[Sprite]
    no_go_sprite_list: SpriteList[Sprite]
    coin_sprite_list: SpriteList[Sprite]
    ext_sprite_list: SpriteList[Sprite]

    monster_sprite_list: SpriteList[Sprite]
    monster_list: list[Monster]

    held_keys: set[int]
    physics_engine: arcade.PhysicsEnginePlatformer
    
    error_message:str
    text_error:arcade.Text

    score: int
    text_score:arcade.Text
    sound_dict: dict[str,arcade.Sound]
    texture_dict: dict[str,str]
    game_map: Map
    plateform_positions_list: list[tuple[int,int]]

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Setup our game
        self.setup()

    def setup(self) -> None:
        """Set up the game here."""

        self.choose_map("test_map_base.txt")

        # Setup of cameras
        self.camera = arcade.camera.Camera2D()
        self.display_camera = arcade.camera.Camera2D()

        # Creates the list of pressed keys
        self.held_keys = set()

        # Loads all sounds that should be played
        Coincollected = arcade.load_sound(":resources:sounds/coin1.wav")
        PlayerJumped = arcade.load_sound(":resources:sounds/jump1.wav")
        GameOver = arcade.load_sound(":resources:sounds/gameover1.wav")
        MonsterKilled = arcade.load_sound(":resources:sounds/hurt3.wav")
        NextLevel = arcade.load_sound(":resources:sounds/upgrade1.wav")

        # 
        self.sound_dict = {}
        self.sound_dict["Coin"]=Coincollected
        self.sound_dict["Jump"]=PlayerJumped
        self.sound_dict["Game_Over"]=GameOver
        self.sound_dict["Monster killed"] = MonsterKilled
        self.sound_dict["Next_level"]=NextLevel

        # 
        self.score = 0
        self.text_score = arcade.Text(f"coins : {self.score}",x=5,y=self.camera.height-30,color=arcade.color.RED_ORANGE,font_size=25)
        self.text_error = arcade.Text(self.error_message,x=150,y=self.camera.height/2,color=arcade.color.RED_DEVIL,font_size=50)
        
        # Define the arrow list
        self.arrow_list = []
        self.arrow_sprite_list = SpriteList(use_spatial_hash=True)
       # 
        self.active_weapon = Weapon_index.SWORD
        self.displayed_weapon_sprite = Sprite("assets/kenney-voxel-items-png/sword_silver.png", center_x=35, center_y=self.camera.height - 65, scale=0.6)
        self.displayed_weapon_sprite.append_texture(arcade.load_texture("assets/kenney-voxel-items-png/bow.png"))

        self.display_sprite_list = SpriteList(use_spatial_hash=True)
        self.display_sprite_list.append(self.displayed_weapon_sprite)

    def choose_map(self, chosen_map:str)-> None:
        # Initialize the map
        self.game_map = Map()
        try:
            if self.game_map.ReadMap(chosen_map):
                self.error_message = ""
                self.Load_Map()
        except Exception as error_message:
            self.load_debug(str(error_message))
        except:
            self.load_debug("Someting is wrong with the map")

    def Load_Map(self)->None:
        self.texture_dict={}
        self.texture_dict["="]=":resources:images/tiles/grassMid.png"
        self.texture_dict["-"]=":resources:images/tiles/grassHalf_mid.png"
        self.texture_dict["x"]=":resources:images/tiles/boxCrate_double.png"
        self.texture_dict["£"]=":resources:images/tiles/lava.png"
        self.texture_dict["E"]=":resources:images/tiles/signExit.png"


        # Create the plateforms 
        self.plateform_positions_list = []
        self.plateform_sprite_list = SpriteList(use_spatial_hash=True)
        plateforms = create_plateforms(self.game_map)
        for plateform in plateforms:
            self.plateform_positions_list.extend(self.load_plateform(plateform))  

        # Create the player
        self.player_sprite=self.load_elements(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png","S")[0]
        self.player_sprite_list = SpriteList(use_spatial_hash=True)
        self.player_sprite_list.append(self.player_sprite)

        # Create the walls, ground | box | platforms
        self.wall_sprite_list = SpriteList(use_spatial_hash=True)
        self.wall_sprite_list.extend(self.load_elements(":resources:images/tiles/grassMid.png","="))
        self.wall_sprite_list.extend(self.load_elements(":resources:images/tiles/boxCrate_double.png","x"))
        self.wall_sprite_list.extend(self.load_elements(":resources:images/tiles/grassHalf_mid.png","-"))

        # Create the "no-go" zones, lava
        self.no_go_sprite_list = SpriteList(use_spatial_hash=True)
        self.no_go_sprite_list.extend(self.load_elements(":resources:images/tiles/lava.png","£"))

        # Create the coins
        self.coin_sprite_list = SpriteList(use_spatial_hash=True)
        self.coin_sprite_list.extend(self.load_elements(":resources:images/items/coinGold.png","*"))

        # Create the exit sign
        self.ext_sprite_list = SpriteList(use_spatial_hash=True)
        self.ext_sprite_list.extend(self.load_elements(":resources:images/tiles/signExit.png","E"))

        # Create the enemies, slimes | bats
        self.monster_list = []

        self.monster_list.extend([Slime(slime) for slime in self.load_elements(":resources:images/enemies/slimeBlue.png","o")])
        self.monster_list.extend([Bat(bat) for bat in self.load_elements("assets/kenney-extended-enemies-png/bat.png","v")])

        self.monster_sprite_list= SpriteList(use_spatial_hash=True)
        self.monster_sprite_list.extend([monster.monster_sprite for monster in self.monster_list])

        # Creating movement physics and collisions
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.wall_sprite_list,
            platforms=self.plateform_sprite_list,
            gravity_constant=PLAYER_GRAVITY
        )

        # Disables multiple jumps
        self.physics_engine.disable_multi_jump(); 

    def load_plateform(self,plateform:Plateform)->list[tuple[int,int]]:
        for bloc in plateform.blocs:
            bloc_sprite = Sprite(self.texture_dict[self.game_map.ShowPosition(bloc)],scale=0.5,
                                   center_x=SPRITE_SIZE/2+bloc[0]*SPRITE_SIZE,
                                   center_y=SPRITE_SIZE/2+bloc[1]*SPRITE_SIZE)
            
            if plateform.pos_max[0] > 0:
                bloc_sprite.change_x = 1
                bloc_sprite.boundary_right = SPRITE_SIZE * (plateform.pos_max[0]+bloc[0]-plateform.pos_start[0]) + bloc_sprite.width
                bloc_sprite.boundary_left = SPRITE_SIZE * (bloc[0]-plateform.pos_start[0])+SPRITE_SIZE-(bloc_sprite.right-bloc_sprite.left)

            if plateform.pos_max[1] > 0:
                bloc_sprite.change_y = 1
                bloc_sprite.boundary_top = SPRITE_SIZE * (plateform.pos_max[1]+bloc[1]-plateform.pos_start[1])+bloc_sprite.height
                bloc_sprite.boundary_bottom = SPRITE_SIZE * (bloc[1]-plateform.pos_start[1])+SPRITE_SIZE-(bloc_sprite.top-bloc_sprite.bottom)
            self.plateform_sprite_list.append(bloc_sprite)
        return plateform.blocs

    def load_elements(self, sprite:str,element:str) -> SpriteList[Sprite]:
        Position = self.game_map.FindElement(element)
        Sprite_List: SpriteList[Sprite]
        Sprite_List = SpriteList(use_spatial_hash=True)
        Sprite_List.extend([Sprite(sprite, scale= 0.5,
                                          center_x= SPRITE_SIZE/2+Pos[0]*SPRITE_SIZE,
                                          center_y= SPRITE_SIZE/2+Pos[1]*SPRITE_SIZE) 
                            for Pos in Position if Pos not in self.plateform_positions_list])
        return Sprite_List

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called when the user presses a key on the keyboard."""

        self.held_keys.add(key)

        match key:
            case arcade.key.UP:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED  
                    arcade.play_sound(self.sound_dict["Jump"])
            case arcade.key.ESCAPE:
                # Restart the game
                self.setup()

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key on the keyboard."""

        self.held_keys.discard(key)

        match key:
            case arcade.key.RIGHT | arcade.key.LEFT:
                self.player_sprite.change_x = 0

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """Called when the user presses a mouse button"""

        self.held_keys.add(button)

        match button:
            case arcade.MOUSE_BUTTON_LEFT:
                # Aim the weapon
                match self.active_weapon:
                    case Weapon_index.SWORD:
                        self.player_weapon = Sword(self.player_sprite.position,self.camera,(x,y))
                        # check to kill monsters
                        Monster_Touched : list[Sprite]
                        Monster_Touched = arcade.check_for_collision_with_list(self.player_weapon.weapon_sprite, self.monster_sprite_list)
                        for monster in Monster_Touched:
                            arcade.play_sound(self.sound_dict["Monster killed"])
                            monster.kill()
                    case Weapon_index.BOW:
                        self.player_weapon = Bow(self.player_sprite.position,self.camera,(x,y))
                        # Spawn an arrow
                        arrow = Arrow(self.player_sprite.position,self.camera,(x,y))
                        self.arrow_list.append(arrow)
                        self.arrow_sprite_list.append(arrow.weapon_sprite)

                self.player_sprite_list.append(self.player_weapon.weapon_sprite)

            case arcade.MOUSE_BUTTON_RIGHT:
                match self.active_weapon:
                    case Weapon_index.SWORD:
                        self.active_weapon = Weapon_index.BOW
                    case Weapon_index.BOW:
                        self.active_weapon = Weapon_index.SWORD
               
                self.displayed_weapon_sprite.set_texture(self.active_weapon-1)
                            

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        """Calles when the user releases a mouse button"""

        # Remembers that the mouse button is released
        self.held_keys.discard(button)
        
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
        for key in self.held_keys:
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

        # Move the weapon around if it exists
        try: 
            self.player_weapon.move(self.player_sprite.position)
        except:
            pass

        # move the arrows
        for arrow in self.arrow_list:
            arrow.move((0,0),wall = self.wall_sprite_list,plateforms=self.plateform_sprite_list,no_go =self.no_go_sprite_list)
            if arrow.weapon_sprite in self.arrow_sprite_list:
                for enemy in arcade.check_for_collision_with_list(arrow.weapon_sprite,self.monster_sprite_list):
                    enemy.kill()
                    arrow.weapon_sprite.kill()
                    del arrow

        # Check for collisions with coins
        Coins_Touched_List : list[Sprite]
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
                # Intended : if there is no next level, load the debugging map
                self.load_debug("There was no next level")

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

    def load_debug(self, error_message:str) -> None:
        self.error_message = error_message
        self.game_map = Map()
        self.game_map.ReadMap("debug_map.txt")
        self.Load_Map()

    def on_draw(self) -> None:
        """Render the screen."""
        self.clear() # always start with self.clear()

        # Displays items on screen
        with self.camera.activate():
            self.player_sprite_list.draw()
            self.wall_sprite_list.draw()
            self.plateform_sprite_list.draw()
            self.no_go_sprite_list.draw()
            self.coin_sprite_list.draw()
            self.ext_sprite_list.draw()
            self.monster_sprite_list.draw()
            self.arrow_sprite_list.draw()
            # Affiche les hitbox si on appuie sur H
            if arcade.key.H in self.held_keys:
                self.player_sprite_list.draw_hit_boxes()
                self.wall_sprite_list.draw_hit_boxes()
                self.plateform_sprite_list.draw_hit_boxes()
                self.no_go_sprite_list.draw_hit_boxes()
                self.coin_sprite_list.draw_hit_boxes()
                self.ext_sprite_list.draw_hit_boxes()
                self.monster_sprite_list.draw_hit_boxes()
                self.arrow_sprite_list.draw_hit_boxes()

        with self.display_camera.activate():
            self.text_score.draw()
            self.display_sprite_list.draw()
            self.text_error.draw()
    