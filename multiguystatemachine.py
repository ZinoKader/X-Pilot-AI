import sys
sys.path.append('pathfinding')
sys.path.append('attacking')
from navigator import *
from maphelper import *
from states import *

class MultiGuyStateMachine:

    def __init__(self, ai):
        self.ai = ai
        self.states = StateHandler()

    def findpath(self, coordinates):
        if self.states.is_ready():
            self.states.set_current_state("pathfinding")
            navigator = Navigator(self.ai, MapHandler(self.ai))
            navigator.navigateTo(coordinates)

    def attack(self, target):
        if self.states.is_ready():
            self.states.set_current_state("attacking")
            
