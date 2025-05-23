from typing import TextIO, Final
import yaml

PATH_PACK = "loading_packs/"

Action_Type = dict[str,str|int]
Switch_type = dict[str,int|bool|list[Action_Type]]
Config_type = str | int | Switch_type

class Map():
    MapString:list[str] # Storing the map disposition
    config:dict[str,Config_type] # Storing parameters and their values
    height:int
    width:int
    caracters: dict[str,str]
    names:dict[str,str]
    textures:dict[str,str]
    sounds:dict[str,str]
    allowed_caracters:Final[tuple[str,...]] = (""," ","=","-","x","£","E","*","^","|","p","S","o","v","8","→","↑","←","↓")

    def __init__(self) -> None:
        self.MapString = []
        self.config = {}
        self.caracters = {}
        self.textures = {}
        self.sounds = {}
    
    def ReadMap(self, chosen_map:str) -> bool:
        with open("map/" + chosen_map, "r", encoding="utf-8", newline='\n') as MapFile:
            read:bool = self.ReadFile(MapFile)
        if read:
            packs = ("caracters","textures","sounds")
            for pack in packs:
                self.config[pack]=self.config.get(pack,PATH_PACK+pack+"/default.txt")
                path = self.config[pack]
                if isinstance(path,str):
                    if not self.ReadPack(pack,path):
                        read = False
                else: raise Exception(f"Something went wrong with the path to the {pack} pack")
            self.names = {name: caracter for caracter,name in self.caracters.items()}
            
        return read


    def ReadFile(self, MapFile: TextIO)->bool:
        try:
            read_config:bool = True # Begins the reading process by checking for parameters
            map_config:list[str]=[]
            map_design:list[str]=[]
            for line in MapFile:
                if read_config: # Read the config part for the map
                    if(line[:3]=="---"): # This detects the end of the "config part" of the file
                        read_config = False
                    else:
                        map_config.append(Remove_from(line))
                else:
                    map_design.append(Remove_from(line))
            
            map_config_yaml = "\n".join(map_config)

            self.config=yaml.safe_load(map_config_yaml)
            
            self.Read_design(map_design)
            
            return True
        except:
            return False

    def Read_design(self, map_string:list[str])->None:
        match self.config["height"]:
            case str(): self.height = int(self.config["height"])
            case int(): self.height = self.config["height"]
            case _: raise Exception(f"Wrong type for config 'height', expected 'str | int' given {type(self.config["height"])}")
        
        match self.config["width"]:
            case str(): self.width = int(self.config["width"])
            case int(): self.width = self.config["width"]
            case _: raise Exception(f"Wrong type for config 'width', expected 'str | int' given {type(self.config["width"])}")

        for line in map_string:
                if len(self.MapString) < self.height:
                    self.MapString.append("")
                    for i in range(self.width):
                        if i >= len(line):
                            self.MapString[-1] += " "
                        elif line[i]=="\n"or line[i]=="\r":
                            self.MapString[-1] += " "
                        else:
                            self.MapString[-1] += line[i]
    
    def FindElement(self, element:str)-> list[tuple[int,int]]:
        Position: list[tuple[int,int]]
        Position= []
        for LineChecked in range(len(self.MapString)):
            for CharacterChecked in range(len(self.MapString[LineChecked])):
                if(self.MapString[LineChecked][CharacterChecked]== element):
                    Position.append((CharacterChecked,len(self.MapString) - 1 - LineChecked))

        return Position

    def ShowPosition(self, position:tuple[int,int])->str:
        if position[0]>=0 and position[0]<self.width and position[1]>=0 and position[1]<self.height:
            return self.MapString[-position[1]-1][position[0]]
        return ""

    def ReadPack(self, pack:str, path:str="")-> bool:
        try:
            if path == "":
                match type(self.config[pack]):
                    case str(): path = self.config[pack]
                    case _: return False

            with open(path, "r", encoding="utf-8", newline='\n') as PackFile:
                match pack:
                    case "caracters": self.caracters = yaml.safe_load(PackFile)
                    case "sounds": self.sounds = yaml.safe_load(PackFile)
                    case "textures": self.textures = yaml.safe_load(PackFile)
                    case _: return False
        except:
            
            return False
        return True

    def match_textures(self,caracter:str)->str:
        return self.textures[self.caracters[caracter]]
        

    def ShowMap(self) -> None:
        # Printing for debugging
        for line in self.config:
            print(line, end=': ')
            print(self.config[line])
        for line in self.MapString:
            print(line)

def Remove_from(line:str,characters:tuple[str,...] = ("\n","\r"))->str:
    """ Take away the unwanted characters at the end of lines"""
    Done = False
    while len(line) > 0 and not Done:
        if line[:-1] in characters:
            line = line[:-1]
        else:
            Done = True
    return line