from imports import *

dead = 0
rescued = 0
wins = 0
damage = 0
max_person = 0

for i in range(1000):
    simulation = Map(False)

    while not simulation.game_over():
        simulation.turn()

    rescued += simulation.poi.rescued_victims
    dead += simulation.poi.scared_victims
    damage += simulation.damage_points
    if simulation.win:
        wins += 1

    if simulation.poi.rescued_victims > max_person:
        max_person = simulation.poi.rescued_victims

print(f"Total rescued victims: {rescued}")
print(f"Max rescued victims: {max_person}")
print(f"Total dead victims: {dead}")
print(f"Total damage points: {damage}")
print(f"Total wins: {wins} out of 1000 ({wins/1000 * 100}%)")