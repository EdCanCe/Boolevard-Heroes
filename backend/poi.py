import numpy as np

class POI:
    """Clase que gestiona los puntos de interés (POI) en el tablero.

    Attributes:
        dashboard (list[list[int]]): Matriz que indica la ubicación de los POI.
            0 -> vacío
            3 -> POI
        real_victims (np.ndarray): Vector de víctimas reales.
        false_alarms (np.ndarray): Vector de falsas alarmas.
        poi (np.ndarray): Vector combinado de víctimas y falsas alarmas.
    """

    def __init__(self, ghosts):
        """Inicializa las variables de la clase.
        """
        self.ghosts = ghosts
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

    # ----- Vectores de víctimas y falsas alarmas -----
    real_victims = np.full(12, 4)
    false_alarms = np.full(6, 5)
    poi = np.concatenate((real_victims, false_alarms)) # Se juntan ambos vectores

    # ----- Selección aleatoria de un POI -----
    def pick_poi(self):
        """Selecciona un POI aleatoriamente y lo elimina del vector.

        Returns:
            int: Valor del POI seleccionado (4 o 5).
        """
        if len(self.poi) <= 0:
            return -1

        np.random.shuffle(self.poi)
        poi_value = self.poi[0]
        self.poi = np.delete(self.poi, 0)
        return poi_value

    # ----- Colocación de un POI en el tablero -----
    def place_poi(self):
        """Coloca un POI en el tablero en coordenadas aleatorias libres.

        Returns:
            int: -1 si no se pudo colocar el POI, None si se colocó correctamente.
        """
        x, y = self.ghosts.generate_coords()

        while self.dashboard[y][x] != 0:
            x, y = self.ghosts.generate_coords()

        if self.dashboard[y][x] == 0:
            self.dashboard[y][x] = 3

        elif self.ghosts.dashboard[y][x] in [1, 2]:
            self.ghosts.dashboard[y][x] = 0
            self.dashboard[y][x] = 3

        else:
            return -1
