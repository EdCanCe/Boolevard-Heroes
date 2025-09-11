from imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from poi import *
    from ghosts import *
    from map import *
    from hero import *
    from actions import *

class Walls:
    """Representa el tablero de juego con paredes y puertas.

    La clase maneja un tablero compuesto por dos matrices:
        - vertical: paredes y puertas verticales (entre columnas)
        - horizontal: paredes y puertas horizontales (entre filas)

    Cada valor en las matrices representa el estado de la pared o puerta:
         -1   -> fuera de límites
         0   -> vacío o pared destruida
         0.5 -> pared dañada
         1   -> pared completa
         2   -> puerta abierta
         3   -> puerta cerrada
         4   -> puerta destruida

    Attributes:
        vertical (list[list[float]]): Matriz de paredes y puertas verticales.
        horizontal (list[list[float]]): Matriz de paredes y puertas horizontales.
    """

    def __init__(self):
        """Inicializa las matrices de paredes y puertas."""

        # Matriz de paredes/puertas verticales (columnas)
        self.vertical = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 3, 0, 1, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 3, 0, 0, 1, 0],
            [2, 0, 3, 0, 0, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 0, 0, 3, 0, 2, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 1, 0],
            [1, 0, 0, 0, 0, 3, 0, 3, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        # Matriz de paredes/puertas horizontales (filas)
        self.horizontal = [
            [0, 1, 1, 1, 1, 1, 2, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 3, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 2, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.exits = [(6, 0), (0, 3), (9, 4), (3, 7)]

    # Getters
    def get_left(self, x, y):
        """Devuelve el estado de la pared/puerta a la izquierda de (x, y)."""
        if x <= 0:
            return -1  # Fuera de límites
        return self.vertical[y][x - 1]

    def get_right(self, x, y):
        """Devuelve el estado de la pared/puerta a la derecha de (x, y)."""
        if x >= 9:
            return -1  # Fuera de límites
        return self.vertical[y][x]

    def get_up(self, x, y):
        """Devuelve el estado de la pared/puerta arriba de (x, y)."""
        if y <= 0 or y >= 8:
            return -1  # Fuera de límites

        return self.horizontal[y - 1][x]

    def get_down(self, x, y):
        """Devuelve el estado de la pared/puerta abajo de (x, y)."""
        if y >= 7:
            return -1  # Fuera de límites
        return self.horizontal[y][x]
    
    # Setters
    def set_left(self, x, y, value):
        """Asigna un valor a la pared/puerta izquierda de (x, y)."""
        if y in [1, 9] and value in [0, 2, 4] and (x, y) not in self.exits:
            self.exits.append((x, y))

        if x <= 0:
            return  # Fuera de límites
        self.vertical[y][x - 1] = value

    def set_right(self, x, y, value):
        """Asigna un valor a la pared/puerta derecha de (x, y)."""
        if y in [8, 0] and value in [0, 2, 4] and (x, y) not in self.exits:
            self.exits.append((x, y))

        if x >= 9:
            return  # Fuera de límites
        self.vertical[y][x] = value

    def set_up(self, x, y, value):
        """Asigna un valor a la pared/puerta arriba de (x, y)."""
        if y in [1, 7] and value in [0, 2, 4] and (x, y) not in self.exits:
            self.exits.append((x, y))

        if y <= 0 or y >= 8:
            return  # Fuera de límites
        self.horizontal[y - 1][x] = value

    def set_down(self, x, y, value):
        """Asigna un valor a la pared/puerta abajo de (x, y)."""
        if y in [6, 0] and value in [0, 2, 4] and (x, y) not in self.exits:
            self.exits.append((x, y))

        if y >= 7:
            return  # Fuera de límites
        self.horizontal[y][x] = value

    # Obtención de casillas adyacentes
    def get_neighbors(self, x, y):
        """Obtiene las casillas adyacentes accesibles desde (x, y).

        Una casilla es vecina si no hay pared, o si hay una puerta abierta
        o destruida.
        """
        neighbors = []
        accepted_values = [0, 2, 4]  # Valores que representan adyacencia

        # Verifica si las casillas de alrededor son adyacentes
        if self.get_left(x, y) in accepted_values:
            neighbors.append((x - 1, y))

        if self.get_right(x, y) in accepted_values:
            neighbors.append((x + 1, y))

        if self.get_up(x, y) in accepted_values:
            neighbors.append((x, y - 1))

        if self.get_down(x, y) in accepted_values:
            neighbors.append((x, y + 1))

        return neighbors
    
    def get_closed_neighbors(self, x, y):
        """Obtiene las casillas adyacentes desde (x, y) donde
        haya una puerta de por medio.
        """

        neighbors = []
        
        # Verifica si las casillas de tienen puerta
        if self.get_left(x, y) == 3:
            neighbors.append((x - 1, y))

        if self.get_right(x, y) == 3:
            neighbors.append((x + 1, y))

        if self.get_up(x, y) == 3:
            neighbors.append((x, y - 1))

        if self.get_down(x, y) == 3:
            neighbors.append((x, y + 1))

        return neighbors