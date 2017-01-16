import sys
sys.path.append('../roaming')
from maphelper import *
import helpfunctions

class Roamer:

    def __init__(self, ai, navigator):
        self.ai = ai
        self.navigator = navigator
        self.random_free_coordinates = helpfunctions.find_free_random_position(self.ai)
        self.maphelper = MapHandler(ai)

    def roam_random(self):
        if self.random_free_coordinates and self.maphelper.coords_to_block(self.random_free_coordinates[0], self.random_free_coordinates[1]) != self.maphelper.coords_to_block(self.ai.selfX(), self.ai.selfY()):
            self.navigator.navigate(self.random_free_coordinates)
        else:
            self.random_free_coordinates = helpfunctions.find_free_random_position(self.ai)
            self.navigator.navigate(self.random_free_coordinates)
