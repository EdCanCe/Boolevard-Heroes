from abc import ABC, abstractmethod

class Actions(ABC):
    self.x = 0
    self.y = 0

    def __init__(self, hero, x, y):
        """Se inicializa la acción.

        Args:
            hero (Hero): El héroe que se moverá
            x (_type_): _description_
            y (_type_): _description_
        """
        self.x = x
        self.y = y

    @abstractmethod
    def is_possible(self):
        """Método abstracto para verificar que sea
        posible realizar ésta acción.
        """
        pass

    

class Move(Actions):
