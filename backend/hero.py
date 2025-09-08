from imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from walls import *
    from poi import *
    from ghosts import *
    from map import *
    from actions import *

class Hero(Agent):
    """El héroe que hará acciones por el mapa para tratar
    de salvar a las 7 víctimas.
    """

    def __init__(self, model : "Map", id):
        """Constructor del héroe.

        Args:
            model (Map): El mapa del tablero.
        """
        super().__init__(model)

        # Atributos necesarios para ejecutar las acciones
        self.map = model
        self.neighbors = []
        self.action_points = 0
        self.stored_action_points = 0
        self.has_victim = False
        self.id = id

        # Json utilizado para mandar datos
        self.json = {}

    def update_position(self, x, y):
        """Modifica la posición del héroe

        Args:
            x (int): La coordenada en X.
            y (int): La coordenada en Y.
        """
        self.map.heroes.move_agent(self, (x, y))
        self.x = x
        self.y = y

    def step(self):
        """Realiza un turno."""

        from actions import ActionList

        # Verifica si aún puede jugar
        if self.map.game_over():
            return

        self.action_points = self.stored_action_points + 4 # Se actualizan sus puntos de acción

        self.json = { # Json que se va a mandar
            "num_steps": self.map.num_steps,
            "saved_victims": 0,
            "scared_victims": 0,
            "damaged_points": 0,
            "agents":[],
            "ghosts":[],
            "walls":[],
            "pois":[]
        }

        self.order = 0 # orden dentro del turno en que se realiza una accion

        # Realiza acciones hasta quedarse sin puntos
        while self.action_points > 0:
            # Verifica si se hace un movimiento naive, o con strat
            if self.map.naiveSimulation: # Simulación naive
                possible_actions = ActionList.generate_list(self)

                np.random.shuffle(possible_actions)

                # Realiza una acción aleatoria
                for action in possible_actions:
                    if action.do_action(): # Verifica que se haya completado
                        break
                    else: # Si no pudo hacerla, restaura los puntos de acción
                        action.restore_action_points()

            else: # TODO: Simulación con estrategia
                print("")

            # Independientemente de la simulación, verifica si reveló POI
            if self.map.poi.get(self.x, self.y) == 3:
                new_poi_value = self.map.poi.pick(self.x, self.y)

                poi = {
                    "x": self.x,
                    "y": self.y,
                    "old_status": 3,
                    "new_status": new_poi_value, # poi eliminado
                    "order": self.order
                }

                self.json["pois"].append(poi)

                if new_poi_value  == 4: # Si es una víctima real
                    if not self.has_victim: # En caso de que no lleve a nadie
                        self.hold_poi_on(self.x, self.y)

                else: # Si es una falsa alarma
                    self.map.poi.remove(self.x, self.y)

            elif self.map.poi.get(self.x, self.y) == 4 and not self.has_victim: # Que alguien más lo reveló pero no lo agarró
                self.hold_poi_on(self.x, self.y)

            self.order += 1
        
        self.old_matrix = copy.deepcopy(self.map.ghosts.dashboard)
        self.map.poi.added_pois = []
        self.map.poi.removed_pois = []

        # Después de los movimientos del héroe, finalizo el turno
        self.map.damage_points += self.map.ghosts.place_fog(self.json, self.order) # Coloca la niebla
        self.check_ghost_changes() # verifica cambios y agrega en json

        self.order += 1 # cambio de sub-turbo entre colocar fantasmas y pois

        for p in self.map.poi.removed_pois:
            poi = {
                "x": p[0][0],
                "y": p[0][1],
                "old_status": p[1],
                "new_status": 0, # poi eliminado
                "order": self.order
            }

            self.json["pois"].append(poi)
        
        self.order += 1 # entre pois removidos y pois agregados

        while self.map.poi.current < 3: # Coloca POIs si es que hay menos de 3
            self.map.poi.place(self.map.heroes)

        for p in self.map.poi.added_pois:
            poi = {
                "x": p[0][0],
                "y": p[0][1],
                "old_status": 3, # poi agregado
                "new_status": 3, # poi agregado
                "order": self.order
            }

            if p[1] > 0: # Antes había algo y se eliminó
                ghost = {
                    "x": p[0][0],
                    "y": p[0][1],
                    "status": 0, # no hay nada
                    "order": self.order
                }

                self.json["ghosts"].append(ghost)
        
            self.json["pois"].append(poi)

        self.order += 1

        for hero in self.map.heroes_array:
            if hero.map.ghosts.get_on(hero.x, hero.y): # Si se extendieron los fantasmas a mi casilla
                if hero.has_victim: # Si estaba con una víctima, se asusta
                    hero.map.poi.scared_victims += 1
                    hero.has_victim = False

                hero.to_closest_spawn_point() # Lo lleva al spawnpoint
                hero.stored_action_points = 0 # Se eliminan puntos de acción guardados
                agent = {
                    "x": hero.x,
                    "y": hero.y,
                    "id": hero.id,
                    "carrying": False,
                    "energy": hero.action_points,
                    "action": "Regresa a spawnpoit",
                    "order": self.order
                }

                self.json["agents"].append(agent)

        self.json["saved_victims"] = self.map.poi.rescued_victims
        self.json["scared_victims"] = self.map.poi.scared_victims
        self.json["damaged_points"] = self.map.damage_points

        return self.json

    def to_closest_spawn_point(self):
        """Mueve el héroe al spawn point más cercano."""

        closest_spawn_point = (0, 0, 1000)

        # Busca la distancia más corta entre los spawnpoints
        for spawn_point in self.map.spawn_points:
            distance = abs(spawn_point[0] - self.x) + abs(spawn_point[1] - self.y) # Obtiene la distancia manhattan

            if distance < closest_spawn_point[2]: # Verifica que sea más cercano
                closest_spawn_point = (spawn_point[0], spawn_point[1], distance)

        self.update_position(closest_spawn_point[0], closest_spawn_point[1])
    
    def check_ghost_changes(self):
        """
        """
        for y in range(len(self.old_matrix)):
            for x in range(len(self.old_matrix[y])):
                if self.old_matrix[y][x] != self.map.ghosts.dashboard[y][x]:
                    ghost = {
                        "x": x,
                        "y": y,
                        "status": self.map.ghosts.dashboard[y][x],
                        "order": self.order
                    }

                    self.json["ghosts"].append(ghost)

    def hold_poi_on(self, x, y):
        self.has_victim = True
        self.map.poi.willBeRescued(x, y) # Quito en el mapa la víctima

        poi = {
            "x": x,
            "y": y,
            "old_status": 4,
            "new_status": 0, # poi eliminado, se va a poner en el héroe
            "order": self.order
        }

        self.json["pois"].append(poi)