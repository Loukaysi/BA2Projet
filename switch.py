from dataclasses import dataclass
from enum import Enum, auto
from typing import Final, Sequence
from arcade import Sprite
from subsprite import SubSprite
from common_types import pos_int

class Gate(SubSprite):
    
    gate_position:Final[pos_int]
    
    def __init__(self, sprite:Sprite,gate_position:pos_int, opened:bool = False)->None:
        super().__init__(sprite)
        self.gate_position = gate_position
        if opened: self.scale = (0,0)

    def set_state(self, opened:bool)->None:
        if opened : self.scale = (0,0)
        else: self.scale = (0.5,0.5)

@dataclass
class Handle_Gate:
    gate:Gate
    open:bool

class State(Enum):
    ON=auto()
    OFF=auto()
    DISABLED=auto()

Raw_Action_type = dict[str,str|int]
Action = State | Handle_Gate

class Switch(SubSprite):
    state:State = State.OFF
    actions: dict[State,list[Action]]

    def __init__(self,sprite:Sprite,state:bool=False, gates:dict[pos_int,Gate] = {},
                 switch_on_actions:Sequence[Raw_Action_type]=[],switch_off_actions:Sequence[Raw_Action_type]=[])->None:
        if state:
            self.state = State.ON
        else:
            self.state = State.OFF
        super().__init__(sprite)
        self.actions = {State.ON:[State.OFF],State.OFF:[State.ON]}
        self.read_actions(switch_off_actions,State.OFF,gates)
        self.read_actions(switch_on_actions,State.ON,gates)

    def read_actions(self,actions:Sequence[Raw_Action_type], switch_to:State, gates:dict[pos_int,Gate]={})->None:
        for action in actions:
            match action['action']:
                case 'open-gate':
                    gate_position = (int(action['x']),int(action['y']))
                    gate = gates[gate_position]
                    self.actions[switch_to].append(Handle_Gate(gate,True))
                case 'close-gate':
                    gate_position = (int(action['x']),int(action['y']))
                    gate = gates[gate_position]
                    self.actions[switch_to].append(Handle_Gate(gate,False))
                case 'disable': self.actions[switch_to].append(State.DISABLED)

    def toggle_state(self)->None:
        display_texture_n:int
        match self.state:
            case State.ON:display_texture_n = 0
            case State.OFF:display_texture_n = 1
            case State.DISABLED: pass
        self.set_texture(display_texture_n)

    def trigger_actions(self)->None:
        if self.state != State.DISABLED:
            self.toggle_state()
            for action in self.actions[self.state]:
                match action:
                    case State(): self.state = action
                    case Handle_Gate(): action.gate.set_state(action.open)