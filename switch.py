from enum import Enum, auto
from typing import Final, Sequence
from arcade import Sprite

class State(Enum):
    ON=auto()
    OFF=auto()
    DISABLED=auto()

class Action:
    def act(self,state:State)->None:
        pass


class SwitchGate(Action):
    gate:Sprite

class DisableSwitch(Action):
    pass

class Switch:
    state:State = State.OFF
    actions:Final[dict[State,tuple[Action,...]]]
    sprite:Final[Sprite]

    def __init__(self,sprite:Sprite,actions:Sequence[str])->None:
        self.state = State.OFF
        self.sprite = sprite
        self.actions = {}
        for action in actions:
            pass

    def __del__(self)->None:
        pass

    def change_state(self)->None:
        pass

    def trigger_actions(self, state:State)->None:
        pass

def load_switches(switch_list:list[dict[str,int]],gates:dict[str,str|int])->Sequence[Switch]:
    switches:list[Switch] = []
    for switch in switch_list:
        print(switch)
    return switches