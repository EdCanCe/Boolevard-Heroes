from imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from walls import *
    from poi import *
    from ghosts import *
    from map import *
    from hero import *

class ActionList:
    """Genera la lista de acciones posibles
    que puede realizar un héroe en un momento
    dado.
    """
    @staticmethod
    def generate_list(hero: "Hero"):
        """Genera la lista de acciones que se pueden
        realizar en el turno actual.

        Args:
            hero (Hero): El héroe a verificar.

        Returns:
            list[Action]: La lista de acciones posibles a hacer.
        """

        free_path = [0, 2, 4] # El valor que puede tener una casilla para poder ir

        (x, y) = hero.pos

        possible_actions = [] # Aquí se guardarán las posibles acciontes

        # En caso de que tenga una víctima
        if hero.has_victim:
            if hero.map.walls.get_up(x, y) in free_path:
                possible_actions.append(MoveWithVictim(2, hero, 0))
            if hero.map.walls.get_right(x, y) in free_path:
                possible_actions.append(MoveWithVictim(2, hero, 1))
            if hero.map.walls.get_down(x, y) in free_path:
                possible_actions.append(MoveWithVictim(2, hero, 2))
            if hero.map.walls.get_left(x, y) in free_path:
                possible_actions.append(MoveWithVictim(2, hero, 3))

        # Si no tiene víctima, puede pasar por el fuego o caminar normal
        else:
            if hero.map.walls.get_up(x, y) in free_path:
                if hero.map.ghosts.get_up(x, y) != 2:
                    possible_actions.append(Move(1, hero, 0))
            if hero.map.walls.get_right(x, y) in free_path:
                if hero.map.ghosts.get_right(x, y) != 2:
                    possible_actions.append(Move(1, hero, 1))
            if hero.map.walls.get_down(x, y) in free_path:
                if hero.map.ghosts.get_down(x, y) != 2:
                    possible_actions.append(Move(1, hero, 2))
            if hero.map.walls.get_left(x, y) in free_path:
                if hero.map.ghosts.get_left(x, y) != 2:
                    possible_actions.append(Move(1, hero, 3))

        # Se añaden las posibilidades de abrir puertas
        if hero.map.walls.get_up(x, y) == 3:
            possible_actions.append(OpenDoor(1, hero, 0))
        if hero.map.walls.get_right(x, y) == 3:
            possible_actions.append(OpenDoor(1, hero, 1))
        if hero.map.walls.get_down(x, y) == 3:
            possible_actions.append(OpenDoor(1, hero, 2))
        if hero.map.walls.get_left(x, y) == 3:
            possible_actions.append(OpenDoor(1, hero, 3))

        # Se añaden las posibilidades de cerrar puertas
        if hero.map.walls.get_up(x, y) == 2:
            possible_actions.append(CloseDoor(1, hero, 0))
        if hero.map.walls.get_right(x, y) == 2:
            possible_actions.append(CloseDoor(1, hero, 1))
        if hero.map.walls.get_down(x, y) == 2:
            possible_actions.append(CloseDoor(1, hero, 2))
        if hero.map.walls.get_left(x, y) == 2:
            possible_actions.append(CloseDoor(1, hero, 3))

        # Se añaden las posibilidades de dañar paredes
        if hero.map.walls.get_up(x, y) == 1:
            possible_actions.append(DamageWall(2, hero, 0))
        if hero.map.walls.get_right(x, y) == 1:
            possible_actions.append(DamageWall(2, hero, 1))
        if hero.map.walls.get_down(x, y) == 1:
            possible_actions.append(DamageWall(2, hero, 2))
        if hero.map.walls.get_left(x, y) == 1:
            possible_actions.append(DamageWall(2, hero, 3))

        # Se añaden las posibilidades de destruir paredes
        if hero.map.walls.get_up(x, y) == 0.5:
            possible_actions.append(DestroyWall(2, hero, 0))
        if hero.map.walls.get_right(x, y) == 0.5:
            possible_actions.append(DestroyWall(2, hero, 1))
        if hero.map.walls.get_down(x, y) == 0.5:
            possible_actions.append(DestroyWall(2, hero, 2))
        if hero.map.walls.get_left(x, y) == 0.5:
            possible_actions.append(DestroyWall(2, hero, 3))

        # Se añaden las posibilidades de disipar niebla y fantasmas
        if hero.map.ghosts.get_up(x, y) == 1:
            possible_actions.append(ClearFog(1, hero, 0))
        elif hero.map.ghosts.get_up(x, y) == 2:
            possible_actions.append(ScareGhost(1, hero, 0))
            possible_actions.append(RemoveGhost(2, hero, 0))
        if hero.map.ghosts.get_right(x, y) == 1:
            possible_actions.append(ClearFog(1, hero, 1))
        elif hero.map.ghosts.get_right(x, y) == 2:
            possible_actions.append(ScareGhost(1, hero, 1))
            possible_actions.append(RemoveGhost(2, hero, 1))
        if hero.map.ghosts.get_down(x, y) == 1:
            possible_actions.append(ClearFog(1, hero, 2))
        elif hero.map.ghosts.get_down(x, y) == 2:
            possible_actions.append(ScareGhost(1, hero, 2))
            possible_actions.append(RemoveGhost(2, hero, 2))
        if hero.map.ghosts.get_left(x, y) == 1:
            possible_actions.append(ClearFog(1, hero, 3))
        elif hero.map.ghosts.get_left(x, y) == 2:
            possible_actions.append(ScareGhost(1, hero, 3))
            possible_actions.append(RemoveGhost(2, hero, 3))
        if hero.map.ghosts.get_on(x, y) == 1:
            possible_actions.append(ClearFog(1, hero, 4))
        elif hero.map.ghosts.get_on(x, y) == 2:
            possible_actions.append(ScareGhost(1, hero, 4))
            possible_actions.append(RemoveGhost(2, hero, 4))

        # Verifica si actualmente está en fuego
        if hero.map.ghosts.get_on(x, y) != 2:
            possible_actions.append(DoNothing(0, hero, 4))

        filtered_actions = [] # Se guardan las acciones verdaderamente posibles

        # Se filtran las acciones a únicamente las que se puedan usar
        for action in possible_actions:
            if action.is_possible():
                filtered_actions.append(action)

        return filtered_actions

