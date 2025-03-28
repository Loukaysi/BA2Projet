class Map():
    MapString:list[str] # Storing the map disposition
    MapConfig:dict[str,str] # Storing parameters and their values

    def __init__(self) -> None:
        self.MapString = []
        self.MapConfig = {}
    
    def ReadMap(self, chosen_map:str) -> None:
        with open("map/" + chosen_map, "r", encoding="utf-8", newline='') as MapFile:
            Read_Config = True # Begins the reading process by checking for parameters
            for line in MapFile:
                if Read_Config: # Read the parameters for the map
                    if(line=="---\r\n"): # This detects the end of the "config part" of the file
                        Read_Config = False
                    else: # Store the new parameter in the "config attribute"
                        Name = "" 
                        Value = ""
                        Name_complete = False
                        for c in line:
                            if c == ':': # Find the separator between the name and the value of the parameter
                                Name_complete = True
                            elif c == '\n': # Check for the end of the line
                                if Name == "next-map":
                                    self.MapConfig[Name] = Value[:-1] # Take away the \r at the end of the line
                                else: 
                                    self.MapConfig[Name] = Value[:-1] # Store the parameter and it's value
                            elif Name_complete == False: # Store the name
                                Name+=(c)
                            elif c != ' ': # Store the value (making sure to exclude the space bewtween the ':' and the value)
                                Value+=(c)
                elif len(self.MapString) ==int(self.MapConfig["height"]): #check for end of file
                    pass
                else: # Store the map disposition
                    self.MapString.append("")
                    for i in range(int(self.MapConfig["width"])):
                        if i >= len(line):
                            self.MapString[-1] = self.MapString[-1] +" "
                        else:
                            self.MapString[-1] = self.MapString[-1] +line[i]

    
    def FindElement(self, element:str)-> list[tuple[int,int]]:
        Position: list[tuple[int,int]]
        Position= []
        for LineChecked in range(len(self.MapString)):
            for CharacterChecked in range(len(self.MapString[LineChecked])):
                if(self.MapString[LineChecked][CharacterChecked]== element):
                    Position.append((len(self.MapString) - LineChecked, CharacterChecked))

        return Position

    def ShowMap(self) -> None:
        # Printing for debugging
        for line in self.MapConfig:
            print(line, end=': ')
            print(self.MapConfig[line])
        for line in self.MapString:
            print(line)