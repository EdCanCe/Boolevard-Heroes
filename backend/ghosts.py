import numpy as np
from collections import deque
from walls import *

class Ghosts:
    """Gestiona la niebla y los fantasmas en el tablero de juego.

    La clase utiliza una matriz para representar la posición de la niebla
    y los fantasmas, con los siguientes valores posibles:
        -1  -> fuera de límites
        0  -> vacío
        1  -> niebla
        2  -> fantasma

    Attributes:
        dashboard (list[list[int]]): Matriz que representa la niebla y
            los fantasmas en cada casilla del tablero.
    """

    def __init__(self, walls):
        """Inicializa las variables de la clase y el tablero."""

        self.walls = walls  # Referencia a la clase Walls para comprobar vecinos

        # Matriz del tablero con fantasmas iniciales
        self.dashboard = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 2, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.fog_list = [] # lista de casillas con niebla

    # Métodos de generación de coordenadas aleatorias
    def generate_coords(self):
        """Genera coordenadas aleatorias dentro de los límites válidos del tablero.

        Returns:
            tuple[int, int]: Coordenadas (x, y) aleatorias.
        """
        x = np.random.randint(1, 9)
        y = np.random.randint(1, 7)
        return (x, y)

    # Getters de celdas adyacentes
    def get_up(self, x, y):
        """Devuelve el valor de la casilla arriba de (x, y)."""
        if y <= 1 or y >= 7:
            return -1  # Fuera de límites
        return self.dashboard[y - 1][x]

    def get_down(self, x, y):
        """Devuelve el valor de la casilla abajo de (x, y)."""
        if y <= 0 or y >= 6:
            return -1
        return self.dashboard[y + 1][x]

    def get_left(self, x, y):
        """Devuelve el valor de la casilla a la izquierda de (x, y)."""
        if x <= 1 or x >= 9:
            return -1
        return self.dashboard[y][x - 1]

    def get_right(self, x, y):
        """Devuelve el valor de la casilla a la derecha de (x, y)."""
        if x <= 0 or x >= 8:
            return -1
        return self.dashboard[y][x + 1]

    # Setters de celdas adyacentes
    def set_up(self, x, y, value):
        """Asigna un valor a la casilla arriba de (x, y)."""
        if y <= 1 or y >= 7:
            return
        self.dashboard[y - 1][x] = value

    def set_down(self, x, y, value):
        """Asigna un valor a la casilla abajo de (x, y)."""
        if y <= 0 or y >= 6:
            return
        self.dashboard[y + 1][x] = value

    def set_left(self, x, y, value):
        """Asigna un valor a la casilla a la izquierda de (x, y)."""
        if x <= 1 or x >= 9:
            return
        self.dashboard[y][x - 1] = value

    def set_right(self, x, y, value):
        """Asigna un valor a la casilla a la derecha de (x, y)."""
        if x <= 0 or x >= 8:
            return
        self.dashboard[y][x + 1] = value

    # Vecinos con niebla
    def get_ghosty_neighbors(self, x, y):
        """Obtiene las casillas vecinas que contienen fantasma y son adyacentes.

        Returns:
            list[tuple[int, int]]: Lista de coordenadas vecinas con fantasmas.
        """
        neighbors = self.walls.get_neighbors(x, y)  # Vecinos accesibles según Walls
        foggy_neighbors = []

        for current_x, current_y in neighbors:
            if self.dashboard[current_y][current_x] == 2:  # hay fantasma
                foggy_neighbors.append((current_x, current_y))

        return foggy_neighbors

    # Propagación de niebla/fantasmas
    def spread_fire(self, x, y):
        """Propaga la niebla convirtiéndola en fantasmas a través de vecinos accesibles."""
        q = deque()
        visited = set()

        q.append((x, y))
        visited.add((x, y))

        while q:
            current_x, current_y = q.popleft()
            neighbors = self.get_ghosty_neighbors(current_x, current_y)
            for new_x, new_y in neighbors:
                if (new_x, new_y) in visited:
                    continue

                visited.add((new_x, new_y))

                if self.dashboard[new_y][new_x] == 2:
                    self.dashboard[current_y][current_x] = 2
                    q.append((new_x, new_y))

    # Verificación de límites del tablero
    def board_length(self, x, y):
        """Verifica si las coordenadas (x, y) están dentro del tablero.

        Returns:
            bool: True si está dentro de límites, False si está fuera.
        """
        return 1 <= x <= 8 and 1 <= y <= 6

    # Explosión/oleada de fantasmas
    def arise(self, x, y):
        """Realiza una oleada de fantasmas desde la posición (x, y) propagándose 
        en todas las direcciones.
        """
        # Arriba, derecha, abajo, izquierda
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  

        for diff_x, diff_y in directions:
            current_x, current_y = (x, y)

            while True:
                new_x = current_x + diff_x
                new_y = current_y + diff_y
                out_of_bounds = not self.board_length(new_x, new_y)

                # Obtiene el valor de la pared o puerta en esa dirección
                # Derecha
                if diff_x == 1 and diff_y == 0:
                    value = self.walls.get_right(current_x, current_y)
                # Izquierda
                elif diff_x == -1 and diff_y == 0:
                    value = self.walls.get_left(current_x, current_y)
                # Arriba
                elif diff_x == 0 and diff_y == -1:
                    value = self.walls.get_up(current_x, current_y)
                # Abajo
                elif diff_x == 0 and diff_y == 1:
                    value = self.walls.get_down(current_x, current_y)
                else:
                    break

                if value == -1 or out_of_bounds:
                    break  # Límite del tablero

                can_pass = False
                can_end = False

                # Manejo de paredes y puertas según su estado
                # Pasa, daña, destruye o termina propagación según valor
                # Derecha
                if diff_x == 1 and diff_y == 0:
                    if value == 0:
                        can_pass = True
                    elif value == 0.5:
                        self.walls.set_right(current_x, current_y, 0)
                        can_end = True
                    elif value == 1:
                        self.walls.set_right(current_x, current_y, 0.5)
                        can_end = True
                    elif value in [2, 4]:
                        self.walls.set_right(current_x, current_y, 4)
                        can_pass = True
                    elif value == 3:
                        self.walls.set_right(current_x, current_y, 4)
                        can_end = True
                    else:
                        can_pass = True
                # Izquierda
                elif diff_x == -1 and diff_y == 0:
                    if value == 0:
                        can_pass = True
                    elif value == 0.5:
                        self.walls.set_left(current_x, current_y, 0)
                        can_end = True
                    elif value == 1:
                        self.walls.set_left(current_x, current_y, 0.5)
                        can_end = True
                    elif value in [2, 4]:
                        self.walls.set_left(current_x, current_y, 4)
                        can_pass = True
                    elif value == 3:
                        self.walls.set_left(current_x, current_y, 4)
                        can_end = True
                    else:
                        can_pass = True
                # Arriba
                elif diff_x == 0 and diff_y == -1:
                    if value == 0:
                        can_pass = True
                    elif value == 0.5:
                        self.walls.set_up(current_x, current_y, 0)
                        can_end = True
                    elif value == 1:
                        self.walls.set_up(current_x, current_y, 0.5)
                        can_end = True
                    elif value in [2, 4]:
                        self.walls.set_up(current_x, current_y, 4)
                        can_pass = True
                    elif value == 3:
                        self.walls.set_up(current_x, current_y, 4)
                        can_end = True
                    else:
                        can_pass = True
                # Abajo
                elif diff_x == 0 and diff_y == 1:
                    if value == 0:
                        can_pass = True
                    elif value == 0.5:
                        self.walls.set_down(current_x, current_y, 0)
                        can_end = True
                    elif value == 1:
                        self.walls.set_down(current_x, current_y, 0.5)
                        can_end = True
                    elif value in [2, 4]:
                        self.walls.set_down(current_x, current_y, 4)
                        can_pass = True
                    elif value == 3:
                        self.walls.set_down(current_x, current_y, 4)
                        can_end = True
                    else:
                        can_pass = True

                if can_end:
                    break

                # Actualiza la casilla si es niebla, vacío o fantasma
                if self.dashboard[new_y][new_x] == 0: # celda vacia
                    self.dashboard[new_y][new_x] = 2 # pone fantasma
                    break
                elif self.dashboard[new_y][new_x] == 1: # celda con niebla
                    self.dashboard[new_y][new_x] = 2 # pone fantasma
                    self.fog_list.remove((new_x, new_y)) # quita lista de niebla
                    break
                elif self.dashboard[new_y][new_x] == 2: # celda con fantasma
                    current_x, current_y = (new_x, new_y) # establece como actual
                    continue
                else:
                    self.dashboard[new_y][new_x] = 2
                    break

    # Colocación de niebla/fantasmas para pruebas
    def place_fog(self, x, y):
        """Coloca niebla o fantasma según el estado actual de la casilla."""
        if self.dashboard[y][x] == 0:
            self.dashboard[y][x] = 1  # Coloca niebla
            self.fog_list.append((x, y))

        elif self.dashboard[y][x] == 1:
            self.dashboard[y][x] = 2  # Convierte niebla en fantasma
            self.fog_list.remove((x, y))
            
        elif self.dashboard[y][x] == 2:
            self.arise(x, y)  # Realiza oleada de fantasmas
        
        for (fog_x, fog_y) in self.fog_list:
            self.spread_fire(fog_x, fog_y)