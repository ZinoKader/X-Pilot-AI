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
targetVelX = None
targetVelY = None
selfHeading = None
selfTracking = None
visibleItems = None
visiblePlayers = []
latestChatMessage = None
missionstarted = None

itemRequests = {"mine" : 0, "missile" : 0, "fuel" : 0, "emergencyshield" : 0, "laser" : 0, "armor" : 0, "phasing" : 0}
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
        global targetVelX
        global targetVelY
        global selfSpeed
        global selfHeading
        global selfTracking
        global velocityvector
        global visibleItems
        global visiblePlayers
        global latestChatMessage
        global missionstarted
        global itemRequests

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
        selfHeading = ai.selfHeadingRad()

        latestChatMessage = ai.scanGameMsg(0)
        interpretMessage(latestChatMessage)

        if not missionstarted:
            ai.talk("teacherbot: start-mission 8")
            missionstarted = True

        if not latestChatMessage:
            handleItem("escape")

        if mode == "ready":
            pass

        elif mode == "escape":
            targetX = targetX - selfX
            targetY = targetY - selfY
            relTargetVelX = targetVelX - selfVelX
            relTargetVelY = targetVelY - selfVelY
            targetdistance = ( ( targetX ** 2) + ( targetY ** 2) ) ** (1 / 2)
            acceleration = 0.1 / 2.25
            ai.setPower(20)

            time_one = (-selfSpeed / acceleration) + math.sqrt(((selfSpeed ** 2) / (acceleration ** 2)) + ((2 * targetdistance) / acceleration))
            time_two = (-selfSpeed / acceleration) - math.sqrt(((selfSpeed ** 2) / (acceleration ** 2)) + ((2 * targetdistance) / acceleration))

            time = max(time_one, time_two)

            uppe = targetY + (relTargetVelY * time)
            nere = targetX + (relTargetVelX * time)

            aimDirection = math.atan2(uppe, nere)

            ai.turnToRad(aimDirection + math.pi)
            ai.thrust()


        elif mode == "thrust":
            targetX = targetX - selfX
            targetY = targetY - selfY
            relTargetVelX = targetVelX - selfVelX
            relTargetVelY = targetVelY - selfVelY

            targetdistance = ( ( targetX ** 2) + ( targetY ** 2) ) ** (1 / 2)

            #a power of 45 (default) gives an acceleration of 0.1 pixels/tick^2 (with no friction)
            #we put the ship on one side of the map, took the time that the ship took to get to the other side
            #and worked out the acceleration (0.1) from there.
            acceleration = 0.1 / 3
            ai.setPower(15)

            time_one = (-selfSpeed / acceleration) + math.sqrt(((selfSpeed ** 2) / (acceleration ** 2)) + ((2 * targetdistance) / acceleration))
            time_two = (-selfSpeed / acceleration) - math.sqrt(((selfSpeed ** 2) / (acceleration ** 2)) + ((2 * targetdistance) / acceleration))

            time = max(time_one, time_two)

            uppe = targetY + (relTargetVelY * time)
            nere = targetX + (relTargetVelX * time)

            aimDirection = math.atan2(uppe, nere)

            ai.turnToRad(aimDirection)
            ai.thrust()

        print(mode)


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

    if "collect-item" in message.lower():
        handleItem(message.lower())

def handleItem(message):
    global mode
    global targetX
    global targetY
    global targetVelX
    global targetVelY

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

    itemdistance = {}
    for i in range(ai.itemCountScreen()):
        itemdistance[ai.itemDist(i)] = i
    closestitem = itemdistance.get(min(itemdistance))

    if "escape" in message.lower() or (ai.itemDist(closestitem) < 80 and ai.itemType(closestitem) != itemtype):
        targetX = ai.itemX(closestitem)
        targetY = ai.itemX(closestitem)
        targetVelX = ai.itemVelX(closestitem)
        targetVelY = ai.itemVelY(closestitem)
        mode = "escape"
    else:
        for itemindex in range(ai.itemCountScreen()):
            if ai.itemType(itemindex) == itemtype:
                targetX = ai.itemX(itemindex)
                targetY = ai.itemY(itemindex)
                targetVelX = ai.itemVelX(itemindex)
                targetVelY = ai.itemVelY(itemindex)
                mode = "thrust"
                break
            else:
                mode = "ready"

def getInventoryItems(itemId):
    return ai.selfItem(itemId)

parser = OptionParser()
parser.add_option ("-p", "--port", action="store", type="int",
                   dest="port", default=15345,
                   help="The port number. Used to avoid port collisions when"
                   " connecting to the server.")

(options, args) = parser.parse_args()

name = "Stub" +  str(random.randint(0,9999))

#
# Start the AI
#

ai.start(tick,["-name", name,
               "-join",
               "-turnSpeed", "64",
               "-turnResistance", "0",
               "-port", str(options.port)])
