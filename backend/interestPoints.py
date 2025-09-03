from ghosts import *
import numpy as np

class POI:
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

    real_victims = np.full(12, 4)  # vector with twelve 4's
    false_alarms = np.full(6, 5)  # vector with six 5's
    poi = np.concatenate((real_victims, false_alarms))  # vector with victims + false alarms

    @staticmethod
    def pick_poi():
        if len(POI.poi) <= 0:  # is empty?
            return -1
        np.random.shuffle(POI.poi)
        poi_value = POI.poi[0]
        POI.poi = np.delete(POI.poi, 0)
        return poi_value

    @staticmethod
    def place_poi():
        x, y = FoggyGhost.generate_coords()  # random coordinates

        while POI.POI_dashboard[y][x] != 0:  # repeat until empty coords found
            x, y = FoggyGhost.generate_coords()  # random coordinates

        if POI.POI_dashboard[y][x] == 0:  # Empty space in POI dashboard
            POI.POI_dashboard[y][x] = 3  # place POI

        elif FoggyGhost.dashboard[y][x] == 2 or FoggyGhost.dashboard[y][x] == 1:  # ghost or fog
            FoggyGhost.dashboard[y][x] = 0  # remove ghost or fog
            POI.POI_dashboard[y][x] = 3

        else:
            return -1
