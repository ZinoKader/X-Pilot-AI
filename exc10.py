#starting server with map xpilots
#xpilots -map maps/obstacle1.xp -noQuit \ +reportToMetaServer -port 15390

import sys
sys.path.append('pathfinding')
import traceback
import math
import libpyAI as ai
from optparse import OptionParser
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
originalheading = None
desiredheading = None
escape_turned = False
selfTracking = None
visibleItems = None
visiblePlayers = []
latestChatMessage = None
missionstarted = False
missioncompleted = False
instructionstack = []
finishedinstructions = []
chatmessages = []

def tick():

    try:

        global tickCount
        global mode
        global escape_turned
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
        global missioncompleted
        global instructionstack
        global finishedinstructions
        global chatmessages
        global maphandler
        global pathlist
        global originalheading
        global desiredheading


        if not ai.selfAlive():
            tickCount = 0
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

        if instructionstack and mode == "ready":
            interpretMessage(instructionstack[-1])

        if not missionstarted and not missioncompleted:
            ai.talk("teacherbot: start-mission 10")
            missionstarted = True

        if not maphandler:
            maphandler = maphelper.MapHandler(ai)

        if ai.wallFeelerRad(50, selfHeading) != -1: # om vägg är inom 60px av hastighetsvektorn
            mode = "escapewall"
        else:
            mode = "ready"

        if mode == "ready":
            escape_turned = False # resetta för nästa escape event
            originalheading = None
            desiredheading = None
        elif mode == "escapewall":
            if not escape_turned:
                escape_turned = True
                print("ESCAAAAAAAAAAAAAAAAAAPEEEEE")
                originalheading = velocityvector
                desiredheading = originalheading + math.pi
                ai.turnToRad(desiredheading)
            else:
                ai.turnToRad(desiredheading)
                ai.setPower(55)
                ai.thrust()



    except:
        print(instructionstack)
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

        message = message.replace(xcoords, "", 1) # ta bort en gång (ifall x och y-koordinaterna är samma)
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
    global missioncompleted

    """
    Testa denna också
    http://code.activestate.com/recipes/578919-python-a-pathfinding-with-binary-heap/
    """

    targetX = int(xcoords)
    targetY = int(ycoords)

    self_block = maphandler.coords_to_block(selfX, selfY)
    target_block = maphandler.coords_to_block(targetX, targetY)

    if self_block == target_block and missionstarted and not missioncompleted:
        missioncompleted = True
        ai.talk("teacherbot: move-to-pass {}, {} completed".format(targetX, targetY))
        print("navigation completed")

    # om vi hamnar på vilospår, hämta ny pathlist
    if self_block not in pathlist:
        pathlist = maphandler.get_path(self_block, target_block)
    elif not pathlist: # om vi inte hämtat ett spår än, gör det
        pathlist = maphandler.get_path(self_block, target_block)

    while self_block in pathlist: # förhindra att vi åker tillbaka (bugg)
        pathlist.remove(self_block)

    if mode == "ready" and pathlist:
        next_move_block = (pathlist[0][0], pathlist[0][1])
        next_move_coords = maphandler.block_to_coords(next_move_block)

        targetDirection = math.atan2(next_move_coords[1] - selfY, next_move_coords[0] - selfX)
        ai.turnToRad(targetDirection)
        ai.setPower(8)
        # thrusta endast när vi har nästa block i sikte så vi inte thrustar in i väggar
        if angleDiff(selfHeading, targetDirection) < 0.1:
            ai.thrust()

        if tickCount % 1 == 0:
            print("mode: " + mode)
            print("Current pos: " + str(selfX) + ", " + str(selfY))
            print("self block" + str(self_block))
            print("NEXT MOVE: " + str(next_move_block))
            print("target block" + str(target_block))
            print("--PATHLIST--")
            print(pathlist)
            print("\n")


def distanceTo(dist1, dist2):
    if dist1 > dist2:
        return dist1 - dist2
    else:
        return dist2 - dist1

def angleDiff(one, two):
    """Calculates the smallest angle between two angles"""

    a1 = (one - two) % (2*math.pi)
    a2 = (two - one) % (2*math.pi)
    return min(a1, a2)

parser = OptionParser()

parser.add_option ("-p", "--port", action="store", type="int",
                   dest="port", default=15345,
                   help="The port number. Used to avoid port collisions when"
                   " connecting to the server.")

(options, args) = parser.parse_args()

name = "Stub"

ai.start(tick,["-name", name,
               "-join",
               "-turnSpeed", "64",
               "-turnResistance", "0",
               "-port", str(options.port)])
