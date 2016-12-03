import sys
sys.path.append('/pathfinding')
import pathfinders as pf
import tilemap as tm

class MapHandler(self, ai):

    def __init__(self):
        self.tilemap = ""

    def create_tile_map(self):

        map_block_width = ai.mapWidthBlocks()
        map_block_height = ai.mapHeightBlocks()

        for x in map_block_width:
            for y in map_block_height:
                # https://www.ida.liu.se/~TDDD63/projects/2016/xpilot/mapdata.html
                if ai.mapData(x, y) == 0: # ingen vägg (empty space)
                    self.tilemap += "1"
                else: # något annat än empty space, räkna det som vägg
                    self.tilemap += "X"
            self.tilemap += "\n"

    def get_path(self, start, end):
        maplist = tm.str_to_map(self.tilemap)
        path = pf.a_star(maplist, start, end) # start kan ex. vara (3, 0) och end kan vara (3, 6) (x, y)
