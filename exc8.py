import sys
import traceback
import math
import random
import libpyAI as ai
from optparse import OptionParser

#
# Global variables that persist between ticks
#
tickCount = 0
mode = "ready"
selfSpeed = None
velocityvector = None
selfX = None
selfY = None
selfVelX = None
selfVelY = None
targetX = None
targetY = None
selfHeading = None
selfTracking = None
visibleItems = None
visiblePlayers = []
latestChatMessage = None
missionstarted = None
mine_id = 8
missile_id = 9
fuel_id = 0
emergencyshield_id = 15
laser_id = 11
armor_id = 20
phasing_id = 18


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
        global selfVelX
        global selfVelY
        global targetX
        global targetY
        global selfSpeed
        global selfHeading
        global selfTracking
        global velocityvector
        global visibleItems
        global visiblePlayers
        global latestChatMessage
        global missionstarted

        if not ai.selfAlive():
            tickCount = 0
            mode = "ready"
            return

        tickCount += 1
        selfX = ai.selfX()
        selfY = ai.selfY()
        selfVelX = ai.selfVelX()
        selfVelY = ai.selfVelY()
        velocityvector = math.atan2(selfVelY, selfVelX)

        selfSpeed = ai.selfSpeed()
        selfTracking = ai.selfTrackingRad()
        selfHeading = ai.selfHeadingRad()
        visibleItems = ai.itemCountScreen()
        latestChatMessage = ai.scanGameMsg(0)
        selfHeading = ai.selfHeadingRad()

        visiblePlayers = []
        for i in range(ai.shipCountScreen()):
            visiblePlayers.append(ai.playerName(i))

        interpretMessage(latestChatMessage)

        if not missionstarted:
            ai.talk("teacherbot: start-mission 8")
            missionstarted = True

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

    global targetX
    global targetY

    itemtype = None

    if "collect-item" in message.lower():

        if "mine" in message.lower():
            itemtype = mine_id
        if "missile" in message.lower():
            itemtype = missile_id
        if "fuel" in message.lower():
            itemtype = fuel_id
        if "emergencyshield" in message.lower():
            itemtype = emergencyshield_id
        if "armor" in message.lower():
            itemtype = armor_id
        if "phasing" in message.lower():
            itemtype = phasing_id

        for i in range(ai.itemCountScreen()):
            if ai.itemType(i) == itemtype:
                targetX = ai.itemX(i)
                targetY = ai.itemY(i)
                targetVelX = ai.itemVelX(i)
                targetVelY = ai.itemVelY(i)
                navigateTo(targetX, targetY, targetVelX, targetVelY)
                break


def navigateTo(targetX, targetY, targetVelX, targetVelY):

    targetX = targetX - selfX
    targetY = targetY - selfY
    vx = targetVelX - selfVelX
    vy = targetVelY - selfVelY

    targetdistance = ( ( targetX ** 2) + ( targetY ** 2) ) ** (1 / 2)

    #a power of 45 (default) gives an acceleration of 0.1 pixels/tick^2 (with no friction)
    acceleration = 0.1 / 3
    ai.setPower(15)

    time_one = (-selfSpeed / acceleration) + math.sqrt(((selfSpeed ** 2) / (acceleration ** 2)) + ((2 * targetdistance) / acceleration))
    time_two = (-selfSpeed / acceleration) - math.sqrt(((selfSpeed ** 2) / (acceleration ** 2)) + ((2 * targetdistance) / acceleration))

    time = max(time_one, time_two)

    uppe = targetY + (vy * time)
    nere = targetX + (vx * time)

    aimDirection = math.atan2(uppe, nere)

    ai.turnToRad(aimDirection)
    ai.thrust()



parser = OptionParser()

parser.add_option ("-p", "--port", action="store", type="int",
                   dest="port", default=15345,
                   help="The port number. Used to avoid port collisions when"
                   " connecting to the server.")

(options, args) = parser.parse_args()


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


name = "Stub" +  str(random.randint(0,9999))

#
# Start the AI
#

ai.start(tick,["-name", name,
               "-join",
               "-turnSpeed", "64",
               "-turnResistance", "0",
               "-port", str(options.port)])
