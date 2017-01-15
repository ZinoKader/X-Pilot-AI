import sys
sys.path.append('pathfinding')
sys.path.append('attacking')
from navigator import *
from attacker import *
from roamer import *
from maphelper import *
from states import *

class MultiGuyStateMachine:


    def __init__(self, ai):
        self.ai = ai
        self.states = StateHandler()


    def set_instruction_handler(self, instructionhandler):
        self.instructionhandler = instructionhandler


    def roam(self):
        if self.states.is_ready() or self.states.is_roaming():
            self.states.set_current_state("roaming")
            roamer = Roamer(self.ai, Navigator(self.ai, MapHandler(self.ai)))
            roamer.roam_random()


    def findpath(self, coordinates):
        if not self.states.is_attacking(): # prioriterar attack före findpath
            self.states.set_current_state("pathfinding")
            navigator = Navigator(self.ai, MapHandler(self.ai))
            if navigator.navigation_finished(coordinates):
                self.instructionhandler.finish_latest_instruction()
            else:
                navigator.navigate(coordinates)
        else:
            print("Must be in either states [ready, pathfinding] and not in state [attacking] to pathfind")


    def attack(self, target = None):
        self.states.set_current_state("attacking") # alltid högsta prioritet
        attacker = Attacker(self.ai)
        if target and not attacker.target_alive(target):
            self.instructionhandler.finish_latest_instruction()
        elif target:
            attacker.attack_player(target)
        else:
            attacker.attack_nearest()
