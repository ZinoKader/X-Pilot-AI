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
        # Declare global variables so we have access to them in the function
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

        itemCountScreen = ai.itemCountScreen()
        targetdistance = 0
        targetlist = {}

        selfX = ai.selfX()
        selfY = ai.selfY()
        selfVelX = ai.selfVelX()
        selfVelY = ai.selfVelY()
        selfSpeed = ai.selfSpeed()
        selfHeading = ai.selfHeadingRad()
        velocityvector = math.atan2(ai.selfVelY(), ai.selfVelX())

        for i in range(itemCountScreen):
            targetdistance = ai.itemDist(i)
            targetlist[targetdistance] = i

        if targetlist:
            targetId = targetlist.get(min(targetlist))
            targetX = ai.itemX(targetId) - selfX
            targetY = ai.itemY(targetId) - selfY
            targetDirection = math.atan2(targetY, targetX)
        else:
            targetDirection = math.atan2(ai.mapHeightPixels() / 2, ai.mapWidthPixels() / 2)

        distancelist = []
        for i in range(360):
            distancelist.append(ai.wallFeelerRad(110, (i * (math.pi / 180))))

        wallnear = True
        walldirection = None
        for i in distancelist:
            if i == -1:
                wallnear = False
            else:
                wallnear = True
                walldirection = distancelist[int(i)]
                break

        if selfSpeed > 8:
            ai.turnToRad(velocityvector + math.pi)
            ai.setPower(55)
            ai.thrust()

        if wallnear:
            if selfSpeed > 2:
                if mode != "breakwall" and mode != "escapewall":
                    mode = "breakwall"
                else:
                    mode = "escapewall"
        else:
            if selfSpeed > 10:
                ai.turnToRad(velocityvector + math.pi)
                ai.setPower(55)
                ai.thrust
            else:
                mode = "thrust"

        if mode == "ready":
            pass
        elif mode == "breakwall":
            ai.turnToRad(velocityvector + math.pi)
            ai.setPower(20)
            ai.thrust()
        elif mode == "escapewall":
            ai.setPower(55)
            ai.thrust()
        elif mode == "thrust":
            ai.turnToRad(targetDirection)
            ai.setPower(20)
            ai.thrust()

        print(mode)




    except:
        print(traceback.print_exc())


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
