from transitions import Machine
import random

# https://github.com/tyarkoni/transitions#quickstart

class StateMachine(object):

    states = ['sleeping', 'roaming', 'pathfinding', 'attacking', 'bulletdodging', 'walldodging']

    def __init__(self, name):

        self.name = name

        self.kittens_rescued = 0

        self.machine = Machine(model=self, states=StateMachine.states, initial='roaming')

        self.machine.add_transition(trigger="findpath", source="*", dest="pathfinding")
        self.machine.add_transition(trigger="attack", source="*", dest="attacking")
        self.machine.add_transition(trigger="dodgebullet", source="*", dest="bulletdodging")

        self.machine.add_transition('clean_up', 'sweaty', 'asleep', conditions=['is_exhausted'])

    def is_exhausted(self):
        """ Basically a coin toss. """
        return random.random() < 0.5
