import sys
import traceback
import math
import libpyAI as ai
from optparse import OptionParser
from multiguystatemachine import *
from instructionhandler import *

multiguy = None
instructionhandler = None
tickCount = 0

def tick():

    try:

        global tickCount
        global multiguy
        global instructionhandler

        if not ai.selfAlive():
            tickCount = 0
            return

        tickCount += 1

        if not multiguy:
            multiguy = MultiGuyStateMachine(ai)

        if not instructionhandler:
            instructionhandler = InstructionHandler(ai, multiguy)
            multiguy.set_instruction_handler(instructionhandler)
        else:
            instructionhandler.add_latest_messages()
            instructionhandler.interpret_latest_message()



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
