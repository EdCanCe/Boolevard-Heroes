from walls import *
from poi import *
from ghosts import *
from map import *
from hero import *
from actions import *

rescued = 0

for i in range(100):

    simulation = Map(True)

    while not simulation.game_over():
        json = simulation.turn()

    print(f"Simulación no: {i}")

    print(f"Se rescataron {simulation.poi.rescued_victims} víctimas")

    print(f"Se asustaron {simulation.poi.scared_victims} víctimas")

    print(f"La casa tuvo {simulation.damage_points} puntos de daño")
    
    print(" ")

    print(f"La partida se {'ganó' if simulation.win else 'perdió'}")

    rescued += simulation.poi.rescued_victims

    

print(f"Se rescataron en total {rescued}")