from gameboard import *
import numpy as np
from collections import deque


class FoggyGhost:
    """Gestiona la niebla y los fantasmas en el tablero.

    La clase utiliza una matriz para representar la posición de la niebla
    y los fantasmas, con los siguientes valores posibles:
        -1  -> fuera de límites
         0  -> vacío
         1  -> niebla
         2  -> fantasma

    Attributes:
        dashboard (list[list[int]]): Matriz que representa la niebla y los
                                     fantasmas en cada casilla del tablero.
    """

    dashboard = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 2, 2, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    # ----- Generación de coordenadas aleatorias -----
    @staticmethod
    def generate_coords():
        """Genera coordenadas aleatorias dentro de los límites del tablero.

        Returns:
            tuple[int, int]: Coordenadas (x, y) generadas aleatoriamente.
        """
        x = np.random.randint(1, 9)
        y = np.random.randint(1, 7)
        return (x, y)

    # ----- Getters -----
    @staticmethod
    def get_up(x, y):
        """Obtiene el valor arriba de (x, y).

        Args:
            x (int): Coordenada X.
            y (int): Coordenada Y.

        Returns:
            int: Valor de la casilla arriba.
        """
        if y <= 1 or y >= 7:
            return -1
        return FoggyGhost.dashboard[y - 1][x]

    @staticmethod
    def get_down(x, y):
        """Obtiene el valor abajo de (x, y).

        Args:
            x (int): Coordenada X.
            y (int): Coordenada Y.

        Returns:
            int: Valor de la casilla abajo.
        """
        if y <= 0 or y >= 6:
            return -1
        return FoggyGhost.dashboard[y + 1][x]

    @staticmethod
    def get_left(x, y):
        """Obtiene el valor a la izquierda de (x, y).

        Args:
            x (int): Coordenada X.
            y (int): Coordenada Y.

        Returns:
            int: Valor de la casilla izquierda.
        """
        if x <= 1 or x >= 9:
            return -1
        return FoggyGhost.dashboard[y][x - 1]

    @staticmethod
    def get_right(x, y):
        """Obtiene el valor a la derecha de (x, y).

        Args:
            x (int): Coordenada X.
            y (int): Coordenada Y.

        Returns:
            int: Valor de la casilla derecha.
        """
        if x <= 0 or x >= 8:
            return -1
        return FoggyGhost.dashboard[y][x + 1]

    # ----- Setters -----
    @staticmethod
    def set_up(x, y, value):
        """Asigna un valor a la casilla arriba de (x, y).

        Args:
            x (int): Coordenada X.
            y (int): Coordenada Y.
            value (int): Nuevo valor de la casilla.
        """
        if y <= 1 or y >= 7:
            return
        FoggyGhost.dashboard[y - 1][x] = value

    @staticmethod
    def set_down(x, y, value):
        """Asigna un valor a la casilla abajo de (x, y).

        Args:
            x (int): Coordenada X.
            y (int): Coordenada Y.
            value (int): Nuevo valor de la casilla.
        """
        if y <= 0 or y >= 6:
            return
        FoggyGhost.dashboard[y + 1][x] = value

    @staticmethod
    def set_left(x, y, value):
        """Asigna un valor a la casilla izquierda de (x, y).

        Args:
            x (int): Coordenada X.
            y (int): Coordenada Y.
            value (int): Nuevo valor de la casilla.
        """
        if x <= 1 or x >= 9:
            return
        FoggyGhost.dashboard[y][x - 1] = value

    @staticmethod
    def set_right(x, y, value):
        """Asigna un valor a la casilla derecha de (x, y).

        Args:
            x (int): Coordenada X.
            y (int): Coordenada Y.
            value (int): Nuevo valor de la casilla.
        """
        if x <= 0 or x >= 8:
            return
        FoggyGhost.dashboard[y][x + 1] = value

    # ----- Vecinos con niebla -----
    @staticmethod
    def get_foggy_neighbors(x, y):
        """Obtiene vecinos accesibles que contienen niebla.

        Args:
            x (int): Coordenada X.
            y (int): Coordenada Y.

        Returns:
            list[tuple[int, int]]: Lista de vecinos con niebla.
        """
        neighbors = GameBoard.get_neighbors(x, y)
        fog = 1
        foggy_neighbors = []

        for n in neighbors:
            current_x, current_y = n
            if FoggyGhost.dashboard[current_y][current_x] == fog:
                foggy_neighbors.append((current_x, current_y))

        return foggy_neighbors

    # ----- Propagación de fuego/fantasmas -----
    @staticmethod
    def spread_fire(x, y):
        """Propaga la niebla convirtiéndola en fantasmas a través de vecinos.

        Args:
            x (int): Coordenada X inicial.
            y (int): Coordenada Y inicial.
        """
        q = deque()
        visited = set()

        q.append((x, y))
        visited.add((x, y))

        while q:
            current_x, current_y = q.popleft()
            neighbors = FoggyGhost.get_foggy_neighbors(current_x, current_y)
            for new_x, new_y in neighbors:
                print(new_x, new_y)
                if (new_x, new_y) in visited:
                    continue

                visited.add((new_x, new_y))

                if FoggyGhost.dashboard[new_y][new_x] == 1:
                    FoggyGhost.dashboard[new_y][new_x] = 2
                    q.append((new_x, new_y))

    # ----- Verificación de límites del tablero -----
    @staticmethod
    def board_length(x, y):
        """Verifica si las coordenadas están dentro del tablero.

        Args:
            x (int): Coordenada X.
            y (int): Coordenada Y.

        Returns:
            bool: True si está dentro de límites, False en caso contrario.
        """
        return 1 <= x <= 8 and 1 <= y <= 6

    # ----- Explosión / oleada de fantasmas -----
    @staticmethod
    def surge(x, y):
        """Realiza una explosión/oleada de fantasmas desde la posición dada.

        Args:
            x (int): Coordenada X inicial.
            y (int): Coordenada Y inicial.
        """
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        for diff_x, diff_y in directions:
            current_x, current_y = (x, y)

            while True:
                new_x = current_x + diff_x
                new_y = current_y + diff_y

                out_of_bounds = not FoggyGhost.board_length(new_x, new_y)

                if diff_x == 1 and diff_y == 0:
                    value = GameBoard.get_right(current_x, current_y)

                elif diff_x == -1 and diff_y == 0:
                    value = GameBoard.get_left(current_x, current_y)

                elif diff_x == 0 and diff_y == -1:
                    value = GameBoard.get_up(current_x, current_y)

                elif diff_x == 0 and diff_y == 1:
                    value = GameBoard.get_down(current_x, current_y)
                    
                else:
                    break

                if value == -1:
                    break

                # Banderas
                can_pass = False
                can_end = False

                # Manejo de paredes y puertas según su dirección
                if diff_x == 1 and diff_y == 0:  # Derecha
                    if value == 0:
                        can_pass = True
                    elif value == 0.5: # Pared dañada
                        GameBoard.set_right(current_x, current_y, 0)
                        can_end = True
                    elif value == 1: # Pared completa
                        GameBoard.set_right(current_x, current_y, 0.5)
                        can_end = True
                    elif value in [2, 4]: # Puerta o pared destruida
                        GameBoard.set_right(current_x, current_y, 4)
                        can_pass = True
                    elif value == 3: # Puerta cerrada
                        GameBoard.set_right(current_x, current_y, 4)
                        can_end = True
                    else:
                        can_pass = True
                elif diff_x == -1 and diff_y == 0:  # Izquierda
                    if value == 0:
                        can_pass = True
                    elif value == 0.5: # Pared dañada
                        GameBoard.set_left(current_x, current_y, 0)
                        can_end = True
                    elif value == 1: # Pared completa
                        GameBoard.set_left(current_x, current_y, 0.5)
                        can_end = True
                    elif value in [2, 4]: # Puerta o pared destruida
                        GameBoard.set_left(current_x, current_y, 4)
                        can_pass = True
                    elif value == 3: # Puerta cerrada
                        GameBoard.set_left(current_x, current_y, 4)
                        can_end = True
                    else:
                        can_pass = True
                elif diff_x == 0 and diff_y == -1:  # Arriba
                    if value == 0:
                        can_pass = True
                    elif value == 0.5: # Pared dañada
                        GameBoard.set_up(current_x, current_y, 0)
                        can_end = True
                    elif value == 1: # Pared completa
                        GameBoard.set_up(current_x, current_y, 0.5)
                        can_end = True
                    elif value in [2, 4]: # Puerta o pared destruida
                        GameBoard.set_up(current_x, current_y, 4)
                        can_pass = True
                    elif value == 3: # Puerta cerrada
                        GameBoard.set_up(current_x, current_y, 4)
                        can_end = True
                    else:
                        can_pass = True
                elif diff_x == 0 and diff_y == 1:  # Abajo
                    if value == 0:
                        can_pass = True
                    elif value == 0.5: # Pared dañada
                        GameBoard.set_down(current_x, current_y, 0)
                        can_end = True
                    elif value == 1: # Pared completa
                        GameBoard.set_down(current_x, current_y, 0.5)
                        can_end = True
                    elif value in [2, 4]: # Puerta o pared destruida
                        GameBoard.set_down(current_x, current_y, 4)
                        can_pass = True
                    elif value == 3: # Puerta cerrada
                        GameBoard.set_down(current_x, current_y, 4)
                        can_end = True
                    else:
                        can_pass = True

                if can_end or out_of_bounds:
                    break

                value_ghost = FoggyGhost.dashboard[new_y][new_x]

                if value_ghost in [0, 1]:
                    FoggyGhost.dashboard[new_y][new_x] = 2
                    break
                elif value_ghost == 2: # Si ya es un fantasma
                    current_x, current_y = (new_x, new_y)
                    continue
                else:
                    FoggyGhost.dashboard[new_y][new_x] = 2
                    break

    # ----- Colocar niebla/fantasma para pruebas -----
    @staticmethod
    def place_fog(x, y):
        """Coloca niebla o fantasma según el estado de la casilla.

        Args:
            x (int): Coordenada X.
            y (int): Coordenada Y.
        """
        if FoggyGhost.dashboard[y][x] == 0:
            FoggyGhost.dashboard[y][x] = 1

        if FoggyGhost.dashboard[y][x] == 1:
            FoggyGhost.dashboard[y][x] = 2
            FoggyGhost.spread_fire(x, y)

        if FoggyGhost.dashboard[y][x] == 2:
            FoggyGhost.surge(x, y)
