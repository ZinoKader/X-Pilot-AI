import sys
sys.path.append('../roaming')
from maphelper import *
import helpfunctions

class Roamer:

    def __init__(self, ai, navigator):
        self.ai = ai
        self.navigator = navigator

    def roam_random(self):
        random_free_coordinates = helpfunctions.find_free_random_position(self.ai)
        self.navigator.navigate(random_free_coordinates)
