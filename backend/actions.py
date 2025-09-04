from abc import ABC, abstractmethod
from hero import *

class ActionList:
    """Genera la lista de acciones posibles
    que puede realizar un héroe en un momento
    dado.
    """
    @staticmethod
    def generate_list(hero: Hero):
        """Genera la lista de acciones que se pueden
        realizar en el turno actual.

        Args:
            hero (Hero): El héroe a verificar.

        Returns:
            list[Action]: La lista de acciones posibles a hacer.
        """

        free_path = [0, 2, 4] # El valor que puede tener una casilla para poder ir

        (x, y) = hero.pos

        possible_actions = [Action] # Aquí se guardarán las posibles acciontes

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
                if hero.map.ghosts.get_up(x, y) == 2:
                    possible_actions.append(MoveIntoGhost(2, hero, 0))
                else:
                    possible_actions.append(Move(1, hero, 0))
            if hero.map.walls.get_right(x, y) in free_path:
                if hero.map.ghosts.get_right(x, y) == 2:
                    possible_actions.append(MoveIntoGhost(2, hero, 1))
                else:
                    possible_actions.append(Move(1, hero, 0))
            if hero.map.walls.get_down(x, y) in free_path:
                if hero.map.ghosts.get_down(x, y) == 2:
                    possible_actions.append(MoveIntoGhost(2, hero, 2))
                else:
                    possible_actions.append(Move(1, hero, 0))
            if hero.map.walls.get_left(x, y) in free_path:
                if hero.map.ghosts.get_left(x, y) == 2:
                    possible_actions.append(MoveIntoGhost(2, hero, 3))
                else:
                    possible_actions.append(Move(1, hero, 0))

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

        filtered_actions = [Action] # Se guardan las acciones verdaderamente posibles

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

    @abstractmethod
    def is_possible(self):
        """Verifica que la acción sea válida"""
        return self.action_points <= self.hero.action_points
    
        pass

    @abstractmethod
    def do_action(self):
        """Método abstracto para realizar la acción."""

        self.hero.action_points -= self.action_points

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

        pass

class Move(Action):
    """Mueve el héroe a otra casilla siempre y cuando
    no esté cargando con una víctima y la casilla no
    tenga fantasmas.
    """

    def do_action(self):
        """Mueve el héroe a otra casilla"""

        super().do_action()

        self.hero.update_position(self.action_x, self.action_y)

        # TODO: Añadir lo correspondiente al JSON

        return True

class MoveWithVictim(Action):
    """Mueve el héroe a otra casilla mientras carga una
    víctima.
    """

    def is_possible(self):
        # Verifica que la casilla no tenga fantasmas
        if self.hero.map.ghosts.get_on(self.action_x, self.action_y) == 2:
            return False
        
        # Verifica por puntos de acción
        return self.action_points <= self.hero.action_points

    def do_action(self):
        """Mueve el héroe y la víctima a otra casilla"""

        super().do_action()

        self.hero.update_position(self.action_x, self.action_y)
        self.hero.map.poi.move_poi(self.current_x, self.current_y, self.action_x, self.action_y)

        # TODO: Añadir lo correspondiente al JSON

        return True

class MoveIntoGhost(Action):
    """Mueve el héroe a otra casilla que tenga un
    fantasma dentro de ella.
    """

    def do_action(self):
        """Mueve al héroe a la casilla con el fantasma."""

        super().do_action()

        self.hero.update_position(self.action_x, self.action_y)

        # TODO: Verificar que no se quede dentro del fuego
        # TODO: Añadir lo correspondiente al JSON

        # ! Se modifica el método de requisito, se verifica que en la nueva posición, restándole los puntos, tenga otra posible acción. Y dentro del arreglo de generación, NO se añade el "no hacer nada" si está dentro del fuego

        # ! O mas bien añadir una especie de bfs dentro de la generación del arreglo/

class OpenDoor(Action):
    """Abre una puerta alrededor del héroe."""

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

        # TODO: Añadir lo correspondiente al JSON

        return True

class CloseDoor(Action):
    """Cierra una puerta alrededor del héroe."""

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

        # TODO: Añadir lo correspondiente al JSON

        return True

class DamageWall(Action):
    """Daña una pared alrededor del héroe."""

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

        # TODO: Añadir lo correspondiente al JSON

        return True

class DestroyWall(Action):
    """Destruye una pared alrededor del héroe."""

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

        # TODO: Añadir lo correspondiente al JSON

        return True

class ClearFog(Action):
    """Dispersa una niebla alrededor del héroe."""

    def do_action(self):
        """Dispersa la niebla alrededor del héroe."""

        super().do_action()

        self.hero.map.ghosts.set_in(self.action_x, self.action_y, 0)

        # TODO: Añadir lo correspondiente al JSON

        return True

class ScareGhost(Action):
    """Ahuyenta un fantasma alrededor del héroe."""

    def do_action(self):
        """Ahuyenta el fantasma."""

        super().do_action()

        self.hero.map.ghosts.set_in(self.action_x, self.action_y, 1)

        # TODO: Añadir lo correspondiente al JSON

        return True

class RemoveGhost(Action):
    """Remueve un fantasma alrededor del héroe."""

    def do_action(self):
        """Remueve el fantasma."""

        super().do_action()

        self.hero.map.ghosts.set_in(self.action_x, self.action_y, 0)

        # TODO: Añadir lo correspondiente al JSON

        return True

class DoNothing(Action):
    """Guarda los puntos de acción restantes del héroe
    con intención de iniciar el siguiente turno.
    """

    def do_action(self):
        """Guarda los puntos de acción."""

        super().do_action()

        self.hero.stored_action_points = min(self.hero.action_points, 4)

        # TODO: Añadir lo correspondiente al JSON

        return True