import math
import helpfunctions

class Navigator:

    def __init__(self, ai):
        self.ai = ai
        self.pathlist = []

    def navigateTo(self, xcoords, ycoords, maphandler):

        targetX = int(xcoords)
        targetY = int(ycoords)
        selfX = self.ai.selfX()
        selfY = self.ai.selfY()

        self_block = maphandler.coords_to_block(selfX, selfY)
        target_block = maphandler.coords_to_block(targetX, targetY)

        if self_block == target_block:
            self.ai.talk("teacherbot: move-to-pass {}, {} completed".format(targetX, targetY))
            print("navigation completed")

        # om vi hamnar på vilospår, hämta ny pathlist
        if not self.pathlist or self_block not in self.pathlist:
            self.pathlist = maphandler.get_path(self_block, target_block)

        while self_block in self.pathlist: # förhindra att vi åker tillbaka (bugg)
            self.pathlist.remove(self_block)

        if self.pathlist:
            next_move_block = (self.pathlist[0][0], self.pathlist[0][1])
            next_move_coords = maphandler.block_to_coords(next_move_block)

            targetDirection = math.atan2(next_move_coords[1] - selfY, next_move_coords[0] - selfX)
            self.ai.turnToRad(targetDirection)
            self.ai.setPower(8)
            # thrusta endast när vi har nästa block i sikte så vi inte thrustar in i väggar
            if helpfunctions.angleDiff(self.ai.selfHeadingRad(), targetDirection) < 0.1:
                self.ai.thrust()
