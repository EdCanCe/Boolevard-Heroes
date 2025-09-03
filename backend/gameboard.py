class GameBoard:
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

    vertical = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 3, 0, 1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 3, 0, 0, 1, 0],
        [3, 0, 3, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 3, 0, 3, 0],
        [1, 0, 0, 0, 0, 1, 0, 1, 1, 0],
        [1, 0, 0, 0, 0, 3, 0, 3, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    horizontal = [
        [0, 1, 1, 1, 1, 1, 3, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 3, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 3, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    # Métodos de acceso a paredes y puertas
    @staticmethod
    def get_left(x, y):
        """Devuelve el estado de la pared/puerta a la izquierda de (x, y).

        Args:
            x (int): Coordenada en el eje X.
            y (int): Coordenada en el eje Y.

        Returns:
            float: Estado de la pared/puerta.
        """
        if x <= 0:
            return -1
        return GameBoard.vertical[y][x-1]

    @staticmethod
    def set_left(x, y, value):
        """Asigna un valor a la pared/puerta izquierda de (x, y).

        Args:
            x (int): Coordenada en el eje X.
            y (int): Coordenada en el eje Y.
            value (float): Nuevo valor para la pared/puerta.
        """
        if x <= 0:
            return
        GameBoard.vertical[y][x-1] = value

    @staticmethod
    def get_right(x, y):
        """Devuelve el estado de la pared/puerta a la derecha de (x, y).

        Args:
            x (int): Coordenada en el eje X.
            y (int): Coordenada en el eje Y.

        Returns:
            float: Estado de la pared/puerta.
        """
        if x >= 9:
            return -1
        return GameBoard.vertical[y][x]

    @staticmethod
    def set_right(x, y, value):
        """Asigna un valor a la pared/puerta derecha de (x, y).

        Args:
            x (int): Coordenada en el eje X.
            y (int): Coordenada en el eje Y.
            value (float): Nuevo valor para la pared/puerta.
        """
        if x >= 9:
            return
        GameBoard.vertical[y][x] = value

    @staticmethod
    def get_up(x, y):
        """Devuelve el estado de la pared/puerta arriba de (x, y).

        Args:
            x (int): Coordenada en el eje X.
            y (int): Coordenada en el eje Y.

        Returns:
            float: Estado de la pared/puerta.
        """
        if y <= 0:
            return -1
        return GameBoard.horizontal[y-1][x]

    @staticmethod
    def set_up(x, y, value):
        """Asigna un valor a la pared/puerta arriba de (x, y).

        Args:
            x (int): Coordenada en el eje X.
            y (int): Coordenada en el eje Y.
            value (float): Nuevo valor para la pared/puerta.
        """
        if y <= 0:
            return
        GameBoard.horizontal[y-1][x] = value

    @staticmethod
    def get_down(x, y):
        """Devuelve el estado de la pared/puerta abajo de (x, y).

        Args:
            x (int): Coordenada en el eje X.
            y (int): Coordenada en el eje Y.

        Returns:
            float: Estado de la pared/puerta.
        """
        if y >= 7:
            return -1
        return GameBoard.horizontal[y][x]

    @staticmethod
    def set_down(x, y, value):
        """Asigna un valor a la pared/puerta abajo de (x, y).

        Args:
            x (int): Coordenada en el eje X.
            y (int): Coordenada en el eje Y.
            value (float): Nuevo valor para la pared/puerta.
        """
        if y >= 7:
            return
        GameBoard.horizontal[y][x] = value

    # Métodos auxiliares
    @staticmethod
    def get_neighbors(x, y):
        """Obtiene las casillas adyacentes accesibles desde (x, y).

        Una casilla es vecina si no hay pared, o si hay una puerta abierta
        o destruida.

        Args:
            x (int): Coordenada en el eje X.
            y (int): Coordenada en el eje Y.

        Returns:
            list[tuple[int, int]]: Lista de coordenadas de casillas adyacentes.
        """
        neighbors = []
        accepted_values = [0, 2, 4]  # accesibles

        if GameBoard.get_left(x, y) in accepted_values:
            neighbors.append((x-1, y))

        if GameBoard.get_right(x, y) in accepted_values:
            neighbors.append((x+1, y))

        if GameBoard.get_up(x, y) in accepted_values:
            neighbors.append((x, y-1))

        if GameBoard.get_down(x, y) in accepted_values:
            neighbors.append((x, y+1))

        return neighbors