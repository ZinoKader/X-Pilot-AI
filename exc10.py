#starting server with map xpilots
#xpilots -map exc10_map_try.xp -noQuit \ +reportToMetaServer -port 15390

import sys
sys.path.append('pathfinding')
import traceback
import math
import libpyAI as ai
from optparse import OptionParser
import binary_heap as pf
import tilemap as tm
import maphelper

maphandler = None
pathlist = []
tickCount = 0
mode = "ready"
selfSpeed = None
velocityvector = None
selfX = None
selfY = None
selfHeading = None
selfTracking = None
visibleItems = None
visiblePlayers = []
latestChatMessage = None
missionstarted = False
instructionstack = []
finishedinstructions = []
chatmessages = []

def tick():

    try:

        global tickCount
        global mode
        global selfX
        global selfY
        global selfSpeed
        global selfHeading
        global selfTracking
        global velocityvector
        global visibleItems
        global visiblePlayers
        global latestChatMessage
        global missionstarted
        global instructionstack
        global finishedinstructions
        global chatmessages
        global maphandler
        global pathlist


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

        for i in range(10):
            if ai.scanGameMsg(i) not in chatmessages:
                chatmessages.append(ai.scanGameMsg(i))

        latestChatMessage = ai.scanGameMsg(0)

        for message in chatmessages:
            if "move" in message and "completed" not in message and message not in instructionstack and message not in finishedinstructions:
                instructionstack.append(message)

        if instructionstack:
            interpretMessage(instructionstack[-1])

        if not missionstarted:
            #ai.talk("teacherbot: start-mission 10")
            missionstarted = True

        if mode == "ready":
            pass

        if tickCount % 60 == 0:
            print(str(len(instructionstack)))
            print((selfX, selfY))

        if not maphandler:
            maphandler = maphelper.MapHandler(ai)
            maphandler.create_tile_map()


    except:
        print(instructionstack)
        print(traceback.print_exc())
        print(selfY)
        print(selfX)


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
    if "move-to-pass" in message.lower() or "move-to-stop" in message.lower():
        moveinstruction = message[:12]
        message = message.replace(moveinstruction, "")
        message = message.strip()

        xcoords = ""
        for char in message:
            if char == " ":
                break
            if char in "0123456789":
                xcoords += char

        message = message.replace(xcoords, "")
        message = message.strip()

        ycoords = ""
        for char in message:
            if char == " ":
                break
            if char in "0123456789":
                ycoords += char

        navigateTo(xcoords, ycoords)


def navigateTo(xcoords, ycoords):
    global pathlist

    """
    Testa denna också
    http://code.activestate.com/recipes/578919-python-a-pathfinding-with-binary-heap/
    """

    targetX = int(xcoords)
    targetY = int(ycoords)

    self_block = maphandler.coords_to_block(selfX, selfY)
    target_block = maphandler.coords_to_block(targetX, targetY)

    if not pathlist:
        pathlist = maphandler.get_path(self_block, target_block)

    next_move_block = (pathlist[0][0], pathlist[0][1])
    next_move_coords = maphandler.block_to_coords(next_move_block)

    if tickCount % 60 == 0:
        print(pathlist)
        print("FUCK")
        print(maphandler.coords_to_block(next_move_coords[0], next_move_coords[1]))

    if maphandler.coords_to_block(next_move_coords[0], next_move_coords[1]) == self_block:
        del(pathlist[0])

    targetDirection = math.atan2(next_move_coords[0] - selfX, next_move_coords[1] - selfY)
    ai.turnToRad(targetDirection)
    ai.setPower(8)
    ai.thrust()


    if tickCount % 10 == 0:
        print("Current pos: " + str(selfX) + ", " + str(selfY))
        print("NEXT MOVE: " + str(next_move_coords))
        print("BLOCK SIZE: " + str(ai.blockSize()))
        print(self_block)
        print(target_block)
        print("\n")


def distanceTo(dist1, dist2):
    if dist1 > dist2:
        return dist1 - dist2
    else:
        return dist2 - dist1

parser = OptionParser()

parser.add_option ("-p", "--port", action="store", type="int",
                   dest="port", default=15345,
                   help="The port number. Used to avoid port collisions when"
                   " connecting to the server.")

(options, args) = parser.parse_args()

name = "Stub"

ai.start(tick,["-name", name,
               "-join",
               "-turnSpeed", "3",
               "-turnResistance", "0",
               "-port", str(options.port)])
