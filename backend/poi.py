import numpy as np

class POI:
    """Gestiona los puntos de interés (POI) en el tablero de juego.

    La clase maneja la ubicación de los POI y controla vectores de
    víctimas reales y falsas alarmas.

    Attributes:
        dashboard (list[list[int]]): Matriz que indica la ubicación de los POI.
            0 -> vacío
            3 -> POI
        real_victims (np.ndarray): Vector de víctimas reales (valor 4).
        false_alarms (np.ndarray): Vector de falsas alarmas (valor 5).
        poi (np.ndarray): Vector combinado de víctimas y falsas alarmas.
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
    real_victims = np.full(12, 4)  # 12 víctimas reales
    false_alarms = np.full(6, 5)   # 6 falsas alarmas
    poi = np.concatenate((real_victims, false_alarms))  # Se combinan ambos vectores

    def pick_poi(self):
        """Selecciona un POI aleatoriamente y lo elimina del vector.

        Returns:
            int: Valor del POI seleccionado.
        """
        if len(self.poi) <= 0:
            return -1  # No hay POI disponibles

        # Mezcla el vector y selecciona el primer POI
        np.random.shuffle(self.poi)
        poi_value = self.poi[0]

        # Elimina el POI seleccionado del vector
        self.poi = np.delete(self.poi, 0)
        return poi_value

    def place_poi(self):
        """Coloca un POI en el tablero en coordenadas aleatorias libres.

        Verifica que la casilla esté libre o reemplaza ciertos valores
        del tablero de ghosts si es necesario.

        Returns:
            int: -1 si no se pudo colocar el POI, o none si se colocó correctamente.
        """
        x, y = self.ghosts.generate_coords()  # Genera coordenadas aleatorias

        # Busca una casilla libre en el tablero
        while self.dashboard[y][x] != 0:
            x, y = self.ghosts.generate_coords()

        if self.dashboard[y][x] == 0:
            self.dashboard[y][x] = 3  # Coloca el POI en la casilla libre

        elif self.ghosts.dashboard[y][x] in [1, 2]:
            # Si la casilla contiene ciertos valores de ghosts, los elimina
            self.ghosts.dashboard[y][x] = 0
            self.dashboard[y][x] = 3  # Coloca el POI

        else:
            return -1  # No se pudo colocar el POI
