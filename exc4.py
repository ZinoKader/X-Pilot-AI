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
            mode = "shoot"
            return

        tickCount += 1

        targetCountScreen = ai.asteroidCountScreen()

        selfX = ai.selfX()
        selfY = ai.selfY()
        selfVelX = ai.selfVelX()
        selfVelY = ai.selfVelY()
        selfSpeed = ai.selfSpeed()

        targetdistance = 0
        targetlist = {}
        for i in range(targetCountScreen):
            targetdistance = ai.asteroidDist(i)
            targetlist[targetdistance] = i

        targetId = targetlist.get(min(targetlist))

        selfHeading = ai.selfHeadingRad()

        targetDirection = math.atan2(ai.asteroidY(targetId) - selfY, ai.asteroidX(targetId) - selfX)

        #print ("tick count:", tickCount, "mode", mode)

        px = ai.asteroidX(targetId) - selfX
        py = ai.asteroidY(targetId) - selfY
        vx = ai.asteroidVelX(targetId) - selfVelX
        vy = ai.asteroidVelY(targetId) - selfVelY

        bulletspeedx = (21 * math.cos(selfHeading)) + selfSpeed
        bulletspeedy = (21 * math.sin(selfHeading)) + selfSpeed
        bulletspeed = ( (bulletspeedx ** 2) + (bulletspeedy ** 2) ) ** (1 / 2)

        reltargetspeedX = ( ai.asteroidSpeed(targetId) * math.cos(ai.asteroidVelX(targetId)) ) + selfSpeed
        reltargetspeedY = ( ai.asteroidSpeed(targetId) * math.sin(ai.asteroidVelY(targetId)) ) + selfSpeed
        reltargetspeed = ( (reltargetspeedX ** 2) + (reltargetspeedY ** 2) ) ** (1 / 2)

        impacttime = time_of_impact(px, py, vx, vy, bulletspeed)

        aimDirection = targetDirection + ( reltargetspeed * impacttime )
        print(aimDirection)


        if mode == "wait":
            if targetCountScreen > 0:
                mode = "shoot"

        elif mode == "shoot":

            if targetCountScreen == 0:
                mode = "wait"
                return
            else:
                ai.turnToRad(aimDirection)
                ai.fireShot()

    except:
        print(traceback.print_exc())



def angleDiff(one, two):
    """Calculates the smallest angle between two angles"""

    a1 = (one - two) % (2*math.pi)
    a2 = (two - one) % (2*math.pi)
    return min(a1, a2)

def time_of_impact(px, py, vx, vy, s):

    a = s * s - (vx * vx + vy * vy)
    b = px * vx + py * vy
    c = px * px + py * py

    d = b*b + a*c

    t = 0;
    if (d >= 0):
        t = (b + math.sqrt(d)) / a
        if (t < 0):
            t = 0
    return t

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
