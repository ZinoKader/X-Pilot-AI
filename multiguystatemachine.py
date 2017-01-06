import sys
sys.path.append('pathfinding')
from navigator import *
from maphelper import *

class MultiGuyStateMachine:

    mode = "ready"

    def __init__(self, ai):
        self.ai = ai

    def findpath(self, xcoords, ycoords):
        maphandler = MapHandler(self.ai)
        navigator = Navigator(self.ai)
        navigator.navigateTo(xcoords, ycoords, maphandler)
