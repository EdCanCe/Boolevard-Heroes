from walls import *
from ghosts import *
from poi import *
from hero import *
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler

class Map(Model):
    """El mapa donde se correrá la simulación."""
    def __init__(self, naiveSimulation):
        """Constructor del modelo.

        Args:
            naiveSimulation (bool): Bandera que dicta si el modelo es naive o con strat.
        """
        super().__init__()

        self.schedule = BaseScheduler(self)

        # La creación de las diferentes matrices
        self.walls = Walls()
        self.ghosts = Ghosts(self.walls)
        self.poi = POI(self.ghosts)
        self.ghosts.add_map(self.poi)
        self.heroes = MultiGrid(10, 8, torus = False)

        self.damage_points = 0 # El daño actual del mapa
        self.naiveSimulation = naiveSimulation

        # Las posiciones iniciales de los héroes
        self.initial_positions = [
            (6, 0),
            (9, 4),
            (3, 7),
            (0, 3),
            (4, 7),
            (5, 0)
        ]

        # Se añaden los héroes al tablero
        for position in self.initial_positions:
            hero = Hero(self)
            self.heroes.place_agent(hero, position)
            self.schedule.add(hero)
            print(hero.pos)

    def step(self):
        """Cada ronda que se hace en la simulación"""
        self.schedule.step() # Ejecuta un turno en cada agente

    def game_over(self):
        if self.damage_points >= 26:
            return True
        # TODO: Poner más condiciones para terminar el juego
        
simulation = Map(0)