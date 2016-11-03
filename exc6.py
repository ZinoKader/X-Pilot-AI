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
selfX = None
selfY = None
selfHeading = None
selfTracking = None
visibleItems = None
visiblePlayers = []
latestChatMessage = None
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
        global selfX
        global selfY
        global selfHeading
        global selfTracking
        global visibleItems
        global visiblePlayers
        global latestChatMessage

        #
        # Reset the state machine if we die.
        #
        if not ai.selfAlive():
            tickCount = 0
            mode = "ready"
            return

        tickCount += 1


        selfX = ai.selfX()
        selfY = ai.selfY()
        selfVelX = ai.selfVelX()
        selfVelY = ai.selfVelY()
        selfSpeed = ai.selfSpeed()
        selfTracking = ai.selfTrackingRad()
        selfHeading = ai.selfHeadingRad()
        visibleItems = ai.itemCountScreen()
        latestChatMessage = ai.scanGameMsg(0)

        visiblePlayers = []
        for i in range(ai.shipCountScreen()):
            visiblePlayers.append(ai.playerName(i))

        interpretMessage(latestChatMessage)

        if mode == "ready":
            pass


    except:
        print(traceback.print_exc())



def getCoordinates():
    return (selfX, selfY)

def getHeading():
    return selfHeading

def getTracking():
    return selfTracking

def getVisibleItems():
    return visibleItems

def getVisiblePlayers():
    return visiblePlayers

def getLatestChatMessage():
    return latestChatMessage

def sendMessage(message):
    if tickCount % 2 == 0:
        message = str(message)
        ai.talk(message)

def interpretMessage(message):
    if "coord" in message.lower():
        sendMessage(getCoordinates())
    if "heading" in message.lower():
        sendMessage(getHeading())
    if "tracking" in message.lower():
        sendMessage(getTracking())
    if "item" in message.lower():
        sendMessage(getVisibleItems())
    if "player" in message.lower():
        sendMessage(getVisiblePlayers())

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
