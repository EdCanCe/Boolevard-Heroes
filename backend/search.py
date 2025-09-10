from imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from walls import *
    from poi import *
    from ghosts import *
    from map import *
    from actions import *

class MapNode():
    def __init__(self, x, y, parent: "MapNode"):
        self.x = x
        self.y = y
        self.parent = parent

def a_star(map: "Map", start_x, start_y, end_x, end_y):
    """Genera una deque de las posicio

    Args:
        map (Map): _description_
        x (_type_): _description_
        y (_type_): _description_
    """