class Action(ABC):
    """Clase abstracta de acción posible a realizar.
    """
    def __init__(self, action_points, hero: Hero, direction):
        """Constructor de la clase de acción

        Args:
            action_points (int): Los puntos de acción que cuesta la acción.
            hero (Hero): El héroe que realizará la acción.
            direction (int): La dirección en que se hará la acción. 
        """

        # Atributos generales para las acciones
        self.action_points = action_points
        self.hero = hero
        self.direction = direction
        self.objective = 0 # Cuánto aporta al objetivo

        # Las posibles direcciones
        self.UP = 0
        self.RIGHT = 1
        self.DOWN = 2
        self.LEFT = 3
        self.SAME = 4

    def update_coords(self):
        (self.current_x, self.current_y) = self.hero.pos
        (self.action_x, self.action_y) = self.hero.pos

        # Actualiza las coordenadas de la acción dependiendo de la dirección
        if self.direction == self.UP:
            self.action_y -= 1
        elif self.direction == self.RIGHT:
            self.action_x += 1
        elif self.direction == self.DOWN:
            self.action_y += 1
        elif self.direction == self.LEFT:
            self.action_x -= 1

    def restore_action_points(self):
        """Se restauran los puntos de acción del héroe."""

        self.hero.action_points += self.action_points

    @abstractmethod
    def is_possible(self):
        """Verifica que la acción sea válida"""
    
        (self.current_x, self.current_y) = self.hero.pos
        (self.action_x, self.action_y) = self.hero.pos

        self.update_coords()

        if self.action_x in [-1, 10] or self.action_y in [-1, 8]:
            return False
    
        return self.action_points <= self.hero.action_points

    @abstractmethod
    def do_action(self):
        """Método abstracto para realizar la acción."""

        self.hero.action_points -= self.action_points

        # TODO: Verifica si alguna de las coordenadas sale del mapa

        pass

class Move(Action):
    """Mueve el héroe a otra casilla siempre y cuando
    no esté cargando con una víctima y la casilla no
    tenga fantasmas.
    """

    def is_possible(self):
        return super().is_possible()

    def do_action(self):
        """Mueve el héroe a otra casilla"""

        super().do_action()

        self.hero.update_position(self.action_x, self.action_y)
        
        agent = {
            "x": self.action_x,
            "y": self.action_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe en movimiento",
            "order": self.hero.order
        }

        self.hero.json["agents"].append(agent)

        return True

