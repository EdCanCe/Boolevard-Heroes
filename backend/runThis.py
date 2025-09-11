# --- walls.py ---
import numpy as np
from mesa.space import MultiGrid
from mesa import Model
from mesa.time import BaseScheduler
from collections import deque
from mesa import Agent
from abc import ABC, abstractmethod
from flask import Flask, jsonify
import copy
import heapq


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
            self.exits.append()

        if x <= 0:
            return  # Fuera de límites
        self.vertical[y][x - 1] = value

    def set_right(self, x, y, value):
        """Asigna un valor a la pared/puerta derecha de (x, y)."""
        if y in [8, 0] and value in [0, 2, 4] and (x, y) not in self.exits:
            self.exits.append()

        if x >= 9:
            return  # Fuera de límites
        self.vertical[y][x] = value

    def set_up(self, x, y, value):
        """Asigna un valor a la pared/puerta arriba de (x, y)."""
        if y in [1, 7] and value in [0, 2, 4] and (x, y) not in self.exits:
            self.exits.append()

        if y <= 0 or y >= 8:
            return  # Fuera de límites
        self.horizontal[y - 1][x] = value

    def set_down(self, x, y, value):
        """Asigna un valor a la pared/puerta abajo de (x, y)."""
        if y in [6, 0] and value in [0, 2, 4] and (x, y) not in self.exits:
            self.exits.append()

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

