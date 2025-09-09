from imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from walls import *
    from poi import *
    from map import *
    from hero import *
    from actions import *

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
        self.added_damage = 0

    def add_poi(self, poi : "POI"):

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

    # Setters de celdas adyacentes
    def set_on(self, x, y, value):
        """Asigna un valor a la casilla (x, y)."""
        self.dashboard[y][x] = value

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

    # Vecinos con fantasmas
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
            self.dashboard[y][x] = 1  # Coloca niebla
            self.fog_list.append((x, y))

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

        self.dashboard[y][x] = 2

        if self.poi.dashboard[y][x] >= 3: # hay un POI
            poi_value = self.poi.dashboard[y][x]
            
            if(poi_value == 3): # POI sin descubrir
                poi_value = self.poi.pick(x, y) # Obtiene el poi que se reveló
            
            if(poi_value == 4): # victima real
                self.poi.scared_victims += 1 # sumar 1 a victimas no salvadas

            self.poi.remove(x, y) # quitar POI del tablero y restar cantidad de actuales
            self.poi.removed_pois.append(((x, y), poi_value))