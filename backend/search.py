from imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from walls import *
    from poi import *
    from ghosts import *
    from map import *
    from actions import *

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

    multiplier = 1
    if movement_type == 2: # En caso de que su intención sea quitar fantasmas
        multiplier = 0.9

    # Las celdas adyacentes
    adyacent = map.walls.get_neighbors(x, y)
    doors = map.walls.get_closed_neighbors(x, y)

    for neighbor in adyacent:
        current = map.ghosts.get_on(neighbor[0], neighbor[1])
        if current == 0:
            neighbors.append((neighbor[0], neighbor[1], 1))
        else:
            if current == 2: multiplier /= 3
            neighbors.append((neighbor[0], neighbor[1], current * multiplier)) # Le aumenta su "costo" si quiere ir a un poi, para evitar fuegos

    for neighbor in doors:
        current = map.ghosts.get_on(neighbor[0], neighbor[1])
        if current == 0:
            neighbors.append((neighbor[0], neighbor[1], 2))
        else:
            if current == 2: multiplier /= 3
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

        if matrix[current_y][current_x].parent == None:
            break

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
        poi_matrix = dijkstra(map, poi[0], poi[1], 2)
        heroes_distance = PriorityQueue()

        # Obtiene la distancia de cada heroe del poi actual
        for hero in map.heroes_array:
            if hero.has_victim == False:
                heroes_distance.push(poi_matrix[hero.y][hero.x].current_cost, hero.id)

        # TODO: El fantasma no mata al poi -> unity

        closest_distance = heroes_distance.top()[0] # Obtiene la distancia que el héroe más cercano tiene al poi

        closest_heroes = []

        while not heroes_distance.empty() and heroes_distance.top()[0] == closest_distance:
            closest_heroes.append(heroes_distance.top()[1])
            heroes_distance.pop()

        # Añade los índices de los héroes más cercanos hacia un poi
        if hero_id in closest_heroes:
            closest_to_pois.push(poi_matrix[poi[1]][poi[0]].current_cost, (i, poi_matrix))

        i += 1

    next_steps = deque()

    # Si no está vacía, significa que es el más cercano a alguno
    if not closest_to_pois.empty():
        (heroes_len, (poi_id, poi_matrix)) = closest_to_pois.top()
        hero_id -= 1

        next_steps = generate_deque(poi_matrix, map.poi.current_poi_coords[poi_id][0], map.poi.current_poi_coords[poi_id][1], map.heroes_array[hero_id].x, map.heroes_array[hero_id].y, False)

        next_steps.append(map.poi.current_poi_coords[poi_id])
        next_steps.popleft()
        
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
        value = matrix[ghost[1]][ghost[0]].current_cost - len(map.ghosts.get_ghosty_neighbors(ghost[0], ghost[1])) * 2

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