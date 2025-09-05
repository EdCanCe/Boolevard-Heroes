import numpy as np
from mesa.space import MultiGrid

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

    def __init__(self, ghosts):
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

        if self.ghosts.dashboard[y][x] in [1, 2]:
            # Si la casilla contiene ciertos valores de ghosts, los elimina
            self.ghosts.dashboard[y][x] = 0

        self.current += 1 # Se aumenta la cantidad de POIs en el tablero
        self.added_pois.append((x, y))

    def remove(self, x, y):
        """Remueve del tablero un POI (no modifica los valores
        de falsos y víctimas)
        """
        
        self.current -= 1
        self.dashboard[y][x] = 0  # Remueve el POI
        
        # TODO: añadir al JSON que se quitó un poi

    def willBeRescued(self, x, y):
        """Marca en el mapa un 0, ya que el POI lo
        llevaría el héroe
        """

        self.dashboard[y][x] = 0

    def move(self, old_x, old_y, new_x, new_y):
        """Mueve un POI a otra casilla."""
        
        self.dashboard[old_y][old_x], self.dashboard[new_y][new_x] = self.dashboard[new_y][new_x], self.dashboard[old_y][old_x]

        # TODO: añadir al JSON que se movió el poi