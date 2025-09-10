from imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from walls import *
    from poi import *
    from ghosts import *
    from map import *
    from actions import *

class MapNode:
    def __init__(self, x, y, current_cost, parent: "MapNode"):
        self.x = x
        self.y = y
        self.current_cost = current_cost
        self.parent = parent

class PriorityQueue:
    def __init__(self):
        self.__data = []

    # Función para verificar si la fila de prioridades está vacía
    def empty(self):
        return not self.__data

    # Función para limpiar la fila de prioridades
    def clear(self):
        self.__data.clear()
    
    # Función para insertar un elemento en la fila de prioridades
    def push(self, priority, value):
        heapq.heappush(self.__data, (priority, value))

    # Función para extraer el elemento con mayor prioridad (menor número)
    def pop(self):
        if self.__data: # not empty
            heapq.heappop(self.__data)
        else:
            raise Exception("No such element")
        
    # Función para obtener el primer elemento sin sacarlo
    def top(self):
        if self.__data: # not empty
            return self.__data[0]
        else:
            raise Exception("No such element")
        
def heuristic(start_x, start_y, end_x, end_y):
    manhattan = abs(start_x - end_x) + abs(start_y - end_y)
    return manhattan

def neigbors_with_cost(map: "Map", x, y, movement_type):
    """Obtiene los vecinos de una casilla, con el costo
    para poder llegar a éstas.
    """

    neighbors = []

    multiplier = 3
    if movement_type == 2: # En caso de que su intención sea quitar fantasmas
        multiplier = 0.7

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

def generate_deque(matrix: list[list[MapNode]], start_x, start_y, end_x, end_y):
    next_steps = deque()
    current_x = end_x
    current_y = end_y
    while (current_x, current_y) != (start_x, start_y):
        next_steps.appendleft((current_x, current_y))
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
    matrix = dijkstra(map, start_x, start_y, movement_type)
    return generate_deque(matrix, start_x, start_y, end_x, end_y)