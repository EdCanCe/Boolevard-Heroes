from walls import *
from ghosts import *
from poi import *

class Map:
    def __init__(self):
        self.walls = Walls()
        self.ghosts = Ghosts(self.walls)
        self.poi = POI(self.ghosts)

        print(self.walls.get_neighbors(1,1))