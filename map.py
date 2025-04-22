from typing import TextIO
import yaml

class Map():
    MapString:list[str] # Storing the map disposition
    MapConfig:dict[str,str] # Storing parameters and their values

    def __init__(self) -> None:
        self.MapString = []
        self.MapConfig = {}
    
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

            self.MapConfig=yaml.safe_load(map_config_yaml)
            self.Read_design(map_design)
            return True
        except:
            return False

    def Read_design(self, map_string:list[str])->None:
        for line in map_string:
            if len(self.MapString) < int(self.MapConfig["height"]):
                self.MapString.append("")
                for i in range(int(self.MapConfig["width"])):
                    if i >= len(line):
                        self.MapString[-1] += " "
                    elif line[i]=="\n"or line[i]=="\r":
                        self.MapString[-1] += " "
                    else:
                        self.MapString[-1] += line[i]

    def ReadMap(self, chosen_map:str) -> bool:
        with open("map/" + chosen_map, "r", encoding="utf-8", newline='') as MapFile:
            return self.ReadFile(MapFile)
    
    def FindElement(self, element:str)-> list[tuple[int,int]]:
        Position: list[tuple[int,int]]
        Position= []
        for LineChecked in range(len(self.MapString)):
            for CharacterChecked in range(len(self.MapString[LineChecked])):
                if(self.MapString[LineChecked][CharacterChecked]== element):
                    Position.append((CharacterChecked,len(self.MapString) - 1 - LineChecked))

        return Position

    def ShowPosition(self, position:tuple[int,int])->str:
        if position[0]>=0 and position[0]<int(self.MapConfig["width"]) and position[1]>=0 and position[1]<int(self.MapConfig["height"]):
            return self.MapString[-position[1]-1][position[0]]
        return ""

    def ShowMap(self) -> None:
        # Printing for debugging
        for line in self.MapConfig:
            print(line, end=': ')
            print(self.MapConfig[line])
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