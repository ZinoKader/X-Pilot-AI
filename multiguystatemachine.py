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


    def set_instruction_handler(self, instructionhandler):
        self.instructionhandler = instructionhandler


    def findpath(self, coordinates):
        if self.states.is_ready() and not self.states.is_attacking(): # prioriterar attack före findpath
            self.states.set_current_state("pathfinding")
            navigator = Navigator(self.ai, MapHandler(self.ai))
            navigator.navigateTo(coordinates)


    def attack(self, target = None):
        self.states.set_current_state("attacking") # alltid högsta prioritet
        attacker = Attacker(self.ai)
        if target:
            attacker.attack_player(target)
        else:
            attacker.attack_nearest()
