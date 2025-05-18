import arcade
import cProfile
from arcade import Sprite, SpriteList, SpriteSequence
from typing import Mapping
from map import Map
from monster import Monster, Slime, Bat, Spider
from weapon import Weapon, Weapon_index
from weapon import Sword, Bow, Arrow
from plateform import Plateform, create_plateforms
from switch import Switch, Gate
from player import Player
from portal import Portal
from typing import Sequence

#Il ne faut pas appeler `update()` sur la SpriteList qui contient les `platforms` que vous donnez au physics engine. Ce dernier fait déjà l'équivalent d'update sur celles-ci. Si vous le faites, le symptôme que vous obtiendrez est que la joueuse "glisse" sur les plateformes en mouvement.

PLAYER_MOVEMENT_SPEED = 7
# Lateral speed of the player, in pixels per frame.

PLAYER_GRAVITY = 1
# Gravity applied to the player, in pixels per frame.

PLAYER_JUMP_SPEED = 21
# Instant vertical speed for jumping, in pixels per frame.

DISTANCE_FROM_UPPER_CAM = 300   
DISTANCE_FROM_LOWER_CAM = 200   
DISTANCE_FROM_RIGHT_CAM = 10    
DISTANCE_FROM_LEFT_CAM = 200    
# Minimum distance between camera and player in all directions

SPRITE_SIZE = 64
# Size of each sprite for the map

PLAYER = ("player")
WALLS = ("full_grass","half_grass","box","gate")
MISCELLANEOUS = ("lava","exit","coin","lever","gate")
ENEMIES = ("slime","bat","spider")
WEAPONS = ("sword","bow","arrow")
ROGUE_BLOCS = ("lever","lava","exit","portal")

MOVING_SPEED = 1

