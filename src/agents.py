from enum import Enum, auto

class State(Enum):
    S = auto()
    I = auto()
    R = auto()

class Agent:
    def __init__(self, idx, compliant=True):
        self.idx = idx
        self.state = State.S
        self.days_in_state = 0
        self.compliant = compliant
