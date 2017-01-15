from maphelper import *

class Roamer:

    def __init__(self, ai):
        self.ai = ai

    def roam_random(self):
        navigator = Navigator(self.ai, MapHandler(self.ai))
        
