import sys
sys.path.append('/pathfinding')
import binary_heap as pf

class MapHandler:

    def __init__(self, ai):
        self.ai = ai
        self.tilemap = []
        self.map_block_width = ai.mapWidthBlocks()
        self.map_block_height = ai.mapHeightBlocks()
        self.block_size = ai.blockSize()

    def create_tile_map(self):

        for y in range(self.map_block_height - 1, -1, -1):
            tilemap_row = []
            for x in range(self.map_block_width):
                if self.ai.mapData(x, y) != 1:
                    tilemap_row += [0]
                else:
                    tilemap_row += [1]
            self.tilemap.append(tilemap_row)

    def get_path(self, start, end):
        maplist = self.tilemap
        path = pf.astar(maplist, start, end) # start kan ex. vara (3, 0) och end kan vara (3, 6) (x, y)
        print(path)
        return path

    def block_to_coords(self, block):
        # dessa blir mellan 0 till 1
        block_number_x = (block[0] - 1)/ self.map_block_width # t.ex. 15 / 30 för mellersta blocket
        block_number_y = (block[1] - 1)/ self.map_block_height # t.ex. 1 / 30 för blocket längst upp

        xcoords = block_number_x * self.ai.mapWidthPixels()
        ycoords = block_number_y * self.ai.mapHeightPixels()

        return (int(xcoords), int(ycoords))

    def coords_to_block(self, x, y):
        block_number_x =  1 + (x / self.ai.mapWidthPixels()) * self.map_block_width
        block_number_y =  1 + (y / self.ai.mapHeightPixels()) * self.map_block_height

        return (int(block_number_x), int(block_number_y))