class GameView(arcade.View):
    """Main in-game view."""
    profiler: cProfile.Profile

    player:Player

    displayed_weapon_sprite: Sprite

    camera: arcade.camera.Camera2D
    display_camera: arcade.camera.Camera2D
    display_sprite_list: SpriteList[Sprite]

    display_map_sprite_list:SpriteList[Sprite]

    wall_sprite_list: SpriteList[Sprite]
    plateform_solid_sprite_list: SpriteList[Sprite]
    plateform_permeable_sprite_list:SpriteList[Sprite]

    no_go_sprite_list: SpriteList[Sprite]
    coin_sprite_list: SpriteList[Sprite]
    exit_sprite_list: SpriteList[Sprite]

    switch_sprite_list:SpriteList[Sprite]
    switch_list:list[Switch]
    gate_list:SpriteList[Gate]

    portal_sprite_list:SpriteList[Sprite]
    portal_list:list[Portal]

    monster_list: SpriteList[Monster]

    held_keys: set[int]
    physics_engine: arcade.PhysicsEnginePlatformer
    
    error_message:str
    text_error:arcade.Text

    text_score:arcade.Text
    texture_dict:dict[str,str]
    sound_dict: dict[str,arcade.Sound]
    game_map: Map

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        self.profiler = cProfile.Profile()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Setup our game
        self.setup()

    def setup(self) -> None:
        """Set up the game here."""

        self.player = Player()

        # Setup of cameras
        self.camera = arcade.camera.Camera2D()
        self.display_camera = arcade.camera.Camera2D()

        # Creates the set of pressed keys
        self.held_keys = set()

        # Set the starting score of the player
        self.error_message = ""
        self.text_score = arcade.Text(f"coins : {self.player.score}",x=5,y=self.camera.height-30,color=arcade.color.RED_ORANGE,font_size=25)
        self.text_error = arcade.Text(self.error_message,x=30,y=self.camera.height/3*2,color=arcade.color.RED_DEVIL,font_size=25)

        self.choose_map("test_load.txt")

    def choose_map(self, chosen_map:str)-> None:
        # Initialize the map
        self.game_map = Map()
        try:
            self.game_map.ReadMap(chosen_map)
            self.Load_Map()
        except Exception as error_message:
            self.load_debug(str(error_message))
        except:
            self.load_debug("Someting is wrong with the map")

    def Load_Map(self)->None:

        self.load_textures()
        self.load_sounds()
        self.load_player()
        self.load_plateform()
        self.load_walls()
        self.load_miscellaneous()
        self.load_monster()
        self.load_gate_and_switch()
        self.load_portal()
        self.load_physics()
        self.load_display()


    def load_textures(self)->None:
        """
        Load the wanted textures for the current map (sprites may be customised using packs)
        And Load every sprite on the map
        """
        self.texture_dict = self.game_map.textures
        invalid_caracters:list[str]=[caracter for line in self.game_map.MapString 
                                     for caracter in line 
                                     if caracter not in self.game_map.allowed_caracters]
        if len(invalid_caracters)!=0:
            raise Exception(f"{invalid_caracters} are not allowed in the mapstring")
        self.display_map_sprite_list = SpriteList(use_spatial_hash=True)
        self.display_map_sprite_list.extend([Sprite(self.game_map.match_textures(caracter), scale = 0.5,
                                                    center_x=SPRITE_SIZE/2 + caracter_number*SPRITE_SIZE,
                                                    center_y=SPRITE_SIZE/2 + (self.game_map.height - 1 - line_number)*SPRITE_SIZE) 
                                                    for line_number,line in enumerate(self.game_map.MapString )
                                                    for caracter_number, caracter in enumerate(line)
                                                    if caracter in self.game_map.caracters])
    # Probablement faire une fonction qui charge le bon type de sprite en fonction du caractère
    def load_sounds(self) -> None:
        """
        Load the wanted sounds for the current map (sounds may be customised using packs)
        """
        self.sound_dict = {}
        for sound,path in self.game_map.sounds.items():
            try:
                self.sound_dict[sound] = arcade.load_sound(path)
            except:
                self.game_map.sounds.pop(sound)
                raise Exception(f"{path} isn't in the sound folder")

    def load_player(self)->None:
        """
        Find the sprite of the player on the map and intialize a few variables
        """
        player_sprite_list:SpriteList[Sprite]=SpriteList()
        self.load_element_in_list("player",player_sprite_list)
        if len(player_sprite_list)!= 1:
            raise Exception(f"There are {len(player_sprite_list)} players (caracter : S) on the map instead of 1")
        self.player.assign_sprite(player_sprite_list[0])
        #self.substitute("player",self.player.sprite)
        self.display_map_sprite_list.remove(self.player.sprite) # Let the player handle itself       

    def load_plateform(self)->None:
        """
        Find the sprites that should move and set their speeds
        Create the lists that will contain the moving blocs
        """
        # No need to check for exceptions as they are handled by the "Create plateform method"
        # arcade recommends turning spatial hash off for moving blocs
        self.plateform_solid_sprite_list = SpriteList(use_spatial_hash=False)
        self.plateform_permeable_sprite_list = SpriteList(use_spatial_hash=False) 
        plateforms = create_plateforms(self.game_map)
        for plateform in plateforms:
            self.load_single_plateform(plateform)

    def load_single_plateform(self,plateform:Plateform)->list[tuple[int,int]]:
        """
        Load a single plateform by setting the speed of every bloc inside of it
        Find the blocs that should the player can walk through and the one she can stand on
        """
        for bloc in plateform.blocs:
            # Find the sprite of the bloc
            bloc_sprite = self.match_position_sprite([bloc])[0]

            if self.game_map.caracters[self.game_map.ShowPosition(bloc)] in  ROGUE_BLOCS:
                if plateform.pos_max[0] > 0:
                    bloc_sprite.change_x = MOVING_SPEED
                    bloc_sprite.boundary_right = bloc_sprite.center_x + SPRITE_SIZE*(plateform.pos_max[0]-plateform.pos_start[0])
                    bloc_sprite.boundary_left = bloc_sprite.center_x - SPRITE_SIZE*plateform.pos_start[0]

                if plateform.pos_max[1] > 0:
                    bloc_sprite.change_y = MOVING_SPEED
                    bloc_sprite.boundary_top = bloc_sprite.center_y + SPRITE_SIZE*(plateform.pos_max[1]-plateform.pos_start[1])
                    bloc_sprite.boundary_bottom = bloc_sprite.center_y - SPRITE_SIZE*plateform.pos_start[1]
                self.plateform_permeable_sprite_list.append(bloc_sprite)
            else:
                # Check if the bloc should move horizontally
                if plateform.pos_max[0] > 0:
                    bloc_sprite.change_x = MOVING_SPEED
                    bloc_sprite.boundary_right = SPRITE_SIZE * (plateform.pos_max[0]+bloc[0]-plateform.pos_start[0]) + bloc_sprite.width+1
                    bloc_sprite.boundary_left = SPRITE_SIZE * (bloc[0]-plateform.pos_start[0])+SPRITE_SIZE-(bloc_sprite.right-bloc_sprite.left)+1

                # check if the sprite should move vertically
                if plateform.pos_max[1] > 0:
                    bloc_sprite.change_y = MOVING_SPEED
                    bloc_sprite.boundary_top = SPRITE_SIZE * (plateform.pos_max[1]+bloc[1]-plateform.pos_start[1])+bloc_sprite.height+1
                    bloc_sprite.boundary_bottom = SPRITE_SIZE * (bloc[1]-plateform.pos_start[1])+SPRITE_SIZE-(bloc_sprite.top-bloc_sprite.bottom)+1
                
                self.plateform_solid_sprite_list.append(bloc_sprite)
        return plateform.blocs

    def load_walls(self)->None:
        """
        Find the sprites that are considered walls (solid but not in plateforms)
        """
        # Create the walls, ground | box | platforms
        self.wall_sprite_list = SpriteList(use_spatial_hash=True)
        for wall in WALLS:
            self.wall_sprite_list.extend([sprite for sprite in self.match_caracter_sprite(self.game_map.names[wall]) 
                                          if sprite not in self.plateform_solid_sprite_list])

    def load_element_in_list(self,element:str,list:SpriteList[Sprite])->None:
        """
        Expand the given list with the sprites of the given element
        """
        list.extend(self.match_caracter_sprite(self.game_map.names[element]))

    def load_miscellaneous(self)->None:
        self.no_go_sprite_list = SpriteList(use_spatial_hash=True)
        self.coin_sprite_list = SpriteList(use_spatial_hash=True)
        self.exit_sprite_list = SpriteList(use_spatial_hash=True)

        self.load_element_in_list("lava",self.no_go_sprite_list)
        self.load_element_in_list("coin",self.coin_sprite_list)
        self.load_element_in_list("exit",self.exit_sprite_list)

    def load_monster(self)->None:
        """
        Initialise the lists for the monsters
        """
        self.monster_list = SpriteList(use_spatial_hash=True)

        slime_pos = self.game_map.FindElement(self.game_map.names["slime"])
        slime_sprite = self.match_position_sprite(slime_pos)
        slime_pos_sprite = zip(slime_pos,slime_sprite)
        self.monster_list.extend([Slime(pos,self.game_map, sprite) for (pos,sprite) in slime_pos_sprite])
        
        spider_pos = self.game_map.FindElement(self.game_map.names["spider"])
        spider_sprite = self.match_position_sprite(spider_pos)
        spider_pos_sprite = zip(spider_pos,spider_sprite)
        self.monster_list.extend([Spider(pos,self.game_map, sprite) for (pos,sprite) in spider_pos_sprite])
        # fix the spiders position (they spawn in the air facing left otherwise)
        for spider in self.monster_list: 
            if isinstance(spider,Spider):
                spider.texture = spider.texture.flip_horizontally()
                spider.center_y -= (SPRITE_SIZE - spider.height)/2

        self.monster_list.extend([Bat(bat) for bat in self.match_caracter_sprite(self.game_map.names["bat"])])

        self.substitute(("slime","spider","bat"),self.monster_list)

    def load_gate_and_switch(self)->None:
        """
        Calls ``load_gate()`` then ``load_switch()`` to ensure that every ``Gate`` object has been initialised 
        """
        gate_dict = self.load_gate()
        self.load_switch(gate_dict)

    def load_gate(self)->dict[tuple[int,int],Gate]:
        """
        Initialise the ``Gate`` objects 

        !! 
        Must be called before ``load_switch()`` it relies on the ``gate_dict`` attribute
        which is initialised in this method
        !!
        """

        self.gate_list = SpriteList(use_spatial_hash=True)
        gate_positions = self.game_map.FindElement(self.game_map.names["gate"])
        gate_sprites = self.match_position_sprite(gate_positions)
        gate_sprite_position = dict(zip(gate_positions,gate_sprites))
        gate_dict:dict[tuple[int,int],Gate] = {}

        if 'gates' in self.game_map.config:
            gates = self.game_map.config['gates']
            if isinstance(gates,list):
                for gate in gates:
                    position = (int(gate['x']), int(gate['y']))
                    state_str:str = gate['state']
                    opened:bool = False
                    match state_str:
                        case 'open': opened = True
                        case 'closed': opened = False
                    sprite = gate_sprite_position[position]
                    gate_dict[position] = Gate(sprite,position,opened)
                    self.gate_list.append(gate_dict[position])

        for pos,sprite in gate_sprite_position.items():
            if pos not in gate_dict:
                gate_dict[pos] = Gate(sprite,pos,False)
                self.gate_list.append(gate_dict[pos])

        self.substitute("gate",self.gate_list)
        return gate_dict

    def load_switch(self, gate_dict:dict[tuple[int,int],Gate])->None:
        """
        Initialise the ``Switch`` objects 

        !!
        Warning the method ``load_gate()`` must be called before hand to ensure
        that the switches can associate with ``gate_dict``
        !!
        """
        self.switch_sprite_list = SpriteList(use_spatial_hash=True)
        self.switch_list = []
        if "switches" in self.game_map.config:
            switches = self.game_map.config["switches"]
            if isinstance(switches,list):
                for switch in switches:
                    if isinstance(switch, dict):
                        if 'x' in switch and 'y' in switch:
                            position = (int(switch['x']),int(switch['y']))
                            sprite = self.match_position_sprite([position])[0]
                        state:bool = False
                        if 'state' in switch:
                            state = switch['state']
                        switch_off_actions = []
                        if 'switch_off' in switch:
                            switch_off_actions = switch['switch_off']
                        switch_on_actions = []
                        if 'switch_on' in switch:
                            switch_on_actions = switch['switch_on']

                        actions = switch_on_actions.copy()
                        actions.extend(switch_off_actions)

                        sprite.append_texture(arcade.load_texture(":resources:/images/tiles/leverRight.png"))
                        self.switch_sprite_list.append(sprite)
                        self.switch_list.append(Switch(sprite, state = state, gates=gate_dict,
                                                       switch_off_actions=switch_off_actions,
                                                       switch_on_actions=switch_on_actions))

    def load_portal(self)->None:
        pass
        """
        Initialise the ``Portal`` objects 
        """
        """self.portal_sprite_list = SpriteList(use_spatial_hash=True)
        self.portal_list = []
        portal_positions = self.game_map.FindElement(self.game_map.names["gate"])
        portal_sprites = self.match_position_sprite(portal_positions)
        gate_sprite_position = dict(zip(gate_positions,gate_sprites))
        self.gate_dict = {}

        if 'portals' in self.game_map.config:
            gates = self.game_map.config['portals']
            if isinstance(gates,list):
                for gate in gates:
                    position = (int(gate['x']), int(gate['y']))
                    state_str:str = gate['state']
                    opened:bool = False
                    match state_str:
                        case 'open': opened = True
                        case 'closed': opened = False
                    sprite = gate_sprite_position[position]
                    self.gate_dict[position] = Gate(sprite,position,opened)
                    self.gate_sprite_list.append(sprite)
                    self.gate_list.append(self.gate_dict[position])
        for pos,sprite in gate_sprite_position.items():
            if sprite not in self.gate_sprite_list:
                self.gate_sprite_list.append(sprite)
                self.gate_dict[pos] = Gate(sprite,pos,False)
                self.gate_list.append(self.gate_dict[pos])"""

    def load_physics(self)->None:
        """
        Intialize the PhysicsEngine (walls, moving plateforms, player movement)
        """
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player.sprite,
            walls=self.wall_sprite_list,
            platforms=self.plateform_solid_sprite_list,
            gravity_constant=self.player.gravity
        )

        # Disables multiple jumps
        self.physics_engine.disable_multi_jump()

    def load_display(self)->None:
        """
        Load the display for the player's weapon 
        """
        self.active_weapon = Weapon_index.SWORD
        self.displayed_weapon_sprite = Sprite("assets/kenney-voxel-items-png/sword_silver.png", center_x=35, center_y=self.camera.height - 65, scale=0.6)
        self.displayed_weapon_sprite.append_texture(arcade.load_texture("assets/kenney-voxel-items-png/bow.png"))

        self.display_sprite_list = SpriteList(use_spatial_hash=True)
        self.display_sprite_list.append(self.displayed_weapon_sprite) 

    def substitute(self,deleted_elements:Sequence[str]|str,subbed_elements:SpriteSequence[Sprite]|Sprite)->None:
        """
        Take away the `deleted_elements` from `self.map_display_sprite_list` and add the `subbed_elements` instead
        """
        # make the elements into ones we can iterate on
        if isinstance(deleted_elements,str):deleted_elements = [deleted_elements]

        unwanted_stuff:SpriteList[Sprite] = SpriteList(lazy=True)
        for unwanted_type in deleted_elements:
            unwanted_stuff.extend(self.match_caracter_sprite(self.game_map.names[unwanted_type]))

        for unwanted in unwanted_stuff :
            if unwanted in self.display_map_sprite_list:self.display_map_sprite_list.remove(unwanted) 

        if isinstance(subbed_elements,Sprite):self.display_map_sprite_list.append(subbed_elements)
        else:self.display_map_sprite_list.extend([wanted for wanted in subbed_elements])


    def match_caracter_sprite(self, element:str)->SpriteList[Sprite]:
        """
        Returns the list of sprites that are associated with the given caracter by calling ``match_position_sprite()``
        """
        return self.match_position_sprite(self.game_map.FindElement(element))

    def match_position_sprite(self, positions:list[tuple[int,int]]) -> SpriteList[Sprite]:
        """
        Returns the list of sprites that are in the given positions
        """
        sprite_list:SpriteList[Sprite] = SpriteList(use_spatial_hash=True)
        sprite_list.extend([sprite for sprite in self.display_map_sprite_list 
                if ((sprite.center_x - SPRITE_SIZE/2) / SPRITE_SIZE,
                    (sprite.center_y - SPRITE_SIZE/2) / SPRITE_SIZE) in positions])
        return sprite_list

    def on_key_press(self, key: int, modifiers: int) -> None:
        """
        Called when the user presses a key on the keyboard
        """

        self.held_keys.add(key) # Keep track of the pressed key

        match key:
            case arcade.key.UP:
                # Jump if possible
                if self.physics_engine.can_jump():
                    self.player.jump() 
                    arcade.play_sound(self.sound_dict["PlayerJumped"])
            case arcade.key.ESCAPE: self.setup() # Restart the game

    def on_key_release(self, key: int, modifiers: int) -> None:
        """
        Called when the user releases a key on the keyboard
        """

        self.held_keys.discard(key) # Keep track of the released key

        match key:
            case arcade.key.RIGHT | arcade.key.LEFT:
                self.player.horizontal_stop()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """
        Called when the user presses a mouse button
        """

        self.held_keys.add(button) # keep track of the held mouse button

        match button:
            case arcade.MOUSE_BUTTON_LEFT:
                # Aim and create the weapon 
                relative_click_x = x + self.camera.position[0] - self.camera.width/2
                relative_click_y = y + self.camera.position[1] - self.camera.height/2
                relative_click = (relative_click_x,relative_click_y)
                self.player.create_weapon(relative_click)
                if self.player.active_weapon == Weapon_index.SWORD:
                    # check to kill monsters
                    Monster_Touched : list[Sprite]
                    Monster_Touched = arcade.check_for_collision_with_list(self.player.weapon, self.monster_list)
                    for monster in Monster_Touched:
                        arcade.play_sound(self.sound_dict["MonsterKilled"])
                        monster.kill()
                    self.trigger_switches(set(arcade.check_for_collision_with_list(self.player.weapon, self.switch_sprite_list)))

            case arcade.MOUSE_BUTTON_RIGHT:
                self.player.toggle_weapon()
                self.displayed_weapon_sprite.set_texture(self.player.active_weapon-1) # adapt the display

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int) -> None:
        """
        Called when the user releases a mouse button
        """

        # Remembers that the mouse button is released
        self.held_keys.discard(button)
        
        match button:
            case arcade.MOUSE_BUTTON_LEFT:
                try:
                    self.player.weapon.kill()
                    del self.player.weapon
                except:
                    pass

    def on_update(self, delta_time: float) -> None:
        """Called once per frame, before drawing.

        This is where in-world time "advances", or "ticks".
        """

        self.profiler.enable()
        self.do_on_update(delta_time)
        self.profiler.disable()

    def do_on_update(self, delta_time: float)->None:
        # Act according to the pressed keys
        for key in self.held_keys:
            match key:
                case arcade.key.RIGHT: self.player.move_right()
                case arcade.key.LEFT: self.player.move_left()

        self.physics_engine.update()

        self.move_fake_plateforms()
        self.move_camera()
        self.move_weapons()
        self.move_monsters()

        self.collision_with_coin()
        self.collision_with_lava()
        self.collisions_with_exit()
        self.collisions_with_monster() 

    def move_fake_plateforms(self)->None:
        """
        Manually move the blocs that aren't in the plateforms but should be moving
        """
        self.plateform_permeable_sprite_list.update()
        for bloc in self.plateform_permeable_sprite_list: 
            # check if the bloc has hit it's boundaries
            if bloc.boundary_bottom!= None and bloc.boundary_top!= None:
                if bloc.boundary_top- bloc.center_y <=0 or bloc.center_y-bloc.boundary_bottom <=0:
                    bloc.change_y = -bloc.change_y
            if bloc.boundary_left != None and bloc.boundary_right != None:
                if bloc.center_x - bloc.boundary_left<= 0 or bloc.boundary_right - bloc.center_x <=0:
                    bloc.change_x = -bloc.change_x

    def move_camera(self)->None:
        """
        Move the camera according to the player's position (measures the difference from the center)
        """
        x = self.player.sprite.position[0] - self.camera.position.x
        y = self.player.sprite.position[1] - self.camera.position.y
        if x > DISTANCE_FROM_RIGHT_CAM:
            self.camera.position += (x-DISTANCE_FROM_RIGHT_CAM,0)
        elif x < -DISTANCE_FROM_LEFT_CAM:
            self.camera.position += (x+DISTANCE_FROM_LEFT_CAM,0)
        if y > DISTANCE_FROM_UPPER_CAM:
            self.camera.position += (0,y-DISTANCE_FROM_UPPER_CAM)
        elif y < -DISTANCE_FROM_LOWER_CAM:
            self.camera.position += (0,y+DISTANCE_FROM_LOWER_CAM)

    def move_weapons(self)->None:
        """
        Move the weapons (i.e. sword, bow, arrows, ...) of the player
        """
        self.player.move_weapon()

        # Check if the arrows hit anything and act accordingly
        self.player.arrows_hit(self.wall_sprite_list)
        self.player.arrows_hit(self.plateform_solid_sprite_list)
        self.player.arrows_hit(self.no_go_sprite_list)

        enemies_touched = self.player.arrows_hit(self.monster_list)
        switch_touched = self.player.arrows_hit(self.switch_sprite_list)

        for enemy in enemies_touched:
            enemy.kill()
            arcade.play_sound(self.sound_dict["MonsterKilled"])

        for switch in self.switch_list:
            if switch.sprite in switch_touched: switch.trigger_actions()

    def move_monsters(self)->None:
        """
        Move the monsters on the map
        """
        for monster in self.monster_list:
            monster.move()

    def collision_with_coin(self)->None:
        """
        Check for collisions with the coins
        Remove any that was touched and up the score of the player accordingly
        """
        Coins_Touched_List : list[Sprite]
        Coins_Touched_List = arcade.check_for_collision_with_list(self.player.sprite, self.coin_sprite_list)

        for coin in Coins_Touched_List:
            self.player.score += 1
            self.text_score.text = f"coins : {self.player.score}"
            arcade.play_sound(self.sound_dict["CoinCollected"])
            coin.remove_from_sprite_lists()

    def collision_with_lava(self)->None:
        """
        Check for collisions with lava and kill the player if so
        """
        if len(arcade.check_for_collision_with_list(self.player.sprite, self.no_go_sprite_list)) != 0:
            self.game_over()

    def collisions_with_exit(self)->None:
        """
        Check if the player has reached the end of the level
        If so load the next level
        If there is no next level, the "debug map" is loaded instead
        """
        if len(arcade.check_for_collision_with_list(self.player.sprite, self.exit_sprite_list)) != 0:
            arcade.play_sound(self.sound_dict["NextLevel"])
            if "next-map" in self.game_map.config:
                match type(self.game_map.config["next-map"]):
                    case str(): self.choose_map(self.game_map.config["next-map"])
                    case _: self.load_debug("Something went wrong with the new map text")
            else:
                self.load_debug("There was no next level")
    
    def collisions_with_monster(self)->None:
        """
        Check for collisions with monsters and kill the player if so
        """
        if len(arcade.check_for_collision_with_list(self.player.sprite, self.monster_list)) != 0:
            self.game_over()

    def trigger_switches(self,switches:set[Sprite])->None:
        """
        Trigger the given switches 
        """
        triggered_switch:list[Switch]=[switch for switch in self.switch_list if switch.sprite in switches]
        for switch in triggered_switch:
            switch.trigger_actions()

    def game_over(self)->None:
        """
        Restart the game and play the "game over" sound effect
        """
        arcade.play_sound(self.sound_dict["GameOver"])
        self.setup()

    def load_debug(self, error_message:str) -> None:
        """
        Load a preset map and display the error message to the user
        """
        self.error_message = error_message
        self.text_error.text = self.error_message
        self.game_map = Map()
        self.game_map.ReadMap("debug_map.txt")
        self.Load_Map()

    def on_draw(self) -> None:
        """
        Render the screen
        """
        self.clear()

        with self.camera.activate():
            self.display_map_sprite_list.draw()
            self.player.draw()
                     
        with self.display_camera.activate(): # display the texts and  the player weapon
            self.text_score.draw()
            self.display_sprite_list.draw()
            self.text_error.draw()   