# --- ghosts.py ---
from imports import *

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
            [0, 0, 0, 0, 0, 0, 2, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.fog_list = [] # lista de casillas con niebla
        self.ghost_list = [(2, 2), (2, 3), (3, 2), (3, 3), (4, 3), (4, 4), (5, 3), (6, 5), (6, 6), (7, 5)]
        self.added_damage = 0

    def add_poi(self, poi : "POI"):
        # TODO: Comentar
        self.poi = poi

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
    def get_on(self, x, y):
        """Devuelve el valor de la casilla (x, y)."""
        return self.dashboard[y][x]

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

    # Setter de celda
    def set_on(self, x, y, value):
        """Asigna un valor a la casilla (x, y)."""

        current = self.dashboard[y][x]

        if current == 1 and value != 1 and (x, y) in self.fog_list:
            self.fog_list.remove((x, y))
        
        if current == 2 and value != 2 and (x, y) in self.ghost_list:
            self.fog_list.remove((x, y))

        if current != 1 and value == 1 and (x, y) not in self.fog_list:
            self.fog_list.append((x, y))

        if current != 2 and value == 2 and (x, y) not in self.ghost_list:
            self.ghost_list.append((x, y))

        self.dashboard[y][x] = value

    # Vecinos con fantasmas
    def get_ghosty_neighbors(self, x, y):
        """Obtiene las casillas vecinas que contienen fantasma y son adyacentes.

        Returns:
            list[tuple[int, int]]: Lista de coordenadas vecinas con fantasmas.
        """
        neighbors = self.walls.get_neighbors(x, y)  # Vecinos accesibles según Walls
        ghosty_neighbors = []

        for current_x, current_y in neighbors:
            if self.dashboard[current_y][current_x] == 2:  # hay fantasma
                ghosty_neighbors.append((current_x, current_y))

        return ghosty_neighbors
    
    # Vecinos con niebla
    def get_foggy_neighbors(self, x, y):
        """Obtiene las casillas vecinas que contienen niebla y son adyacentes.

        Returns:
            list[tuple[int, int]]: Lista de coordenadas vecinas con niebla.
        """
        neighbors = self.walls.get_neighbors(x, y)  # Vecinos accesibles según Walls
        foggy_neighbors = []

        for current_x, current_y in neighbors:
            if self.dashboard[current_y][current_x] == 1:  # hay niebla
                foggy_neighbors.append((current_x, current_y))

        return foggy_neighbors

    # Propagación de niebla/fantasmas
    def spread_ghost(self, x, y):
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
                    self.place_ghost(current_x, current_y) # pone fantasma
                    if (current_x, current_y) in self.fog_list:
                        self.fog_list.remove((current_x, current_y))
                    self.fog_changed = True
                    q.append((new_x, new_y))

    # Verificación de límites del tablero
    def board_length(self, x, y):
        """Verifica si las coordenadas (x, y) están dentro del tablero.

        Returns:
            bool: True si está dentro de límites, False si está fuera.
        """
        return 0 <= x <= 9 and 0 <= y <= 7

    # Explosión/oleada de fantasmas
    def arise(self, x, y):
        """Realiza una oleada de fantasmas desde la posición (x, y) propagándose 
        en todas las direcciones.
        """
        # Arriba, derecha, abajo, izquierda
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        ghost = {
            "x": x,
            "y": y,
            "status": 2,
            "order": self.order
        }

        self.json["ghosts"].append(ghost) # Añade la casilla donde ocurrió la explosión

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

                set_value = -1 # El valor al que se actualizará la pared/puerta
                side_value = -1 # La dirección a la que se actualizará la pared

                # Manejo de paredes y puertas según su estado
                # Pasa, daña, destruye o termina propagación según valor
                # Derecha
                if diff_x == 1 and diff_y == 0:
                    if value == 0:
                        can_pass = True
                    elif value == 0.5:
                        set_value = 0
                        can_end = True
                    elif value == 1:
                        set_value = 0.5
                        can_end = True
                    elif value == 2:
                        set_value = 4
                        can_pass = True
                    elif value == 3:
                        set_value = 4
                        can_end = True
                    else:
                        can_pass = True

                    if value > 0:
                        side_value = 1
                        self.walls.set_right(current_x, current_y, set_value)
                        
                # Izquierda
                elif diff_x == -1 and diff_y == 0:
                    if value == 0:
                        can_pass = True
                    elif value == 0.5:
                        set_value = 0
                        can_end = True
                    elif value == 1:
                        set_value = 0.5
                        can_end = True
                    elif value == 2:
                        set_value = 4
                        can_pass = True
                    elif value == 3:
                        set_value = 4
                        can_end = True
                    else:
                        can_pass = True

                    if value > 0:
                        side_value = 3
                        self.walls.set_left(current_x, current_y, set_value)

                # Arriba
                elif diff_x == 0 and diff_y == -1:
                    if value == 0:
                        can_pass = True
                    elif value == 0.5:
                        set_value = 0
                        can_end = True
                    elif value == 1:
                        set_value = 0.5
                        can_end = True
                    elif value == 2:
                        set_value = 4
                        can_pass = True
                    elif value == 3:
                        set_value = 4
                        can_end = True
                    else:
                        can_pass = True

                    if value > 0:
                        side_value = 0
                        self.walls.set_up(current_x, current_y, set_value)
                        
                # Abajo
                elif diff_x == 0 and diff_y == 1:
                    if value == 0:
                        can_pass = True
                    elif value == 0.5:
                        set_value = 0
                        can_end = True
                    elif value == 1:
                        set_value = 0.5
                        can_end = True
                    elif value == 2:
                        set_value = 4
                        can_pass = True
                    elif value == 3:
                        set_value = 4
                        can_end = True
                    else:
                        can_pass = True

                    if value > 0:
                        side_value = 2
                        self.walls.set_down(current_x, current_y, set_value)

                if value > 0 and set_value != -1:
                    wall = {
                        "direction": side_value, # direccion a la que apunta
                        "status": set_value, # a que valor se actualiza
                        "order": self.order,
                        "x": current_x,
                        "y": current_y
                    }

                    if value not in [2, 3, 4]:
                        self.added_damage += 1

                    self.json["walls"].append(wall)

                if can_end:
                    break

                # Actualiza la casilla si es niebla, vacío o fantasma
                if self.dashboard[new_y][new_x] == 0: # celda vacia
                    self.place_ghost(new_x, new_y) # pone fantasma
                    break
                elif self.dashboard[new_y][new_x] == 1: # celda con niebla
                    self.place_ghost(new_x, new_y) # pone fantasma
                    if (new_x, new_y) in self.fog_list:
                        self.fog_list.remove((new_x, new_y)) # quita lista de niebla
                    break
                elif self.dashboard[new_y][new_x] == 2: # celda con fantasma
                    current_x, current_y = (new_x, new_y) # establece como actual
                    continue
                else:
                    self.place_ghost(new_x, new_y) # pone fantasma
                    break

    # Colocación de niebla de cada turno
    def place_fog(self, json, order):
        """Coloca niebla o fantasma según el estado actual de la casilla.

        Args:
            json (Json): El json que contiene los datos que se pasarán en el endpoint.
            order (int): El número de orden de la acción.
        """

        self.json = json
        self.order = order
        self.added_damage = 0

        (x, y) = self.generate_coords()

        if self.dashboard[y][x] == 0:
            self.set_on(x, y, 1)  # Coloca niebla

        elif self.dashboard[y][x] == 1: # Hay niebla
            self.place_ghost(x, y) # colocar fantasma
            if (x, y) in self.fog_list:
                self.fog_list.remove((x, y))
            
        elif self.dashboard[y][x] == 2:
            self.arise(x, y)  # Realiza oleada de fantasmas
        
        self.fog_changed = True
        while self.fog_changed:
            self.fog_changed = False
            for (fog_x, fog_y) in self.fog_list:
                self.spread_ghost(fog_x, fog_y)

        return self.added_damage

    # Colocación de fantasma en una casilla
    def place_ghost(self, x, y):
        """Coloca un fantasma en una casilla."""

        self.set_on(x, y, 2)

        if self.poi.dashboard[y][x] >= 3: # hay un POI
            poi_value = self.poi.dashboard[y][x]
            
            if(poi_value == 3): # POI sin descubrir
                poi_value = self.poi.pick(x, y) # Obtiene el poi que se reveló
            
            if(poi_value == 4): # victima real
                self.poi.scared_victims += 1 # sumar 1 a victimas no salvadas

            self.poi.remove(x, y) # quitar POI del tablero y restar cantidad de actuales
            self.poi.removed_pois.append(((x, y), poi_value))

# --- poi.py ---
from imports import *

class POI:
    """Gestiona los puntos de interés (POI) en el tablero de juego.

    La clase maneja la ubicación de los POI y controla vectores de
    víctimas reales y falsas alarmas.

    Attributes:
        dashboard (list[list[int]]): Matriz que indica la ubicación de los POI.
            0 -> vacío
            3 -> POI
            4 -> Víctima real
            5 -> Falsa alarma
    """

    def __init__(self, ghosts : "Ghosts"):
        """Inicializa las variables de la clase y el tablero de POI."""

        self.ghosts = ghosts  # Referencia al objeto ghosts para generar coordenadas

        # Matriz del tablero con las ubicaciones POI iniciales
        self.dashboard = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 3, 0, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        # Vectores de víctimas reales y falsas alarmas
        self.real_victims = np.full(12, 4)  # 12 víctimas reales
        self.false_alarms = np.full(6, 5)   # 6 falsas alarmas
        self.poi_list = np.concatenate((self.real_victims, self.false_alarms))  # Se combinan ambos vectores

        self.current = 3
        self.rescued_victims = 0
        self.scared_victims = 0
        self.removed_pois = []
        self.added_pois = []

        self.current_poi_coords = [(4, 2), (1, 5), (8, 5)]

    def pick(self, x, y):
        """Selecciona un POI aleatoriamente y lo elimina del vector.

        Returns:
            int: Valor del POI seleccionado.
        """

        if len(self.poi_list) <= 0:
            return -1  # No hay POI disponibles

        # Mezcla el vector y selecciona el primer POI
        np.random.shuffle(self.poi_list)
        poi_value = self.poi_list[0]

        # Elimina el POI seleccionado del vector
        self.poi_list = np.delete(self.poi_list, 0)

        # TODO: Se añade algo que indique al json que se reveló

        self.dashboard[y][x] = poi_value # Se le pone a dicha posición el valor del poi

        return poi_value
    
    def get(self, x, y):
        """Regresa el valor de el valor en
        dichas coordenadas.
        """

        return self.dashboard[y][x]

    def place(self, heroes: MultiGrid):
        """Coloca un POI sin saber qué es en el tablero."""

        x, y = self.ghosts.generate_coords()  # Genera coordenadas aleatorias

        # Busca una casilla libre en el tablero
        while self.dashboard[y][x] != 0 and not heroes.is_cell_empty((x, y)):
            x, y = self.ghosts.generate_coords()

        self.dashboard[y][x] = 3  # Coloca el POI en la casilla libre

        oldValue = self.ghosts.dashboard[y][x]

        if self.ghosts.dashboard[y][x] in [1, 2]:
            # Si la casilla contiene ciertos valores de ghosts, los elimina
            self.ghosts.set_on(x, y, 0)

        self.current += 1 # Se aumenta la cantidad de POIs en el tablero
        self.added_pois.append(((x, y), oldValue))
        self.current_poi_coords.append((x, y))

    def remove(self, x, y):
        """Remueve del tablero un POI (no modifica los valores
        de falsos y víctimas)
        """
        
        self.current -= 1
        self.dashboard[y][x] = 0  # Remueve el POI
        self.current_poi_coords.remove((x, y))
        
    def willBeRescued(self, x, y):
        """Marca en el mapa un 0, ya que el POI lo
        llevaría el héroe
        """

        self.dashboard[y][x] = 0
        self.current_poi_coords.remove((x, y))

# --- map.py ---
from imports import *

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

        if self.poi.scared_victims >= 4 or self.damage_points >= 24:
            self.win = False
            return True
        
        if self.poi.rescued_victims >= 7:
            self.win = True
            return True
        
        return False

# --- hero.py ---
from imports import *

class Hero(Agent):
    """El héroe que hará acciones por el mapa para tratar
    de salvar a las 7 víctimas.
    """

    def __init__(self, model : "Map", id):
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
        self.id = id

        # Json utilizado para mandar datos
        self.json = {}

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

        self.json = { # Json que se va a mandar
            "num_steps": self.map.num_steps,
            "saved_victims": 0,
            "scared_victims": 0,
            "damaged_points": 0,
            "agents":[],
            "ghosts":[],
            "walls":[],
            "pois":[]
        }

        self.order = 0 # orden dentro del turno en que se realiza una accion

        action_type = 0 # dicta qué tipo de acción se hará

        self.next_steps = deque()
        self.movement_type = 0

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

            # Movimiento con estrategia
            else:
                if self.has_victim:
                    if not self.next_steps: # Si está vacía
                        self.next_steps = closest_exit(self.map, self.x, self.y)

                else: # Si no tiene víctima
                    if self.movement_type == 0:
                        self.next_steps = closest_poi(self.map, self.id)
                        self.movement_type = 1
                        if not self.next_steps: # En caso de que está vacía lo lleva al fuego mejor
                            self.next_steps = closest_ghost(self.map, self.x, self.y)
                            self.movement_type = 2
                    
                    if self.movement_type == 1: # Va a poi
                        if not self.next_steps: # Si está vacía
                            self.next_steps = closest_poi(self.map, self.id)

                    elif self.movement_type == 2: # Va a fantasmas
                        if not self.next_steps: # Si está vacía
                            self.next_steps = closest_ghost(self.map, self.x, self.y)
                            
                self.move_with_deque()
                
            # Independientemente de la simulación, verifica si reveló POI
            if self.map.poi.get(self.x, self.y) == 3:
                new_poi_value = self.map.poi.pick(self.x, self.y)

                poi = {
                    "x": self.x,
                    "y": self.y,
                    "old_status": 3,
                    "new_status": int(new_poi_value), # poi eliminado
                    "order": self.order
                }

                self.json["pois"].append(poi)

                if new_poi_value  == 4: # Si es una víctima real
                    if not self.has_victim: # En caso de que no lleve a nadie
                        self.hold_poi_on(self.x, self.y)

                else: # Si es una falsa alarma
                    self.map.poi.remove(self.x, self.y)

            elif self.map.poi.get(self.x, self.y) == 4 and not self.has_victim: # Que alguien más lo reveló pero no lo agarró
                self.hold_poi_on(self.x, self.y)

            self.order += 1
        
        self.old_matrix = copy.deepcopy(self.map.ghosts.dashboard)
        self.map.poi.added_pois = []
        self.map.poi.removed_pois = []

        # Después de los movimientos del héroe, finalizo el turno
        self.map.damage_points += self.map.ghosts.place_fog(self.json, self.order) # Coloca la niebla
        self.check_ghost_changes() # verifica cambios y agrega en json

        self.order += 1 # cambio de sub-turbo entre colocar fantasmas y pois

        for p in self.map.poi.removed_pois:
            poi = {
                "x": p[0][0],
                "y": p[0][1],
                "old_status": int(p[1]),
                "new_status": 0, # poi eliminado
                "order": self.order
            }

            self.json["pois"].append(poi)
        
        self.order += 1 # entre pois removidos y pois agregados

        while self.map.poi.current < 3: # Coloca POIs si es que hay menos de 3
            self.map.poi.place(self.map.heroes)

        for p in self.map.poi.added_pois:
            poi = {
                "x": p[0][0],
                "y": p[0][1],
                "old_status": 3, # poi agregado
                "new_status": 3, # poi agregado
                "order": self.order
            }

            if p[1] > 0: # Antes había algo y se eliminó
                ghost = {
                    "x": p[0][0],
                    "y": p[0][1],
                    "status": 0, # no hay nada
                    "order": self.order
                }

                self.json["ghosts"].append(ghost)
        
            self.json["pois"].append(poi)

        self.order += 1

        for hero in self.map.heroes_array:
            if hero.map.ghosts.get_on(hero.x, hero.y): # Si se extendieron los fantasmas a mi casilla
                if hero.has_victim: # Si estaba con una víctima, se asusta
                    hero.map.poi.scared_victims += 1
                    hero.has_victim = False

                hero.to_closest_spawn_point() # Lo lleva al spawnpoint
                hero.stored_action_points = 0 # Se eliminan puntos de acción guardados
                agent = {
                    "x": hero.x,
                    "y": hero.y,
                    "id": hero.id,
                    "carrying": False,
                    "energy": hero.action_points,
                    "action": "Regresa a spawnpoit",
                    "order": self.order
                }

                self.json["agents"].append(agent)

        self.json["saved_victims"] = self.map.poi.rescued_victims
        self.json["scared_victims"] = self.map.poi.scared_victims
        self.json["damaged_points"] = self.map.damage_points

        return self.json

    def to_closest_spawn_point(self):
        """Mueve el héroe al spawn point más cercano."""

        closest_spawn_point = (0, 0, 1000)

        # Busca la distancia más corta entre los spawnpoints
        for spawn_point in self.map.spawn_points:
            distance = abs(spawn_point[0] - self.x) + abs(spawn_point[1] - self.y) # Obtiene la distancia manhattan

            if distance < closest_spawn_point[2]: # Verifica que sea más cercano
                closest_spawn_point = (spawn_point[0], spawn_point[1], distance)

        self.update_position(closest_spawn_point[0], closest_spawn_point[1])
    
    def check_ghost_changes(self):
        """
        """
        for y in range(len(self.old_matrix)):
            for x in range(len(self.old_matrix[y])):
                if self.old_matrix[y][x] != self.map.ghosts.dashboard[y][x]:
                    ghost = {
                        "x": x,
                        "y": y,
                        "status": self.map.ghosts.dashboard[y][x],
                        "order": self.order
                    }

                    self.json["ghosts"].append(ghost)

    def hold_poi_on(self, x, y):
        self.has_victim = True
        self.map.poi.willBeRescued(x, y) # Quito en el mapa la víctima

        poi = {
            "x": x,
            "y": y,
            "old_status": 4,
            "new_status": 0, # poi eliminado, se va a poner en el héroe
            "order": self.order
        }

        self.json["pois"].append(poi)

    def get_direction(self, new_x, new_y):
        if new_y < self.y: return 0
        if new_x > self.x: return 1
        if new_y > self.y: return 2
        if new_x < self.x: return 3
        return 4

    def move_with_deque(self):
        """Mueve un agente basándose en una deque y el ambiente actual."""

        # Front = Left = 0 ; Back = nada = -1
        (next_x, next_y) = self.next_steps[0]

        direction = self.get_direction(next_x, next_y) # La dirección de movimiento

        # Verifica si su destino tiene niebla y lo elimina
        if self.map.ghosts.get_on(next_x, next_y) == 1:
            action = ClearFog(1, self, direction)
            if action.is_possible():
                action.do_action()
                return
            
        # Verifica si su destino tiene fantasma y lo elimina
        if self.map.ghosts.get_on(next_x, next_y) == 2:
            action = RemoveGhost(2, self, direction)
            if action.is_possible():
                action.do_action()
                return

        # Despeja fantasma de sus vecinos dependiendo de su tipo de movimiento
        if self.movement_type == 2: # Está tratando de eliminar un fantasma
            neighbors = self.map.ghosts.get_ghosty_neighbors(self.x, self.y)
            for neighbor in neighbors:
                action = RemoveGhost(2, self, direction)
                if action.is_possible():
                    action.do_action()
                    return
        
        # Despeja niebla de sus vecinos
        neighbors = self.map.ghosts.get_foggy_neighbors(self.x, self.y)
        for neighbor in neighbors:
            action = ClearFog(1, self, direction)
            if action.is_possible():
                action.do_action()
                return
            
        # Verifica si se tiene que acabar el movimiento antes de llegar al fantasma
        if self.movement_type == 2 and len(self.next_steps) == 1: # Es un fantasma y ya va a llegar
            self.next_steps.popleft()
            self.movement_type = 0
            return
            
        # Verifica si para llegar a su destino tiene que abrir una puerta
        if direction == 0 and self.map.walls.get_up(self.x, self.y) == 3:
            action = OpenDoor(1, self, direction)
            if action.is_possible():
                action.do_action()
                return
        if direction == 1 and self.map.walls.get_right(self.x, self.y) == 3:
            action = OpenDoor(1, self, direction)
            if action.is_possible():
                action.do_action()
                return
        if direction == 2 and self.map.walls.get_down(self.x, self.y) == 3:
            action = OpenDoor(1, self, direction)
            if action.is_possible():
                action.do_action()
                return
        if direction == 3 and self.map.walls.get_left(self.x, self.y) == 3:
            action = OpenDoor(1, self, direction)
            if action.is_possible():
                action.do_action()
                return

        # Al quitar fantasmas, nieblas y liberar su camino, avanza
        action = Action(0, self, 0)
        if self.has_victim:
            action = MoveWithVictim(2, self, direction)
        else:
            action = Move(1, self, direction)
        if action.is_possible():
            self.next_steps.popleft()

            # Si ya no tiene más pasos (llegó), libera el movement
            if not self.next_steps:
                self.movement_type = 0

            action.do_action
            return
        
        # Si no pudo hacer ninguna de las anteriores, espera
        action = DoNothing(0, self, direction)
        action.do_action()



class MapNode:
    """Un nodo dentro del mapa que te dicta qué nodo se ocupa
    para llegar a éste.
    """
    def __init__(self, x, y, current_cost, parent: "MapNode"):
        self.x = x
        self.y = y
        self.current_cost = current_cost
        self.parent = parent

class PriorityQueue:
    """Priority queue para ordenar las próximas casillas a visitar.
    """
    def __init__(self):
        self.__data = []

    # Verifica si está vacía
    def empty(self):
        return not self.__data
    
    # Inserta un nuevo elemento
    def push(self, priority, value):
        heapq.heappush(self.__data, (priority, value))

    # Elimina el elemento más próximo
    def pop(self):
        if self.__data: # No está vacío
            heapq.heappop(self.__data)
        else:
            raise Exception("No such element")
        
    # Obtiene el próximo elemento
    def top(self):
        if self.__data: # No está vacío
            return self.__data[0]
        else:
            raise Exception("No such element")
        
def neigbors_with_cost(map: "Map", x, y, movement_type):
    """Obtiene los vecinos de una casilla, con el costo
    para poder llegar a éstas.
    """

    neighbors = []

    multiplier = 3
    if movement_type == 2: # En caso de que su intención sea quitar fantasmas
        multiplier = 0.7

    # Las celdas adyacentes
    adyacent = map.walls.get_neighbors(x, y)
    doors = map.walls.get_closed_neighbors(x, y)

    for neighbor in adyacent:
        current = map.ghosts.get_on(neighbor[0], neighbor[1])
        if current == 0:
            neighbors.append((neighbor[0], neighbor[1], 1))
        else:
            neighbors.append((neighbor[0], neighbor[1], current * multiplier)) # Le aumenta su "costo" si quiere ir a un poi, para evitar fuegos

    for neighbor in doors:
        current = map.ghosts.get_on(neighbor[0], neighbor[1])
        if current == 0:
            neighbors.append((neighbor[0], neighbor[1], 2))
        else:
            neighbors.append((neighbor[0], neighbor[1], current * multiplier + 1)) # Le aumenta su "costo" si quiere ir a un poi, para evitar fuegos

    return neighbors

def start_matrix(map: "Map"):
    """Inicializa la matriz de los nodos:

    Args:
        map (Map): El mapa del tablero

    Returns:
        list[list[MapNode]]: Los nodos del mapa
    """

    height = len(map.ghosts.dashboard)
    width = len(map.ghosts.dashboard[0])

    # Línea de código creada con ChatGPT, no estoy acostumbrado a trabajar con matrices en Python
    return [[MapNode(x, y, 1000, None) for x in range(width)] for y in range(height)]

def generate_deque(matrix: list[list[MapNode]], start_x, start_y, end_x, end_y, starts_from_hero):
    """Genera la deque que dicta que casillas pasar para llegar de un nodo a otro
    """

    next_steps = deque()
    current_x = end_x
    current_y = end_y

    # Sigue los pasos marcados por los padres de los nodos
    while (current_x, current_y) != (start_x, start_y):
        # Dependiendo del tipo en que se tiene que añadir, hace un append u otro
        if starts_from_hero:
            next_steps.appendleft((current_x, current_y))
        else:
            next_steps.append((current_x, current_y))

        temp_x = current_x
        current_x = matrix[current_y][current_x].parent.x
        current_y = matrix[current_y][temp_x].parent.y

    return next_steps

def dijkstra(map: "Map", start_x, start_y, movement_type):
    """Genera una matriz de las posiciones necesarias
    para ir de un punto a otros.

    Args:
        map (Map): El mapa del tablero
        start_x (_type_): Posición en X inicial
        start_y (_type_): Posición en Y inicial
    """

    # Inicializa el mapa, la queue y su primera posición
    matrix = start_matrix(map)
    matrix[start_y][start_x] = MapNode(start_x, start_y, 0, None)
    left_to_visit = PriorityQueue()
    left_to_visit.push(0, (start_x, start_y))

    # Corre hasta ya no poder más
    while not left_to_visit.empty():
        (current_cost, (current_x, current_y)) = left_to_visit.top()
        left_to_visit.pop()

        neighbors = neigbors_with_cost(map, current_x, current_y, movement_type)
        for neighbor in neighbors:
            (x, y, cost) = neighbor

            if current_cost + cost < matrix[y][x].current_cost: # Se encuentra una nueva opción para llegar a esa casilla
                matrix[y][x].current_cost = current_cost + cost
                matrix[y][x].parent = matrix[current_y][current_x]
                left_to_visit.push(matrix[y][x].current_cost, (x, y))

    return matrix

def dijkstra_to(map: "Map", start_x, start_y, end_x, end_y, movement_type):
    """Utilizando el algoritmo de dijkstra, regresa una deque
    de las casillas necesarias para llegar de una casilla a otra.
    """

    matrix = dijkstra(map, start_x, start_y, movement_type)
    return generate_deque(matrix, start_x, start_y, end_x, end_y, True)

def closest_poi(map: "Map", hero_id):
    """Obtiene el camino para llegar al POI más cercano en caso
    de tener uno, en caso contrario, regresa una deque vacía.

    Args:
        map (Map): El mapa del tablero
        hero_id (int): El ID del héroe a verificar
    """

    closest_to_pois = PriorityQueue()

    # Para cada POI
    i = 0
    for poi in map.poi.current_poi_coords:
        poi_matrix = dijkstra(map, poi[0], poi[1], 1)
        heroes_distance = PriorityQueue()

        # Obtiene la distancia de cada heroe del poi actual
        for hero in map.heroes_array:
            heroes_distance.push(poi_matrix[hero.y][hero.x].current_cost, hero.id)

        closest_distance = heroes_distance.top()[0] # Obtiene la distancia que el héroe más cercano tiene al poi

        closest_heroes = []

        while not heroes_distance.empty() and heroes_distance.top()[0] == closest_distance:
            closest_heroes.append(heroes_distance.top()[1])
            heroes_distance.pop()

        # Añade los índices de los héroes más cercanos hacia un poi
        if hero_id in closest_heroes:
            closest_to_pois.push(len(closest_heroes), (i, poi_matrix))

        i += 1

    next_steps = deque()

    # Si no está vacía, significa que es el más cercano a alguno
    if not closest_to_pois.empty():
        (heroes_len, (poi_id, poi_matrix)) = closest_to_pois.top()
        hero_id -= 1

        next_steps = generate_deque(poi_matrix, map.poi.current_poi_coords[poi_id][0], map.poi.current_poi_coords[poi_id][1], map.heroes_array[hero_id].x, map.heroes_array[hero_id].y, False)

        next_steps.popleft()
        next_steps.append(map.poi.current_poi_coords[poi_id])
        
    return next_steps

def closest_ghost(map: "Map", x, y):
    """Obtiene el camino para llegar al POI más cercano en caso
    de tener uno, en caso contrario, regresa una deque vacía.

    Args:
        map (Map): El mapa del tablero
        x (int): La coordenada X del héroe
        y (int): La coordenada Y del héroe
    """
     
    matrix = dijkstra(map, x, y, 2)

    closest_ghost = (5, 4, 1000)

    for ghost in map.ghosts.ghost_list:
        value = matrix[ghost[1]][ghost[0]].current_cost - len(map.ghosts.get_ghosty_neighbors(ghost[0], ghost[1]))

        if value < closest_ghost[2]:
            closest_ghost = (ghost[0], ghost[1], value)

    return generate_deque(matrix, x, y, closest_ghost[0], closest_ghost[1], True)

def closest_exit(map: "Map", x, y):
    """Obtiene el camino para llegar a la salida más cercana.

    Args:
        map (Map): El mapa del tablero
        x (int): La coordenada X del héroe
        y (int): La coordenada Y del héroe
    """
     
    matrix = dijkstra(map, x, y, 1)

    closest = (0, 0, 1000)

    for exit in map.walls.exits:
        value = matrix[exit[1]][exit[0]].current_cost

        if value < closest[2]:
            closest = (exit[0], exit[1], value)

    return generate_deque(matrix, x, y, closest[0], closest[1], True)

# --- actions.py ---
from imports import *

# ChatGPT me mostró que al usar typing, no se añade al runtime y solo ayuda en el editor
class ActionList:
    """Genera la lista de acciones posibles
    que puede realizar un héroe en un momento
    dado.
    """
    @staticmethod
    def generate_list(hero: "Hero"):
        """Genera la lista de acciones que se pueden
        realizar en el turno actual.

        Args:
            hero (Hero): El héroe a verificar.

        Returns:
            list[Action]: La lista de acciones posibles a hacer.
        """

        free_path = [0, 2, 4] # El valor que puede tener una casilla para poder ir

        (x, y) = hero.pos

        possible_actions = [] # Aquí se guardarán las posibles acciontes

        # En caso de que tenga una víctima
        if hero.has_victim:
            if hero.map.walls.get_up(x, y) in free_path:
                possible_actions.append(MoveWithVictim(2, hero, 0))
            if hero.map.walls.get_right(x, y) in free_path:
                possible_actions.append(MoveWithVictim(2, hero, 1))
            if hero.map.walls.get_down(x, y) in free_path:
                possible_actions.append(MoveWithVictim(2, hero, 2))
            if hero.map.walls.get_left(x, y) in free_path:
                possible_actions.append(MoveWithVictim(2, hero, 3))

        # Si no tiene víctima, puede pasar por el fuego o caminar normal
        else:
            if hero.map.walls.get_up(x, y) in free_path:
                if hero.map.ghosts.get_up(x, y) != 2:
                    possible_actions.append(Move(1, hero, 0))
            if hero.map.walls.get_right(x, y) in free_path:
                if hero.map.ghosts.get_right(x, y) != 2:
                    possible_actions.append(Move(1, hero, 1))
            if hero.map.walls.get_down(x, y) in free_path:
                if hero.map.ghosts.get_down(x, y) != 2:
                    possible_actions.append(Move(1, hero, 2))
            if hero.map.walls.get_left(x, y) in free_path:
                if hero.map.ghosts.get_left(x, y) != 2:
                    possible_actions.append(Move(1, hero, 3))

        # Se añaden las posibilidades de abrir puertas
        if hero.map.walls.get_up(x, y) == 3:
            possible_actions.append(OpenDoor(1, hero, 0))
        if hero.map.walls.get_right(x, y) == 3:
            possible_actions.append(OpenDoor(1, hero, 1))
        if hero.map.walls.get_down(x, y) == 3:
            possible_actions.append(OpenDoor(1, hero, 2))
        if hero.map.walls.get_left(x, y) == 3:
            possible_actions.append(OpenDoor(1, hero, 3))

        # Se añaden las posibilidades de cerrar puertas
        if hero.map.walls.get_up(x, y) == 2:
            possible_actions.append(CloseDoor(1, hero, 0))
        if hero.map.walls.get_right(x, y) == 2:
            possible_actions.append(CloseDoor(1, hero, 1))
        if hero.map.walls.get_down(x, y) == 2:
            possible_actions.append(CloseDoor(1, hero, 2))
        if hero.map.walls.get_left(x, y) == 2:
            possible_actions.append(CloseDoor(1, hero, 3))

        # Se añaden las posibilidades de dañar paredes
        if hero.map.walls.get_up(x, y) == 1:
            possible_actions.append(DamageWall(2, hero, 0))
        if hero.map.walls.get_right(x, y) == 1:
            possible_actions.append(DamageWall(2, hero, 1))
        if hero.map.walls.get_down(x, y) == 1:
            possible_actions.append(DamageWall(2, hero, 2))
        if hero.map.walls.get_left(x, y) == 1:
            possible_actions.append(DamageWall(2, hero, 3))

        # Se añaden las posibilidades de destruir paredes
        if hero.map.walls.get_up(x, y) == 0.5:
            possible_actions.append(DestroyWall(2, hero, 0))
        if hero.map.walls.get_right(x, y) == 0.5:
            possible_actions.append(DestroyWall(2, hero, 1))
        if hero.map.walls.get_down(x, y) == 0.5:
            possible_actions.append(DestroyWall(2, hero, 2))
        if hero.map.walls.get_left(x, y) == 0.5:
            possible_actions.append(DestroyWall(2, hero, 3))

        # Se añaden las posibilidades de disipar niebla y fantasmas
        if hero.map.ghosts.get_up(x, y) == 1:
            possible_actions.append(ClearFog(1, hero, 0))
        elif hero.map.ghosts.get_up(x, y) == 2:
            possible_actions.append(ScareGhost(1, hero, 0))
            possible_actions.append(RemoveGhost(2, hero, 0))
        if hero.map.ghosts.get_right(x, y) == 1:
            possible_actions.append(ClearFog(1, hero, 1))
        elif hero.map.ghosts.get_right(x, y) == 2:
            possible_actions.append(ScareGhost(1, hero, 1))
            possible_actions.append(RemoveGhost(2, hero, 1))
        if hero.map.ghosts.get_down(x, y) == 1:
            possible_actions.append(ClearFog(1, hero, 2))
        elif hero.map.ghosts.get_down(x, y) == 2:
            possible_actions.append(ScareGhost(1, hero, 2))
            possible_actions.append(RemoveGhost(2, hero, 2))
        if hero.map.ghosts.get_left(x, y) == 1:
            possible_actions.append(ClearFog(1, hero, 3))
        elif hero.map.ghosts.get_left(x, y) == 2:
            possible_actions.append(ScareGhost(1, hero, 3))
            possible_actions.append(RemoveGhost(2, hero, 3))
        if hero.map.ghosts.get_on(x, y) == 1:
            possible_actions.append(ClearFog(1, hero, 4))
        elif hero.map.ghosts.get_on(x, y) == 2:
            possible_actions.append(ScareGhost(1, hero, 4))
            possible_actions.append(RemoveGhost(2, hero, 4))

        # Verifica si actualmente está en fuego
        if hero.map.ghosts.get_on(x, y) != 2:
            possible_actions.append(DoNothing(0, hero, 4))

        filtered_actions = [] # Se guardan las acciones verdaderamente posibles

        # Se filtran las acciones a únicamente las que se puedan usar
        for action in possible_actions:
            if action.is_possible():
                filtered_actions.append(action)

        return filtered_actions

class Action(ABC):
    """Clase abstracta de acción posible a realizar.
    """
    def __init__(self, action_points, hero: "Hero", direction):
        """Constructor de la clase de acción

        Args:
            action_points (int): Los puntos de acción que cuesta la acción.
            hero (Hero): El héroe que realizará la acción.
            direction (int): La dirección en que se hará la acción. 
        """

        # Atributos generales para las acciones
        self.action_points = action_points
        self.hero = hero
        self.direction = direction
        self.objective = 0 # Cuánto aporta al objetivo

        # Las posibles direcciones
        self.UP = 0
        self.RIGHT = 1
        self.DOWN = 2
        self.LEFT = 3
        self.SAME = 4

    def update_coords(self):
        (self.current_x, self.current_y) = self.hero.pos
        (self.action_x, self.action_y) = self.hero.pos

        # Actualiza las coordenadas de la acción dependiendo de la dirección
        if self.direction == self.UP:
            self.action_y -= 1
        elif self.direction == self.RIGHT:
            self.action_x += 1
        elif self.direction == self.DOWN:
            self.action_y += 1
        elif self.direction == self.LEFT:
            self.action_x -= 1

    def restore_action_points(self):
        """Se restauran los puntos de acción del héroe."""

        self.hero.action_points += self.action_points

    @abstractmethod
    def is_possible(self):
        """Verifica que la acción sea válida"""
    
        (self.current_x, self.current_y) = self.hero.pos
        (self.action_x, self.action_y) = self.hero.pos

        self.update_coords()

        if self.action_x in [-1, 10] or self.action_y in [-1, 8]:
            return False
    
        return self.action_points <= self.hero.action_points

    @abstractmethod
    def do_action(self):
        """Método abstracto para realizar la acción."""

        self.hero.action_points -= self.action_points

        # TODO: Verifica si alguna de las coordenadas sale del mapa

        pass

class Move(Action):
    """Mueve el héroe a otra casilla siempre y cuando
    no esté cargando con una víctima y la casilla no
    tenga fantasmas.
    """

    def is_possible(self):
        return super().is_possible()

    def do_action(self):
        """Mueve el héroe a otra casilla"""

        super().do_action()

        self.hero.update_position(self.action_x, self.action_y)
        
        agent = {
            "x": self.action_x,
            "y": self.action_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe en movimiento",
            "order": self.hero.order
        }

        self.hero.json["agents"].append(agent)

        return True

class MoveWithVictim(Action):
    """Mueve el héroe a otra casilla mientras carga una
    víctima.
    """

    def is_possible(self):
        # Verifica que la casilla no tenga fantasmas
        self.update_coords()

        if self.action_x in [-1, 10] or self.action_y in [-1, 8]:
            return False
        
        if self.hero.map.ghosts.get_on(self.action_x, self.action_y) == 2:
            return False

        # Verifica por puntos de acción
        return self.action_points <= self.hero.action_points
    
    

    def do_action(self):
        """Mueve el héroe y la víctima a otra casilla"""

        super().do_action()

        self.hero.update_position(self.action_x, self.action_y)

        # Verifica si acaba de salvar a la persona
        if self.action_x in [0, 10] or self.action_y in [0, 8]:
            self.hero.map.poi.rescued_victims += 1
            self.hero.has_victim = False # Ya que ya salvó la víctima

        agent = {
            "x": self.action_x,
            "y": self.action_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe en movimiento con victima",
            "order": self.hero.order
        }

        # TODO: En unity modificar el sprite del agente segun su estado de carrying
        # TODO: En caso de que si, mostrar un mensaje de cambio

        self.hero.json["agents"].append(agent)

        return True

class OpenDoor(Action):
    """Abre una puerta alrededor del héroe."""

    def is_possible(self):
        return super().is_possible()

    def do_action(self):
        """Abre la puerta."""

        super().do_action()

        if self.direction == self.UP:
            self.hero.map.walls.set_up(self.current_x, self.current_y, 2)
        elif self.direction == self.RIGHT:
            self.hero.map.walls.set_right(self.current_x, self.current_y, 2)
        elif self.direction == self.DOWN:
            self.hero.map.walls.set_down(self.current_x, self.current_y, 2)
        elif self.direction == self.LEFT:
            self.hero.map.walls.set_left(self.current_x, self.current_y, 2)

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe abre una puerta",
            "order": self.hero.order
        }

        wall = {
            "direction": self.direction, # direccion a la que apunta
            "status": 2, # puerta abierta
            "order": self.hero.order,
            "x": self.current_x,
            "y": self.current_y
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["walls"].append(wall)

        return True

class CloseDoor(Action):
    """Cierra una puerta alrededor del héroe."""

    def is_possible(self):
        return super().is_possible()

    def do_action(self):
        """Cierra la puerta."""

        super().do_action()

        if self.direction == self.UP:
            self.hero.map.walls.set_up(self.current_x, self.current_y, 3)
        elif self.direction == self.RIGHT:
            self.hero.map.walls.set_right(self.current_x, self.current_y, 3)
        elif self.direction == self.DOWN:
            self.hero.map.walls.set_down(self.current_x, self.current_y, 3)
        elif self.direction == self.LEFT:
            self.hero.map.walls.set_left(self.current_x, self.current_y, 3)

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe cierra una puerta",
            "order": self.hero.order
        }

        wall = {
            "direction": self.direction, # direccion a la que apunta
            "status": 3, # puerta cerrado
            "order": self.hero.order,
            "x": self.current_x,
            "y": self.current_y
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["walls"].append(wall)

        return True

class DamageWall(Action):
    """Daña una pared alrededor del héroe."""

    def is_possible(self):
        return super().is_possible()

    def do_action(self):
        """Daña la pared."""

        super().do_action()

        if self.direction == self.UP:
            self.hero.map.walls.set_up(self.current_x, self.current_y, 0.5)
        elif self.direction == self.RIGHT:
            self.hero.map.walls.set_right(self.current_x, self.current_y, 0.5)
        elif self.direction == self.DOWN:
            self.hero.map.walls.set_down(self.current_x, self.current_y, 0.5)
        elif self.direction == self.LEFT:
            self.hero.map.walls.set_left(self.current_x, self.current_y, 0.5)

        self.hero.map.damage_points += 1

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe dañó una pared",
            "order": self.hero.order
        }

        wall = {
            "direction": self.direction, # direccion a la que apunta
            "status": 0.5, # pared dañada
            "order": self.hero.order,
            "x": self.current_x,
            "y": self.current_y
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["walls"].append(wall)

        return True

class DestroyWall(Action):
    """Destruye una pared alrededor del héroe."""

    def is_possible(self):
        return super().is_possible()

    def do_action(self):
        """Destruye la pared."""

        super().do_action()

        if self.direction == self.UP:
            self.hero.map.walls.set_up(self.current_x, self.current_y, 0)
        elif self.direction == self.RIGHT:
            self.hero.map.walls.set_right(self.current_x, self.current_y, 0)
        elif self.direction == self.DOWN:
            self.hero.map.walls.set_down(self.current_x, self.current_y, 0)
        elif self.direction == self.LEFT:
            self.hero.map.walls.set_left(self.current_x, self.current_y, 0)

        self.hero.map.damage_points += 1

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe ha tumbado una pared",
            "order": self.hero.order
        }

        wall = {
            "direction": self.direction, # direccion a la que apunta
            "status": 0, # pared destruida
            "order": self.hero.order,
            "x": self.current_x,
            "y": self.current_y
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["walls"].append(wall)

        return True

class ClearFog(Action):
    """Dispersa una niebla alrededor del héroe."""

    def is_possible(self):
        (self.current_x, self.current_y) = self.hero.pos
        (self.action_x, self.action_y) = self.hero.pos

        self.update_coords()

        if not (self.action_x, self.action_y) in self.hero.map.walls.get_neighbors(self.current_x, self.current_y) and (self.action_x, self.action_y) != (self.current_x, self.current_y):
            return False

        return super().is_possible()

    def do_action(self):
        """Dispersa la niebla alrededor del héroe."""

        super().do_action()

        self.hero.map.ghosts.set_on(self.action_x, self.action_y, 0)

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe dispersa una niebla",
            "order": self.hero.order
        }

        ghost = {
            "x": self.action_x,
            "y": self.action_y,
            "status": 0, # sin niebla
            "order": self.hero.order
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["ghosts"].append(ghost)

        return True

class ScareGhost(Action):
    """Ahuyenta un fantasma alrededor del héroe."""

    def is_possible(self):
        (self.current_x, self.current_y) = self.hero.pos
        (self.action_x, self.action_y) = self.hero.pos

        self.update_coords()

        if not (self.action_x, self.action_y) in self.hero.map.walls.get_neighbors(self.current_x, self.current_y) and (self.action_x, self.action_y) != (self.current_x, self.current_y):
            return False

        return super().is_possible()
    
    def do_action(self):
        """Ahuyenta el fantasma."""

        super().do_action()

        self.hero.map.ghosts.set_on(self.action_x, self.action_y, 1)

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe ahuyenta un fantasma a niebla",
            "order": self.hero.order
        }

        ghost = {
            "x": self.action_x,
            "y": self.action_y,
            "status": 1, # establecer niebla
            "order": self.hero.order
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["ghosts"].append(ghost)

        return True

class RemoveGhost(Action):
    """Remueve un fantasma alrededor del héroe."""

    def is_possible(self):
        (self.current_x, self.current_y) = self.hero.pos
        (self.action_x, self.action_y) = self.hero.pos

        self.update_coords()

        if not (self.action_x, self.action_y) in self.hero.map.walls.get_neighbors(self.current_x, self.current_y) and (self.action_x, self.action_y) != (self.current_x, self.current_y):
            return False

        return super().is_possible()

    def do_action(self):
        """Remueve el fantasma."""

        super().do_action()

        self.hero.map.ghosts.set_on(self.action_x, self.action_y, 0)

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe ahuyenta un fantasma por completo",
            "order": self.hero.order
        }

        ghost = {
            "x": self.action_x,
            "y": self.action_y,
            "status": 0, # sin niebla
            "order": self.hero.order
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["ghosts"].append(ghost)

        return True

class DoNothing(Action):
    """Guarda los puntos de acción restantes del héroe
    con intención de iniciar el siguiente turno.
    """

    def is_possible(self):
        return super().is_possible()

    def do_action(self):
        """Guarda los puntos de acción."""

        super().do_action()

        self.hero.stored_action_points = min(self.hero.action_points, 4)
        self.hero.action_points = 0

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe espera en su casilla",
            "order": self.hero.order
        }

        self.hero.json["agents"].append(agent)

        return True

# --- endpoint.py ---
from imports import *

app = Flask(__name__)

turns = []

@app.route("/start/<mode>")
def start(mode):
    global simulation
    if mode == "naive":
        simulation = Map(True)
    else:
        simulation = Map(False)
    return "Simulation created"

@app.route("/turn")
def turn():
    if not isinstance(simulation, Map):
        return "Simulation not started", 400
    current = jsonify(simulation.turn())
    turns.append(current)
    return current

@app.route("/turn/<id>")
def selected_turn(id):
    if not isinstance(simulation, Map):
        return "Simulation not started", 400
    return turns[int(id)]

if __name__ == "__main__":
    app.run(debug=True)

