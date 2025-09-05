from mesa import Agent
import numpy as np

# Con ChatGPT se encontró como evitar importes circulares
# No ayudó a la lógica del código, solo a eso.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from map import *
    from actions import *

class Hero(Agent):
    """El héroe que hará acciones por el mapa para tratar
    de salvar a las 7 víctimas.
    """

    def __init__(self, model : "Map"):
        """Constructor del héroe.

        Args:
            model (Map): El mapa del tablero.
        """
        super().__init__(model)

        # Atributos necesarios para ejecutar las acciones
        self.map = model
        self.neighbors = []
        self.action_points = 0
        self.stored_action_points = 0
        self.has_victim = False

    def update_position(self, x, y):
        """Modifica la posición del héroe

        Args:
            x (int): La coordenada en X.
            y (int): La coordenada en Y.
        """
        self.map.heroes.move_agent(self, (x, y))
        self.x = x
        self.y = y

    def step(self):
        """Realiza un turno."""

        from actions import ActionList

        # Verifica si aún puede jugar
        if self.map.game_over():
            return

        self.action_points = self.stored_action_points + 4 # Se actualizan sus puntos de acción

        # Realiza acciones hasta quedarse sin puntos
        while self.action_points > 0:
            # Verifica si se hace un movimiento naive, o con strat
            if self.map.naiveSimulation: # Simulación naive
                possible_actions = ActionList.generate_list(self)

                np.random.shuffle(possible_actions)

                # Realiza una acción aleatoria
                for action in possible_actions:
                    if action.do_action(): # Verifica que se haya completado
                        break
                    else: # Si no pudo hacerla, restaura los puntos de acción
                        action.restore_action_points()

            else: # TODO: Simulación con estrategia
                print("")

            # Independientemente de la simulación, verifica si reveló POI
            if self.map.poi.get(self.x, self.y) == 3:
                if self.map.poi.pick(self.x, self.y) == 4: # Si es una víctima real
                    if not self.has_victim: # En caso de que no lleve a nadie
                        self.has_victim = True
                        self.map.poi.willBeRescued(self.x, self.y) # Quito en el mapa la víctima
                else: # Si es una falsa alarma
                    self.map.poi.remove(self.x, self.y)

            elif self.map.poi.get(self.x, self.y) == 4 and not self.has_victim: # Que alguien más lo reveló pero no lo agarró
                self.has_victim = True
                self.map.poi.willBeRescued(self.x, self.y) # Quito en el mapa la víctima

        # Después de los movimientos del héroe, finalizo el turno
        self.map.ghosts.place_fog() # Coloca la niebla

        while self.map.poi.current < 3: # Coloca POIs si es que hay menos de 3
            self.map.poi.place(self.map.heroes)

        if self.map.ghosts.get_on(self.x, self.y): # Si se extendieron los fantasmas a mi casilla
            if self.has_victim: # Si estaba con una víctima, se asusta
                self.map.poi.scared_victims += 1
                self.has_victim = False

            self.to_closest_spawn_point() # Lo lleva al spawnpoint
            self.stored_action_points = 0 # Se eliminan puntos de acción guardados

        # TODO: Aquí se crearía un JSON que se regresaría en la función

    def to_closest_spawn_point(self):
        """Mueve el héroe al spawn point más cercano."""

        closest_spawn_point = (0, 0, 1000)

        # Busca la distancia más corta entre los spawnpoints
        for spawn_point in self.map.spawn_points:
            distance = abs(spawn_point[0] - self.x) + abs(spawn_point[1] - self.y) # Obtiene la distancia manhattan

            if distance < closest_spawn_point[2]: # Verifica que sea más cercano
                closest_spawn_point = (spawn_point[0], spawn_point[1], distance)

        self.update_position(closest_spawn_point[0], closest_spawn_point[1])