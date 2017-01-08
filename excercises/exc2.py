#
# This file can be used as a starting point for the bots.
#

import sys
import traceback
import math
import libpyAI as ai
from optparse import OptionParser

#
# Global variables that persist between ticks
#
tickCount = 0
mode = "ready"
# add more if needed

def tick():
    #
    # The API won't print out exceptions, so we have to catch and print them ourselves.
    #
    try:
        #
        global tickCount
        global mode

        #
        # Reset the state machine if we die.
        #
        if not ai.selfAlive():
            tickCount = 0
            mode = "ready"
            return

        tickCount += 1

        #
        # Read some "sensors" into local variables, to avoid excessive calls to the API
        # and improve readability.
        #

        selfX = ai.selfX()
        selfY = ai.selfY()
        selfVelX = ai.selfVelX()
        selfVelY = ai.selfVelY()
        selfSpeed = ai.selfSpeed()

        selfHeading = ai.selfHeadingRad()
        # 0-2pi, 0 in x direction, positive toward y

        checkpoint = ai.nextCheckpoint()

        checkpointX = ai.checkpointX(checkpoint) - selfX
        checkpointY = ai.checkpointY(checkpoint) - selfY

        #https://www.youtube.com/watch?v=k1tsGGz-Qw0
        highonpotenuse = ( (checkpointX ** 2) + (checkpointY ** 2) ) ** (1 / 2)
        centerX = 400 - selfX
        centerY = 400 - selfY

        if highonpotenuse < 250:
            targetDirection = math.atan2(centerY, centerX)
            mode = "stop"
        else:
            mode = "travel"
            targetDirection = math.atan2(checkpointY, checkpointX)

        ai.turnToRad(targetDirection)

        angledifference = angleDiff(selfHeading, targetDirection)


        if angledifference <= 0.05:
            mode = "travel"


        if mode == "ready":
            pass

        if mode == "travel":
            ai.setPower(40)
            ai.thrust()

        if mode == "stop":
            ai.turnRad(math.pi)
            ai.setPower(55)
            ai.thrust()

        if mode == "shoot":
            ai.fireShot()


        #print debug info every tenth tick to avoid congestion
            if tickCount % 10 == 0:
                print("\n")
                #print(str(highonpotenuse))
                print("X:" + str(selfX))
                print("Y:" + str(selfY))
                print(str(checkpoint))

    except:
        print(traceback.print_exc())



def angleDiff(one, two):
    """Calculates the smallest angle between two angles"""

    a1 = (one - two) % (2*math.pi)
    a2 = (two - one) % (2*math.pi)
    return min(a1, a2)


#
# Parse the command line arguments
#
parser = OptionParser()

parser.add_option ("-p", "--port", action="store", type="int",
                   dest="port", default=15345,
                   help="The port number. Used to avoid port collisions when"
                   " connecting to the server.")

(options, args) = parser.parse_args()

name = "Stub"

#
# Start the AI
#

ai.start(tick,["-name", name,
               "-join",
               "-turnSpeed", "64",
               "-turnResistance", "0",
               "-port", str(options.port)])
