import sys
import traceback
import math
import random
import libpyAI as ai
from optparse import OptionParser

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
currenttask = None
instructionstack = []

minecount = 0
missilecount = 0
emergencyshieldcount = 0
armorcount = 0
lasercount = 0
fuelcount = 0
phasingcount = 0

mine_id = 8
missile_id = 9
fuel_id = 0
emergencyshield_id = 15
laser_id = 11
armor_id = 20
phasing_id = 18

def tick():

    try:
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
        global instructionstack
        global currenttask
        global minecount
        global missilecount
        global emergencyshieldcount
        global armorcount
        global lasercount
        global fuelcount
        global phasingcount

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

        if not missionstarted:
            ai.talk("teacherbot: start-mission 8")
            missionstarted = True

        chatmessages = []
        for i in range(10):
            if "collect-item" in ai.scanGameMsg(i) and "completed" not in ai.scanGameMsg(i):
                chatmessages.append(ai.scanGameMsg(i))

        for i in range(10):
            ai.removeTalkMsg(i)

        for message in chatmessages:
            if "collect-item" in message and "completed" not in message:
                instructionstack.append(message)

        if not currenttask:
            currenttask = instructionstack[0]
            instructionstack.pop(0)
            if "mine" in currenttask:
                minecount = ai.selfItem(getItemIndex("mine"))
            if "missile" in currenttask:
                missilecount = ai.selfItem(getItemIndex("missile"))
            if "fuel" in currenttask:
                fuelcount = ai.selfItem(getItemIndex("fuel"))
                ai.thrust() # to make sure fuelcount changes before next tick
            if "emergencyshield" in currenttask:
                emergencyshieldcount = ai.selfItem(getItemIndex("emergencyshield"))
            if "armor" in currenttask:
                armorcount = ai.selfItem(getItemIndex("armor"))
            if "phasing" in currenttask:
                phasingcount = ai.selfItem(getItemIndex("phasing"))
            if "laser" in currenttask:
                lasercount = ai.selfItem(getItemIndex("laser"))

        if "mine" in currenttask and ai.selfItem( getItemIndex( getItemName(currenttask) ) ) != minecount:
            ai.talk("teacherbot:completed collect-item mine")
            currenttask = None
        elif "missile" in currenttask and ai.selfItem( getItemIndex( getItemName(currenttask) ) ) != missilecount:
            ai.talk("teacherbot:completed collect-item missile")
            currenttask = None
        elif "fuel" in currenttask and ai.selfItem( getItemIndex( getItemName(currenttask) ) ) != fuelcount:
            ai.talk("teacherbot:completed collect-item fuel")
            currenttask = None
        elif "emergencyshield" in currenttask and ai.selfItem( getItemIndex( getItemName(currenttask) ) ) != emergencyshieldcount:
            ai.talk("teacherbot:completed collect-item emergencyshield")
            currenttask = None
        elif "armor" in currenttask and ai.selfItem( getItemIndex( getItemName(currenttask) ) ) != armorcount:
            ai.talk("teacherbot:completed collect-item armor")
            currenttask = None
        elif "phasing" in currenttask and ai.selfItem( getItemIndex( getItemName(currenttask) ) ) != phasingcount:
            ai.talk("teacherbot:completed collect-item phasing")
            currenttask = None
        elif "laser" in currenttask and ai.selfItem( getItemIndex( getItemName(currenttask) ) ) != lasercount:
            ai.talk("teacherbot:completed collect-item laser")
            currenttask = None

        if currenttask:
            interpretMessage(currenttask)

        print(instructionstack)

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
            acceleration = 0.1 / 3 # möjligen (0.1 / 3) * (1 - friktion)
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

def getItemName(currenttask):
    if "fuel" in currenttask:
        return "fuel"
    if "mine" in currenttask:
        return "mine"
    if "missile" in currenttask:
        return "missile"
    if "emergencyshield" in currenttask:
        return "emergencyshield"
    if "laser" in currenttask:
        return "laser"
    if "armor" in currenttask:
        return "armor"
    if "phasing" in currenttask:
        return "phasing"

def getItemIndex(itemname):
    if itemname == "fuel":
        return 0
    if itemname == "mine":
        return 8
    if itemname == "missile":
        return 9
    if itemname == "emergencyshield":
        return 15
    if itemname == "laser":
        return 11
    if itemname == "armor":
        return 20
    if itemname == "phasing":
        return 18

def interpretMessage(message):
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
    if "laser" in message.lower():
        itemtype = laser_id

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
