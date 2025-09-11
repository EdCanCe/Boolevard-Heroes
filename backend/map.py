from imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from walls import *
    from poi import *
    from ghosts import *
    from hero import *
    from actions import *

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
        self.num_steps = 0

        self.damage_points = 0 # El daño actual del mapa
        self.naiveSimulation = naiveSimulation

        self.win = False

        # Las posiciones iniciales de los héroes
        self.initial_positions = [
            (6, 0),
            (9, 4),
            (3, 7),
            (0, 3),
            (4, 7),
            (5, 0)
        ]

        self.spawn_points = [
            (6, 0),
            (5, 0),
            (9, 4),
            (9, 3),
            (3, 7),
            (4, 7),
            (0, 3),
            (0, 4),
        ]

        # Se añaden los héroes al tablero
        self.heroes_array = []
        counter = 1
        for position in self.initial_positions:
            hero = Hero(self, counter)
            (hero.x, hero.y) = position
            self.heroes.place_agent(hero, position)
            self.heroes_array.append(hero)
            self.schedule.add(hero)
            counter += 1

        self.current_hero = 0

    # ? Verificar si se va a quedar step(Todo el ronda) o turn(Solo un héroe)
    def step(self):
        """Realiza una ronda completa de turnos."""

        self.schedule.step() # Ejecuta un turno en cada agente

    def turn(self):
        """Realiza únicamente el turno del próximo héroe."""

        json = self.heroes_array[self.current_hero].step()
        self.current_hero = (self.current_hero + 1) % 6
        self.num_steps += 1
        return json

    def game_over(self):
        """Verifica si con el estado actual del tablero, el
        juego ya acabó o aún no.
        """

        if self.poi.rescued_victims >= 7:
            self.win = True
            return True
        
        if self.poi.scared_victims >= 4 or self.damage_points >= 24:
            if self.damage_points > 24: self.damage_points = 24
            self.win = False
            return True
        
        return False