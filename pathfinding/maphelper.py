import astar as poopstar
import implementation as astar

class MapHandler:

    def __init__(self, ai):
        self.ai = ai
        self.tilemap = []
        self.map_block_width = ai.mapWidthBlocks()
        self.map_block_height = ai.mapHeightBlocks()
        self.block_size = ai.blockSize()

    def find_walls(self):
        walls = []
        for y in range(self.map_block_height - 1, -1, -1):
            for x in range(self.map_block_width):
                if self.ai.mapData(x, y) == 1:
                    walls.append( (x, y) )
        return walls

    def create_tile_map(self):

        for y in range(self.map_block_height - 1, -1, -1):
            tilemap_row = []
            for x in range(self.map_block_width):
                if self.ai.mapData(x, y) != 1:
                    tilemap_row += [0] # Empty space
                else:
                    tilemap_row += [1] # Wall block
            self.tilemap.append(tilemap_row)

    def is_wall(block):
        blockx = block[0]
        blocky = block[1]
        iswall = self.tilemap[blocky][blockx]:
        return iswall == 1 # 1 är vägg, True om blocket är en vägg

    def get_path(self, start, goal):
        """
        finder = astar.pathfinder(self.ai, astar.grid_neighbors(self.map_block_width - 1, self.map_block_height - 1))
        path = finder(start, end)
        """
        mapgrid = astar.SquareGrid(32, 32)
        mapgrid.walls = self.find_walls()
        path = astar.a_star_search(mapgrid, start, goal)
        return path

    def block_to_coords(self, block):
        # dessa blir mellan 0 till 1
        """block_number_x = (block[0]) / self.map_block_width # t.ex. 15 / 30 för mellersta blocket
        block_number_y = (block[1]) / self.map_block_height # t.ex. 1 / 30 för blocket längst upp

        xcoords = block_number_x * self.ai.mapWidthPixels() + self.block_size / 2
        ycoords = block_number_y * self.ai.mapHeightPixels() + self.block_size / 2"""

        xcoords = block[0] * self.block_size + (self.block_size / 2) # Add half block to get center coords
        ycoords = block[1] * self.block_size + (self.block_size / 2)

        return (int(xcoords), int(ycoords))

    def coords_to_block(self, x, y):
        """block_number_x = (x / self.ai.mapWidthPixels()) * (self.map_block_width)
        block_number_y = (y / self.ai.mapHeightPixels()) * (self.map_block_height)"""

        block_number_x = x / self.block_size
        block_number_y = y / self.block_size

        return (int(block_number_x), int(block_number_y))
