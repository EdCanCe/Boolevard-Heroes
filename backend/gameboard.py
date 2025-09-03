# Clase para manejar el estado actual del tablero
class GameBoard:
    # Las matrices de paredes y puertas
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

    # Getters y setters para las puertas y paredes alrededor de las casillas
    @staticmethod
    def get_left(x, y):
        if x <= 0:
            return -1
        return GameBoard.vertical[y][x-1]

    @staticmethod
    def set_left(x, y, value):
        if x <= 0:
            return
        GameBoard.vertical[y][x-1] = value

    @staticmethod
    def get_right(x, y):
        if x >= 9:
            return -1
        return GameBoard.vertical[y][x]

    @staticmethod
    def set_right(x, y, value):
        if x >= 9:
            return
        GameBoard.vertical[y][x] = value

    @staticmethod
    def get_up(x, y):
        if y <= 0:
            return -1
        return GameBoard.horizontal[y-1][x]

    @staticmethod
    def set_up(x, y, value):
        if y <= 0:
            return
        GameBoard.horizontal[y-1][x] = value

    @staticmethod
    def get_down(x, y):
        if y >= 7:
            return -1
        return GameBoard.horizontal[y][x]

    @staticmethod
    def set_down(x, y, value):
        if y >= 7:
            return
        GameBoard.horizontal[y][x] = value

    # Obtiene los vecinos dependiendo de las casillas de alrededor
    @staticmethod
    def get_neighbors(x, y):
        neighbors = []

        # Estados donde no hay pared, hay puerta abierta o destruida
        accepted_values = [0, 2, 4]

        # Se verifica que dicho elemento sea accesible
        if GameBoard.get_left(x, y) in accepted_values:
            neighbors.append((x-1, y))

        if GameBoard.get_right(x, y) in accepted_values:
            neighbors.append((x+1, y))

        if GameBoard.get_up(x, y) in accepted_values:
            neighbors.append((x, y-1))

        if GameBoard.get_down(x, y) in accepted_values:
            neighbors.append((x, y+1))

        return neighbors
