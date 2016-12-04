import sys
sys.path.append('/pathfinding')
import pathfinders as pf
import tilemap as tm

class MapHandler:

    def __init__(self, ai):
        self.ai = ai
        self.tilemap = ""
        self.map_block_width = ai.mapWidthBlocks()
        self.map_block_height = ai.mapHeightBlocks()
        self.block_size = ai.blockSize()

    def create_tile_map(self):

        for x in range(self.map_block_width):
            for y in range(self.map_block_height):
                empty_space_list_index = [0,30,40,50,60]
                # https://www.ida.liu.se/~TDDD63/projects/2016/xpilot/mapdata.html
                if self.ai.mapData(x, y) in empty_space_list_index: # ingen vägg (empty space)
                    self.tilemap += "1"
                else: # något annat än empty space, räkna det som vägg
                    self.tilemap += "X"
        self.tilemap += "\n"

        print(self.tilemap)

    def get_path(self, start, end):
        maplist = tm.str_to_map(self.tilemap)
        path = pf.a_star(maplist, start, end) # start kan ex. vara (3, 0) och end kan vara (3, 6) (x, y)
        return path

    def block_to_coords(self, block):
        # dessa blir mellan 0 till 1
        block_number_x = block[0] / self.map_block_width # t.ex. 15 / 30 för mellersta blocket
        block_number_y = block[1] / self.map_block_height # t.ex. 1 / 30 för blocket längst upp

        xcoords = block_number_x * self.ai.mapWidthPixels()
        ycoords = block_number_y * self.ai.mapHeightPixels()

        return (int(xcoords), int(ycoords))

    def coords_to_block(self, x, y):
        block_number_x = (x / self.ai.mapWidthPixels()) * self.map_block_width
        block_number_y = (y / self.ai.mapHeightPixels()) * self.map_block_height

        return (int(block_number_x), int(block_number_y))
