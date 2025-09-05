from mesa import Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler

from walls import *
from ghosts import *
from poi import *
from hero import *

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
        self.ghosts.add_poi(self.poi)
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
        self.heroes_array = [Hero]
        for position in self.initial_positions:
            hero = Hero(self)
            (hero.x, hero.y) = position
            self.heroes.place_agent(hero, position)
            self.heroes_array.append(hero)
            self.schedule.add(hero)
            print(hero.pos)

        self.current_hero = 0

    # ? Verificar si se va a quedar step(Todo el turno) o turn(Solo un héroe)
    def step(self):
        """Realiza una ronda completa de turnos."""

        self.schedule.step() # Ejecuta un turno en cada agente

    def turn(self):
        """Realiza únicamente el turno del próximo héroe."""

        self.heroes_array[self.current_hero].step()
        self.current_hero = (self.current_hero + 1) % 6

    def game_over(self):
        """Verifica si con el estado actual del tablero, el
        juego ya acabó o aún no.
        """

        if self.damage_points >= 24 or self.poi.scared_victims >= 4:
            self.win = False
            return True
        
        if self.poi.rescued_victims >= 7:
            self.win = True
            return True
        
        return False