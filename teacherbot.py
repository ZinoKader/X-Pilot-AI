#!/usr/bin/python3

#
# This file can be used as a starting point for the bots.
#

import sys
import traceback
import math
import libpyAI as ai
from optparse import OptionParser

from random import randint

#
# Global variables that persist between ticks
#
tickCount = 0
mode = "ready"
# add more if needed
msgs = []
mission = None

def get_free_random_position():
    mapwidth = ai.mapWidthPixels()
    mapheight = ai.mapHeightPixels()
    mapwblock = ai.mapWidthBlocks()
    maphblock = ai.mapHeightBlocks()
    dw = mapwidth/mapwblock
    dh = mapheight/maphblock

#    print("MAP:", mapwidth, mapheight, mapwblock, maphblock, dw, dh)
    
    found = False
    while not found:
        bx = randint(0, mapwblock-1)
        by = randint(0, maphblock-1)
        type = ai.mapData(bx, by)
        if type == 0:
            found = True
#    print("TYPE:", type, bx, by)

    x = int(bx*dw + dw/2)
    y = int(by*dh + dh/2)

    return (x, y)

def hold_position():
    if ai.selfSpeed() > 1:
        ai.turnToRad(ai.selfTrackingRad() + math.pi)
        ai.thrust()

class mission_7:
    def __init__(self, worker):
        self.mode = "ready"
        self.tick_count = 0
        self.worker = worker
        self.nwps = 5
        self.seqlen = 5
        self.oldmode = ""
    
    def tick(self):
        self.tick_count += 1

        if self.mode != self.oldmode:
            print("MODE:", self.mode)
            self.oldmode = self.mode

        if self.mode == "ready":
            if self.tick_count == 20:
                self.mode = "send-move-to-pass-order"

        elif self.mode == "send-move-to-pass-order":
            (x, y) = get_free_random_position ()
            if self.nwps > 0:
                if self.nwps == 1:                
                    msg = "{}:move-to-stop {} {}".format(self.worker, x, y)
                else:
                    msg = "{}:move-to-pass {} {}".format(self.worker, x, y)
                self.nwps -= 1
                print ("SEND:", msg)
                ai.talk(msg)
                self.mode = "wait-for-finished"
            else:
                self.mode = "finished"

        elif self.mode == "wait-for-finished":
            if len(msgs) > 0:
                msg = msgs[0]
                print("RECV:", msg)
                msgs.pop(0)
                fields = msg.split()
                if fields[0] == "completed":
                    if self.nwps == 0:
                        self.mode = "fly-sequence"
                    else:
                        self.mode = "send-move-to-pass-order"

        elif self.mode == "fly-sequence":
            for i in range(self.seqlen):
                (x, y) = get_free_random_position ()                
                if i == 4:                
                    msg = "{}:move-to-stop {} {}".format(self.worker, x, y)
                else:
                    msg = "{}:move-to-pass {} {}".format(self.worker, x, y)
                print ("SEND:", msg)
                ai.talk(msg)
            self.mode = "wait-for-finished-seq"

        elif self.mode == "wait-for-finished-seq":
            if len(msgs) > 0:
                msg = msgs[0]
                print("RECV:", msg)
                msgs.pop(0)
            

class mission_8:
    def __init__(self, worker):
        self.mode = "ready"
        self.tick_count = 0
        self.worker = worker
        self.itemindex = 0
        self.items = ["mine", "missile", "fuel", "emergencyshield", "laser", "armor"] 
        self.oldmode = ""
    
    def tick(self):
        self.tick_count += 1

        if self.mode != self.oldmode:
            print("MODE:", self.mode)
            self.oldmode = self.mode

        if self.mode == "ready":
            if self.tick_count == 20:
                self.mode = "send-collect-item-order"

        elif self.mode == "send-collect-item-order":
            if self.itemindex < len(self.items):
                msg = "{}:collect-item {}".format(self.worker, self.items[self.itemindex])
                self.itemindex += 1
                print ("SEND:", msg)
                ai.talk(msg)
                self.mode = "wait-for-finished"
            else:
                self.mode = "finished"

        elif self.mode == "wait-for-finished":
            if len(msgs) > 0:
                msg = msgs[0]
                print("RECV:", msg)
                msgs.pop(0)
                fields = msg.split()
                if fields[0] == "completed":
                    self.mode = "send-collect-item-order"


class mission_9:
    def __init__(self, worker):
        self.mode = "ready"
        self.tick_count = 0
        self.worker = worker
        self.itemindex = 0
        self.items = ["mine", "mine", "missile", "fuel", "emergencyshield", "laser", "armor"] 
        self.oldmode = ""
    
    def tick(self):
        self.tick_count += 1

        if self.tick_count % 2 == 0:
            hold_position()

        if self.mode != self.oldmode:
            print("MODE:", self.mode)
            self.oldmode = self.mode

        if self.mode == "ready":
            if self.tick_count == 20:
                self.mode = "send-use-item-order"

        elif self.mode == "send-use-item-order":
            if self.itemindex < len(self.items):
                item = self.items[self.itemindex]
                msg = "{}:use-item {} self".format(self.worker, item)
                if item == "mine" and self.itemindex == 0:
                    (x, y) = get_free_random_position()
                    msg = "{}:use-item {} {} {}".format(self.worker, item, x, y)
                elif item == "mine" or item == "missile" or item == "laser":
                    msg = "{}:use-item {} {}".format(self.worker, item, ai.selfName())

                self.itemindex += 1
                print ("SEND:", msg)
                ai.talk(msg)
                self.mode = "wait-for-finished"
            else:
                self.mode = "finished"

        elif self.mode == "wait-for-finished":
            if len(msgs) > 0:
                msg = msgs[0]
                print("RECV:", msg)
                msgs.pop(0)
                fields = msg.split()
                if fields[0] == "completed":
                    self.mode = "send-use-item-order"


