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

        selfX = ( ai.selfRadarX() / ai.radarWidth() ) * ai.mapWidthPixels()
        selfY = ( ai.selfRadarY() / ai.radarHeight() ) * ai.mapHeightPixels()
        selfVelX = ai.selfVelX()
        selfVelY = ai.selfVelY()
        selfSpeed = ai.selfSpeed()
        velocityvector = math.atan2(ai.selfVelY(), ai.selfVelX())

        targetdistance = 0
        targetlist = {}
        for i in range(targetCountScreen):
            targetdistance = ai.radarDist(i)
            targetlist[targetdistance] = i

        targetId = targetlist.get(min(targetlist))

        selfHeading = ai.selfHeadingRad()

        bulletspeedx = (30 * math.cos(selfHeading)) + selfSpeed
        bulletspeedy = (30 * math.sin(selfHeading)) + selfSpeed
        bulletspeed = ( (bulletspeedx ** 2) + (bulletspeedy ** 2) ) ** (1 / 2)

        px = ai.asteroidX(targetId) - selfX
        vx = ai.asteroidVelX(targetId) - selfVelX

        py = ai.asteroidY(targetId) - selfY
        vy = ai.asteroidVelY(targetId) - selfVelY

        s = bulletspeed
        t = time_of_impact(px, py, vx, vy, s)

        uppe = py + (vy * t)
        nere = px + (vx * t)

        if selfSpeed > 8:
            ai.turnToRad(velocityvector + math.pi)
            ai.thrust()

        aimDirection = math.atan2(uppe, nere)

        #print ("tick count:", tickCount, "mode", mode)

        if mode == "wait":
            if targetCountScreen > 0:
                mode = "shoot"

        elif mode == "shoot":

            if targetCountScreen == 0:
                mode = "wait"
                return
            elif selfSpeed < 8:
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

    a = (s * s) - ( (vx * vx) + (vy * vy) )
    b = (px * vx) + (py * vy)
    c = (px * px) + (py * py)

    d = (b * b) + (a * c)

    t = 0
    if d >= 0:
        t = (b + math.sqrt(d)) / a
        if t < 0:
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
