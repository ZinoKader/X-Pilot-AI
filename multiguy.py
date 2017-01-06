import sys
import traceback
import math
import libpyAI as ai
from optparse import OptionParser
from multiguystatemachine import *
from chathandler import *

multiguy = None
chathandler = None
tickCount = 0

def tick():

    try:

        global tickCount
        global mode
        global multiguy
        global chathandler

        if not ai.selfAlive():
            tickCount = 0
            mode = "ready"
            return

        tickCount += 1

        if mode == "ready":
            pass

        if not chathandler:
            chathandler = ChatHandler(ai)
        else:
            chathandler.add_latest_messages()
            chathandler.interpret_latest_message()

        if not multiguy:
            multiguy = MultiGuyStateMachine(ai)


    except:
        print(traceback.print_exc())



parser = OptionParser()

parser.add_option ("-p", "--port", action="store", type="int",
                   dest="port", default=15345,
                   help="The port number. Used to avoid port collisions when"
                   " connecting to the server.")

(options, args) = parser.parse_args()

name = "MultiGuy"

ai.start(tick,["-name", name,
               "-join",
               "-turnSpeed", "64",
               "-turnResistance", "0",
               "-port", str(options.port)])
