from navigator import *

class MultiGuyStateMachine(object):

    mode = "ready"

    def __init__(self, ai):
        self.ai = ai

    def findpath(xcoords, ycoords):
        maphandler = maphelper.MapHandler(self.ai)
        navigator = Navigator(self.ai)
        navigator.navigateTo(xcoords, ycoords, maphandler)