class MoveWithVictim(Action):
    """Mueve el héroe a otra casilla mientras carga una
    víctima.
    """

    def is_possible(self):
        # Verifica que la casilla no tenga fantasmas
        self.update_coords()

        if self.action_x in [-1, 10] or self.action_y in [-1, 8]:
            return False
        
        if self.hero.map.ghosts.get_on(self.action_x, self.action_y) == 2:
            return False

        # Verifica por puntos de acción
        return self.action_points <= self.hero.action_points
    
    

    def do_action(self):
        """Mueve el héroe y la víctima a otra casilla"""

        super().do_action()

        self.hero.update_position(self.action_x, self.action_y)

        # Verifica si acaba de salvar a la persona
        if self.action_x in [0, 10] or self.action_y in [0, 8]:
            self.hero.map.poi.rescued_victims += 1
            self.hero.has_victim = False # Ya que ya salvó la víctima

        agent = {
            "x": self.action_x,
            "y": self.action_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe en movimiento con victima",
            "order": self.hero.order
        }

        # TODO: En unity modificar el sprite del agente segun su estado de carrying
        # TODO: En caso de que si, mostrar un mensaje de cambio

        self.hero.json["agents"].append(agent)

        return True

class OpenDoor(Action):
    """Abre una puerta alrededor del héroe."""

    def is_possible(self):
        return super().is_possible()

    def do_action(self):
        """Abre la puerta."""

        super().do_action()

        if self.direction == self.UP:
            self.hero.map.walls.set_up(self.current_x, self.current_y, 2)
        elif self.direction == self.RIGHT:
            self.hero.map.walls.set_right(self.current_x, self.current_y, 2)
        elif self.direction == self.DOWN:
            self.hero.map.walls.set_down(self.current_x, self.current_y, 2)
        elif self.direction == self.LEFT:
            self.hero.map.walls.set_left(self.current_x, self.current_y, 2)

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe abre una puerta",
            "order": self.hero.order
        }

        wall = {
            "direction": self.direction, # direccion a la que apunta
            "status": 2, # puerta abierta
            "order": self.hero.order,
            "x": self.current_x,
            "y": self.current_y
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["walls"].append(wall)

        return True

class CloseDoor(Action):
    """Cierra una puerta alrededor del héroe."""

    def is_possible(self):
        return super().is_possible()

    def do_action(self):
        """Cierra la puerta."""

        super().do_action()

        if self.direction == self.UP:
            self.hero.map.walls.set_up(self.current_x, self.current_y, 3)
        elif self.direction == self.RIGHT:
            self.hero.map.walls.set_right(self.current_x, self.current_y, 3)
        elif self.direction == self.DOWN:
            self.hero.map.walls.set_down(self.current_x, self.current_y, 3)
        elif self.direction == self.LEFT:
            self.hero.map.walls.set_left(self.current_x, self.current_y, 3)

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe cierra una puerta",
            "order": self.hero.order
        }

        wall = {
            "direction": self.direction, # direccion a la que apunta
            "status": 3, # puerta cerrado
            "order": self.hero.order,
            "x": self.current_x,
            "y": self.current_y
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["walls"].append(wall)

        return True

class DamageWall(Action):
    """Daña una pared alrededor del héroe."""

    def is_possible(self):
        return super().is_possible()

    def do_action(self):
        """Daña la pared."""

        super().do_action()

        if self.direction == self.UP:
            self.hero.map.walls.set_up(self.current_x, self.current_y, 0.5)
        elif self.direction == self.RIGHT:
            self.hero.map.walls.set_right(self.current_x, self.current_y, 0.5)
        elif self.direction == self.DOWN:
            self.hero.map.walls.set_down(self.current_x, self.current_y, 0.5)
        elif self.direction == self.LEFT:
            self.hero.map.walls.set_left(self.current_x, self.current_y, 0.5)

        self.hero.map.damage_points += 1

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe dañó una pared",
            "order": self.hero.order
        }

        wall = {
            "direction": self.direction, # direccion a la que apunta
            "status": 0.5, # pared dañada
            "order": self.hero.order,
            "x": self.current_x,
            "y": self.current_y
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["walls"].append(wall)

        return True

class DestroyWall(Action):
    """Destruye una pared alrededor del héroe."""

    def is_possible(self):
        return super().is_possible()

    def do_action(self):
        """Destruye la pared."""

        super().do_action()

        if self.direction == self.UP:
            self.hero.map.walls.set_up(self.current_x, self.current_y, 0)
        elif self.direction == self.RIGHT:
            self.hero.map.walls.set_right(self.current_x, self.current_y, 0)
        elif self.direction == self.DOWN:
            self.hero.map.walls.set_down(self.current_x, self.current_y, 0)
        elif self.direction == self.LEFT:
            self.hero.map.walls.set_left(self.current_x, self.current_y, 0)

        self.hero.map.damage_points += 1

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe ha tumbado una pared",
            "order": self.hero.order
        }

        wall = {
            "direction": self.direction, # direccion a la que apunta
            "status": 0, # pared destruida
            "order": self.hero.order,
            "x": self.current_x,
            "y": self.current_y
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["walls"].append(wall)

        return True

class ClearFog(Action):
    """Dispersa una niebla alrededor del héroe."""

    def is_possible(self):
        (self.current_x, self.current_y) = self.hero.pos
        (self.action_x, self.action_y) = self.hero.pos

        self.update_coords()

        if not (self.action_x, self.action_y) in self.hero.map.walls.get_neighbors(self.current_x, self.current_y) and (self.action_x, self.action_y) != (self.current_x, self.current_y):
            return False

        return super().is_possible()

    def do_action(self):
        """Dispersa la niebla alrededor del héroe."""

        super().do_action()

        self.hero.map.ghosts.set_on(self.action_x, self.action_y, 0)

        self.hero.map.ghosts.fog_list.remove((self.action_x, self.action_y))

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe dispersa una niebla",
            "order": self.hero.order
        }

        ghost = {
            "x": self.action_x,
            "y": self.action_y,
            "status": 0, # sin niebla
            "order": self.hero.order
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["ghosts"].append(ghost)

        return True

class ScareGhost(Action):
    """Ahuyenta un fantasma alrededor del héroe."""

    def is_possible(self):
        (self.current_x, self.current_y) = self.hero.pos
        (self.action_x, self.action_y) = self.hero.pos

        self.update_coords()

        if not (self.action_x, self.action_y) in self.hero.map.walls.get_neighbors(self.current_x, self.current_y) and (self.action_x, self.action_y) != (self.current_x, self.current_y):
            return False

        return super().is_possible()
    
    def do_action(self):
        """Ahuyenta el fantasma."""

        super().do_action()

        self.hero.map.ghosts.set_on(self.action_x, self.action_y, 1)
        self.hero.map.ghosts.fog_list.append((self.action_x, self.action_y))

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe ahuyenta un fantasma a niebla",
            "order": self.hero.order
        }

        ghost = {
            "x": self.action_x,
            "y": self.action_y,
            "status": 1, # establecer niebla
            "order": self.hero.order
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["ghosts"].append(ghost)

        return True

class RemoveGhost(Action):
    """Remueve un fantasma alrededor del héroe."""

    def is_possible(self):
        (self.current_x, self.current_y) = self.hero.pos
        (self.action_x, self.action_y) = self.hero.pos

        self.update_coords()

        if not (self.action_x, self.action_y) in self.hero.map.walls.get_neighbors(self.current_x, self.current_y) and (self.action_x, self.action_y) != (self.current_x, self.current_y):
            return False

        return super().is_possible()

    def do_action(self):
        """Remueve el fantasma."""

        super().do_action()

        self.hero.map.ghosts.set_on(self.action_x, self.action_y, 0)

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe ahuyenta un fantasma por completo",
            "order": self.hero.order
        }

        ghost = {
            "x": self.action_x,
            "y": self.action_y,
            "status": 0, # sin niebla
            "order": self.hero.order
        }

        self.hero.json["agents"].append(agent)
        self.hero.json["ghosts"].append(ghost)

        return True

class DoNothing(Action):
    """Guarda los puntos de acción restantes del héroe
    con intención de iniciar el siguiente turno.
    """

    def is_possible(self):
        return super().is_possible()

    def do_action(self):
        """Guarda los puntos de acción."""

        super().do_action()

        self.hero.stored_action_points = min(self.hero.action_points, 4)
        self.hero.action_points = 0

        agent = {
            "x": self.current_x,
            "y": self.current_y,
            "id": self.hero.id,
            "carrying": self.hero.has_victim,
            "energy": self.hero.action_points,
            "action": "héroe espera en su casilla",
            "order": self.hero.order
        }

        self.hero.json["agents"].append(agent)

        return True