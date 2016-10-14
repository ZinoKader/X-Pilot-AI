#
# This file can be used as a starting point for the bot in exercise 1
#

import sys
import traceback
import math
import os
import libpyAI as ai
from optparse import OptionParser


#
# Create global variables that persist between ticks.
#

tickCount = 0
mode = "wait"
targetId = -1

def tick():
    #
    # The API won't print out exceptions, so we have to catch and print them ourselves.
    #
    try:

        #
        # Declare global variables so we're allowed to use them in the function
        #

        global tickCount
        global mode
        global targetId

        #
        # Reset the state machine if we die.
        #
        if not ai.selfAlive():
            tickCount = 0
            mode = "aim"
            return

        tickCount += 1


        #
        # Read some "sensors" into local variables to avoid excessive calls to the API
        # and improve readability.
        #
        selfX = ai.selfX()
        selfY = ai.selfY()
        selfHeading = ai.selfHeadingRad()
        # 0-2pi, 0 in x direction, positive toward y

        targetCount = ai.targetCountServer()
        #print statements for debugging, either here or further down in the code.
        # Useful functions: round(), math.degrees(), math.radians(), etc.
        # os.system('clear') clears the terminal screen, which can be useful.()
        targetCountAlive = 0

        for i in range(targetCount):
            if ai.targetAlive(i):
                targetCountAlive += 1

        # Use print statements for debugging, either here or further down in the code.
        # Useful functions: round(), math.degrees(), math.radians(), etc.
        # os.system('clear') clears the terminal screen, which can be useful.

        targetlist = {}
        for i in range(targetCount):
            if ai.targetAlive(i):
                targetdistance = ( ( (ai.targetX(i) - selfX) ** 2) + ( (ai.targetY(i) - selfY) ** 2) ) ** (1 / 2)
                targetlist[targetdistance] = i

        targetId = targetlist.get(min(targetlist))
        print("current targetId: " + str(targetId))
        targetX = ai.targetX(targetId) - selfX
        targetY = ai.targetY(targetId) - selfY

        print(targetX)
        print(targetY)
        print(targetlist)

        targetdistance = ( ( targetX ** 2) + ( targetY ** 2) ) ** (1 / 2)
        targetDirection = math.atan2(targetY, targetX)
        print(targetDirection)

        velocity = ((ai.selfVelX() ** 2) + (ai.selfVelY() ** 2)) ** (1 / 2)
        velocityvector = math.atan2(ai.selfVelY(), ai.selfVelX())

        print("tick count:", tickCount, "mode:", mode, "heading:",round(math.degrees(selfHeading)), "targets alive:", targetCountAlive)

        if mode == "wait":
            if targetCountAlive > 0:
                mode = "aim"

        elif mode == "aim":
            if targetCountAlive == 0:
                mode = "wait"
                return

            if velocity < 15 and tickCount % 3 == 0:
                ai.turnToRad(targetDirection)
                ai.setPower(40)
                ai.thrust()
            elif velocity > 15:
                ai.turnToRad(velocityvector + math.pi)
                ai.setPower(55)
                ai.thrust()

            angledifference = angleDiff(selfHeading, targetDirection)

            if angledifference <= 0.05 and targetdistance < 600:
                mode = "shoot"
            else:
                mode = "aim"

        elif mode == "shoot":

            if not ai.targetAlive(targetId):
                mode = "aim"
            else:
                if velocity > 10 and tickCount % 5 == 0 and targetdistance > 600:
                    ai.turnToRad(velocityvector + math.pi)
                    ai.setPower(55)
                    ai.thrust()
                elif targetdistance < 250: #spin-circus compensation. Will eventually fully stop if the ship keeps spinning around a target.
                    if velocity > 5:
                        ai.turnToRad(velocityvector + math.pi)
                        ai.setPower(55)
                        ai.thrust()
                    else:
                        ai.turnToRad(targetDirection)
                        ai.fireShot()
                elif targetdistance < 600:
                    ai.turnToRad(targetDirection)
                    ai.setPower(55)
                    ai.thrust()
                    ai.fireShot()
                elif targetdistance > 800:
                    mode = "aim"

    except:
        #
        # If tick crashes, print debugging information
        #
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
        help="The port to use. Used to avoid port collisions when"
        " connecting to the server.")

(options, args) = parser.parse_args()

name = "Exc. 1 skeleton" #Feel free to change this

#
# Start the main loop. Callback are done to tick.
#

ai.start(tick, ["-name", name,
    "-join",
    "-turnSpeed", "64",
    "-turnResistance", "0",
    "-port", str(options.port)])