class mission_10:
    def __init__(self, worker):
        self.mode = "ready"
        self.tick_count = 0
        self.worker = worker
        self.nwps = 5
        self.seqlen = 5
        self.oldmode = ""
    
    def tick(self):
        self.tick_count += 1

        if self.mode != self.oldmode:
            print("MODE:", self.mode)
            self.oldmode = self.mode

        if self.mode == "ready":
            if self.tick_count == 20:
                self.mode = "send-move-to-order"

        elif self.mode == "send-move-to-order":
            (x, y) = get_free_random_position ()
            if self.nwps > 0:
                msg = "{}:move-to-stop {} {}".format(self.worker, x, y)
                self.nwps -= 1
                print ("SEND:", msg)
                ai.talk(msg)
                self.mode = "wait-for-finished"
            else:
                self.mode = "finished"

        elif self.mode == "wait-for-finished":
            if len(msgs) > 0:
                msg = msgs[0]
                print("RECV:", msg)
                msgs.pop(0)
                fields = msg.split()
                if fields[0] == "completed":
                    if self.nwps == 0:
                        self.mode = "fly-sequence"
                    else:
                        self.mode = "send-move-to-order"

        elif self.mode == "fly-sequence":
            for i in range(self.seqlen):
                (x, y) = get_free_random_position ()                
                msg = "{}:move-to-stop {} {}".format(self.worker, x, y)
                print ("SEND:", msg)
                ai.talk(msg)
            self.mode = "wait-for-finished-seq"

        elif self.mode == "wait-for-finished-seq":
            if len(msgs) > 0:
                msg = msgs[0]
                print("RECV:", msg)
                msgs.pop(0)

# DEPRECATED!        
#class mission_11:
#    def __init__(self, worker):
#        self.mode = "ready"
#        self.tick_count = 0
#        self.worker = worker
#        self.nwps = 3
#        self.oldmode = ""
#        self.follower = ""
#    
#    def tick(self):
#        self.tick_count += 1
#
#        if self.mode != self.oldmode:
#            print("MODE:", self.mode)
#            self.oldmode = self.mode
#
#        if self.mode == "ready":
#            if self.tick_count == 20:
#                self.mode = "find-follower"
#
#        elif self.mode == "find-follower":
#            n = ai.playerCountServer()
#            badnames = ["Teacherbot", "Psycho", "Slugger", "Bonnie", "Hermes", 
#                        "Robby", "Sparky", "Pixie", "Boson", self.worker]
#            for i in range(n):
#                id = ai.playerId(i)
#                name = ai.playerName(i)
#                print("PLAYER:", id, name)
#                if name not in badnames:
#                    self.follower = name
#                    print("FOLLOWER:", name)
#            if self.follower != "":
#                self.mode = "send-follow-order"
#
#        elif self.mode == "send-follow-order":
#            msg = "{}:follow-agent {}".format(self.follower, self.worker)
#            print ("SEND:", msg)
#            ai.talk(msg)
#            self.mode = "send-move-to-order"
#
#        elif self.mode == "send-move-to-order":
#            (x, y) = get_free_random_position ()
#            if self.nwps > 0:
#                msg = "{}:move-to-stop {} {}".format(self.worker, x, y)
#                self.nwps -= 1
#                print ("SEND:", msg)
#                ai.talk(msg)
#                self.mode = "wait-for-finished"
#            else:
#                self.mode = "finished"
#
#        elif self.mode == "wait-for-finished":
#            if len(msgs) > 0:
#                msg = msgs[0]
#                print("RECV:", msg)
#                msgs.pop(0)
#                fields = msg.split()
#                if fields[0] == "completed":
#                    self.mode = "send-move-to-order"
#
        

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
        global msgs
        global mission

        #
        # Reset the state machine if we die.
        #
        if not ai.selfAlive():
            tickCount = 0
            mode = "ready"
            return

        tickCount += 1
#        print ("tick count:", tickCount, "mode", mode, selfX, selfY)

        ai.setMaxMsgs(15)
        maxmsgs = ai.getMaxMsgs()
#        print("MAXMSGS:", maxmsgs)

        for i in reversed(range(maxmsgs)):
            msg = ai.scanTalkMsg(i)
            if msg != "":
                try:
                    fields = msg.split()
                    fromto = fields[-1]
                    [fr, to] = fromto.split(":")
                    if to == "[Teacherbot]":
#                        print (i, ": ", msg)
                        msgs.append(msg)
                except:
                    print("Message not understood: ", msg)
                ai.removeTalkMsg(i)

        #
        # Check if top message on queue is swap mission
        #
        if len(msgs) > 0:
            msg = msgs[0]
            fields = msg.split()
            if fields[0] == "start-mission":
                print("RECV:", msg)
                msgs.pop(0)
                [sender, recv] = fields[2].split(":")
                sender = sender[1:-1]
                print("WORKER IS:", sender)
                if fields[1] == "7":
                    mission = mission_7(sender)
                if fields[1] == "8":
                    mission = mission_8(sender)
                if fields[1] == "9":
                    mission = mission_9(sender)
                if fields[1] == "10":
                    mission = mission_10(sender)
                if fields[1] == "11":
                    mission = mission_11(sender)

        if mission:
            mission.tick()

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

name = "teacherbot"

#
# Start the AI
#

ai.headlessMode()

ai.start(tick,["-name", name, 
               "-join",
               "-turnSpeed", "64",
               "-turnResistance", "0",
               "-port", str(options.port)])
