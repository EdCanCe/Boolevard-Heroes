from ghosts import *
import numpy as np

class POI:
    """Clase que gestiona los puntos de interés (POI) en el tablero.

    Attributes:
        POI_dashboard (list[list[int]]): Matriz que indica la ubicación de los POI.
            0 -> vacío
            3 -> POI
        real_victims (np.ndarray): Vector de víctimas reales.
        false_alarms (np.ndarray): Vector de falsas alarmas.
        poi (np.ndarray): Vector combinado de víctimas y falsas alarmas.
    """

    # ----- Tablero de POI -----
    POI_dashboard = [
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
    @staticmethod
    def pick_poi():
        """Selecciona un POI aleatoriamente y lo elimina del vector.

        Returns:
            int: Valor del POI seleccionado (4 o 5), o -1 si no quedan POI.
        """
        if len(POI.poi) <= 0:
            return -1

        np.random.shuffle(POI.poi)
        poi_value = POI.poi[0]
        POI.poi = np.delete(POI.poi, 0)
        return poi_value

    # ----- Colocación de un POI en el tablero -----
    @staticmethod
    def place_poi():
        """Coloca un POI en el tablero en coordenadas aleatorias libres.

        Returns:
            int: -1 si no se pudo colocar el POI, None si se colocó correctamente.
        """
        x, y = FoggyGhost.generate_coords()

        while POI.POI_dashboard[y][x] != 0:
            x, y = FoggyGhost.generate_coords()

        if POI.POI_dashboard[y][x] == 0:
            POI.POI_dashboard[y][x] = 3

        elif FoggyGhost.dashboard[y][x] in [1, 2]:
            FoggyGhost.dashboard[y][x] = 0
            POI.POI_dashboard[y][x] = 3

        else:
            return -1
