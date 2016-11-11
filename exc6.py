#
# This file can be used as a starting point for the bots.
#

import sys
import traceback
import math
import libpyAI as ai
import random
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
comm_role = None
requester_questions = ["requesting... give me your coords", "requesting... hand over some headings, will ya?",\
 "requesting... tracking please", "requesting... what items do you see?", "requesting... wanna tell me about the players on the screen?"]

def tick():

    try:

        global tickCount
        global mode
        global selfX
        global selfY
        global selfHeading
        global selfTracking
        global visibleItems
        global visiblePlayers
        global latestChatMessage


        if not ai.selfAlive():
            tickCount = 0

        selfX = ai.selfX()
        selfY = ai.selfY()
        selfVelX = ai.selfVelX()
        selfVelY = ai.selfVelY()
        selfSpeed = ai.selfSpeed()
        selfTracking = ai.selfTrackingRad()
        selfHeading = ai.selfHeadingRad()
        visibleItems = ai.itemCountScreen()
        latestChatMessage = ai.scanTalkMsg(0)

        visiblePlayers = []
        for i in range(ai.shipCountScreen()):
            visiblePlayers.append(ai.playerName(i))

        allPlayers = []
        for i in range(ai.playerCountServer()):
            allPlayers.append(ai.playerName(i))

        setRole(allPlayers)

        if comm_role == "requester" and "requesting" not in latestChatMessage:
            if not latestChatMessage:
                ai.talk(requester_questions[0])
            elif "answerer" in latestChatMessage:
                if "coord" in latestChatMessage:
                    ai.talk(requester_questions[1])
                elif "heading" in latestChatMessage:
                    ai.talk(requester_questions[2])
                elif "tracking" in latestChatMessage:
                    ai.talk(requester_questions[3])
                elif "item" in latestChatMessage:
                    ai.talk(requester_questions[4])


        interpretMessage(latestChatMessage)

        text_file = open("Output.txt", "a")
        text_file.write(latestChatMessage + "\n")
        text_file.close()


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
    global comm_role

    message = str(message)
    ai.talk(message)

def setRole(players):
    global comm_role

    self_name = ai.selfName()
    self_id = int(self_name.replace("Bot",""))

    players.remove(self_name)

    other_name = players[0]
    other_id = int(other_name.replace("Bot",""))

    if self_id > other_id:
        comm_role = "requester"
    else:
        comm_role = "answerer"
    print(comm_role)


def interpretMessage(message):
    global comm_role

    if comm_role == "answerer" and "requesting" in message.lower() and "answerer" not in latestChatMessage:
        if "coord" in message.lower():
            sendMessage(comm_role + "," + "coord," + str(getCoordinates()))
        elif "heading" in message.lower():
            sendMessage(comm_role + "," + "heading," + str(getHeading()))
        elif "tracking" in message.lower():
            sendMessage(comm_role + "," + "tracking," + str(getTracking()))
        elif "item" in message.lower():
            sendMessage(comm_role + "," + "item," + str(getVisibleItems()))
        elif "player" in message.lower():
            sendMessage(comm_role + "," + "player," + str(getVisiblePlayers()))

parser = OptionParser()

parser.add_option ("-p", "--port", action="store", type="int",
                   dest="port", default=15345,
                   help="The port number. Used to avoid port collisions when"
                   " connecting to the server.")

(options, args) = parser.parse_args()

name = "Bot" + str(random.randint(0,9999))


ai.start(tick,["-name", name,
               "-join",
               "-turnSpeed", "64",
               "-turnResistance", "0",
               "-port", str(options.port)])
