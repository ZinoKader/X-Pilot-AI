class Navigator:

    def __init__(self, ai):
        self.ai = ai

    def navigateTo(xcoords, ycoords, pathlist, maphandler):

        targetX = int(xcoords)
        targetY = int(ycoords)

        self_block = maphandler.coords_to_block(selfX, selfY)
        target_block = maphandler.coords_to_block(targetX, targetY)

        if self_block == target_block:
            self.ai.talk("teacherbot: move-to-pass {}, {} completed".format(targetX, targetY))
            print("navigation completed")

        # om vi hamnar på vilospår, hämta ny pathlist
        if self_block not in pathlist:
            pathlist = maphandler.get_path(self_block, target_block)
        elif not pathlist: # om vi inte hämtat ett spår än, gör det
            pathlist = maphandler.get_path(self_block, target_block)

        while self_block in pathlist: # förhindra att vi åker tillbaka (bugg)
            pathlist.remove(self_block)

        if pathlist:
            next_move_block = (pathlist[0][0], pathlist[0][1])
            next_move_coords = maphandler.block_to_coords(next_move_block)

            targetDirection = math.atan2(next_move_coords[1] - selfY, next_move_coords[0] - selfX)
            self.ai.turnToRad(targetDirection)
            self.ai.setPower(8)
            # thrusta endast när vi har nästa block i sikte så vi inte thrustar in i väggar
            if angleDiff(selfHeading, targetDirection) < 0.1:
                self.ai.thrust()
