from walls import *
from ghosts import *
from poi import *
from mesa import Model
from mesa.space import MultiGrid

class Map(Model):
    """El mapa donde se correrá la simulación."""
    def __init__(self):
        """Constructor del mapa."""
        super().__init__()

        # La creación de las diferentes matrices
        self.walls = Walls()
        self.ghosts = Ghosts(self.walls)
        self.poi = POI(self.ghosts)
        self.ghosts.add_map(self.poi)
        self.heroes = MultiGrid(10, 8, torus = False)

        self.damage_points = 0 # El daño actual del mapa

        print("Ay cabrón")
        print(self.ghosts.poi.pick_poi())

Map()