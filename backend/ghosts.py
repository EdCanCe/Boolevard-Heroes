from gameboard import *
import numpy as np
from collections import deque

class FoggyGhost:
    dashboard = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 2, 2, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    @staticmethod
    def generate_coords():
        x = np.random.randint(1, 9)  # 1 - 8
        y = np.random.randint(1, 7)  # 1 - 6
        return (x, y)

    # GETTERS
    @staticmethod
    def get_up(x, y):
        if y <= 1 or y >= 7:
            return -1
        return FoggyGhost.dashboard[y - 1][x]

    @staticmethod
    def get_down(x, y):
        if y <= 0 or y >= 6:
            return -1
        return FoggyGhost.dashboard[y + 1][x]

    @staticmethod
    def get_left(x, y):
        if x <= 1 or x >= 9:
            return -1
        return FoggyGhost.dashboard[y][x - 1]

    @staticmethod
    def get_right(x, y):
        if x <= 0 or x >= 8:
            return -1
        return FoggyGhost.dashboard[y][x + 1]

    # SETTERS
    @staticmethod
    def set_up(x, y, value):
        if y <= 1 or y >= 7:
            return
        FoggyGhost.dashboard[y - 1][x] = value

    @staticmethod
    def set_down(x, y, value):
        if y <= 0 or y >= 6:
            return
        FoggyGhost.dashboard[y + 1][x] = value

    @staticmethod
    def set_left(x, y, value):
        if x <= 1 or x >= 9:
            return
        FoggyGhost.dashboard[y][x - 1] = value

    @staticmethod
    def set_right(x, y, value):
        if x <= 0 or x >= 8:
            return
        FoggyGhost.dashboard[y][x + 1] = value

    @staticmethod
    def get_foggy_neighbors(x, y):
        neighbors = GameBoard.get_neighbors(x, y)
        fog = 1
        foggy_neighbors = []

        for n in neighbors:
            current_x, current_y = n
            if FoggyGhost.dashboard[current_y][current_x] == fog:
                foggy_neighbors.append((current_x, current_y))

        return foggy_neighbors

    @staticmethod
    def spread_fire(x, y):
        q = deque()
        visited = set()

        q.append((x, y))
        visited.add((x, y))

        while q:
            current_x, current_y = q.popleft()
            neighbors = FoggyGhost.get_foggy_neighbors(current_x, current_y)
            for new_x, new_y in neighbors:
                print(new_x, new_y)
                if (new_x, new_y) in visited:
                    continue

                visited.add((new_x, new_y))

                if FoggyGhost.dashboard[new_y][new_x] == 1:
                    FoggyGhost.dashboard[new_y][new_x] = 2
                    q.append((new_x, new_y))

    @staticmethod
    def board_length(x, y):
        return 1 <= x <= 8 and 1 <= y <= 6

    @staticmethod
    def surge(x, y):
        # directions: up, right, down, left
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        for diff_x, diff_y in directions:
            current_x, current_y = (x, y)

            while True:
                new_x = current_x + diff_x
                new_y = current_y + diff_y

                # out of bounds/boardgame
                out_of_bounds = not FoggyGhost.board_length(new_x, new_y)

                # Right
                if diff_x == 1 and diff_y == 0:
                    value = GameBoard.get_right(current_x, current_y)

                # Left
                elif diff_x == -1 and diff_y == 0:
                    value = GameBoard.get_left(current_x, current_y)

                # Up
                elif diff_x == 0 and diff_y == -1:
                    value = GameBoard.get_up(current_x, current_y)

                # Down
                elif diff_x == 0 and diff_y == 1:
                    value = GameBoard.get_down(current_x, current_y)

                # Error
                else:
                    break

                if value == -1:  # Not found a value
                    break

                # Flags
                can_pass = False
                can_end = False

                # Right
                if diff_x == 1 and diff_y == 0:
                    if value == 0:  # Empty space
                        can_pass = True
                    elif value == 0.5:  # Damaged wall
                        GameBoard.set_right(current_x, current_y, 0)
                        can_end = True
                    elif value == 1:  # Full wall
                        GameBoard.set_right(current_x, current_y, 0.5)
                        can_end = True
                    elif value == 2 or value == 4:  # Open/destroyed door
                        GameBoard.set_right(current_x, current_y, 4)
                        can_pass = True
                    elif value == 3:  # Closed door
                        GameBoard.set_right(current_x, current_y, 4)
                        can_end = True
                    else:
                        can_pass = True

                # Left
                elif diff_x == -1 and diff_y == 0:
                    if value == 0:
                        can_pass = True
                    elif value == 0.5:
                        GameBoard.set_left(current_x, current_y, 0)
                        can_end = True
                    elif value == 1:
                        GameBoard.set_left(current_x, current_y, 0.5)
                        can_end = True
                    elif value == 2 or value == 4:
                        GameBoard.set_left(current_x, current_y, 4)
                        can_pass = True
                    elif value == 3:
                        GameBoard.set_left(current_x, current_y, 4)
                        can_end = True
                    else:
                        can_pass = True

                # Up
                elif diff_x == 0 and diff_y == -1:
                    if value == 0:
                        can_pass = True
                    elif value == 0.5:
                        GameBoard.set_up(current_x, current_y, 0)
                        can_end = True
                    elif value == 1:
                        GameBoard.set_up(current_x, current_y, 0.5)
                        can_end = True
                    elif value == 2 or value == 4:
                        GameBoard.set_up(current_x, current_y, 4)
                        can_pass = True
                    elif value == 3:
                        GameBoard.set_up(current_x, current_y, 4)
                        can_end = True
                    else:
                        can_pass = True

                # Down
                elif diff_x == 0 and diff_y == 1:
                    if value == 0:
                        can_pass = True
                    elif value == 0.5:
                        GameBoard.set_down(current_x, current_y, 0)
                        can_end = True
                    elif value == 1:
                        GameBoard.set_down(current_x, current_y, 0.5)
                        can_end = True
                    elif value == 2 or value == 4:
                        GameBoard.set_down(current_x, current_y, 4)
                        can_pass = True
                    elif value == 3:
                        GameBoard.set_down(current_x, current_y, 4)
                        can_end = True
                    else:
                        can_pass = True

                if can_end or out_of_bounds:
                    break

                value_ghost = FoggyGhost.dashboard[new_y][new_x]

                if value_ghost == 0 or value_ghost == 1:
                    FoggyGhost.dashboard[new_y][new_x] = 2  # place ghost
                    break
                elif value_ghost == 2:  # Already a ghost
                    current_x, current_y = (new_x, new_y)
                    continue
                else:
                    FoggyGhost.dashboard[new_y][new_x] = 2
                    break

    # For testing
    @staticmethod
    def place_fog(x, y):
        # (x, y) = FoggyGhost.generate_coords()  # random coordinates

        if FoggyGhost.dashboard[y][x] == 0:
            FoggyGhost.dashboard[y][x] = 1  # place fog

        if FoggyGhost.dashboard[y][x] == 1:
            FoggyGhost.dashboard[y][x] = 2  # place ghost
            FoggyGhost.spread_fire(x, y)

        if FoggyGhost.dashboard[y][x] == 2:  # a ghost
            FoggyGhost.surge(x, y)  # occurred an explosion/surge
