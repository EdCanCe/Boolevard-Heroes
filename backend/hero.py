from mesa import Agent
import numpy as np
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
        self.map.heroes.move_agent((x, y))

    def step(self):
        """Realiza un turno."""

        # Verifica si aún puede jugar
        if self.map.game_over():
            return

        self.action_points = self.stored_action_points + 4 # Se actualizan sus puntos de acción

        # Verifica si se hace un movimiento naive, o con strat
        if self.map.naiveSimulation:
            # Realiza acciones hasta quedarse sin puntos
            while self.action_points > 0:
                possible_actions = ActionList.generate_list(self)

                np.random.shuffle(possible_actions)

                # Realiza una acción aleatoria
                for action in possible_actions:
                    if action.do_action(): # Verifica que se haya completado
                        break

        # Cambiar el ciclo, mejor tenerlo afuera, y que dentro haya una u otra. ya que independientemente, al final de el subturno, va a tener que revelar pois en caso de que haya, y añadir los que falten si es que hay menos de 3

        else:
            print("")
            
        # TODO: Independientemente del tipo de simulación, se tiene que colocar fuego y verificar pois