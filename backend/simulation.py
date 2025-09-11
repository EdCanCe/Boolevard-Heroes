from imports import *

dead = 0
rescued = 0
wins = 0
damage = 0

for i in range(1000):
    print(f"Starting simulation {i}...")
    simulation = Map(False)

    while not simulation.game_over():
        simulation.turn()

    print(f"Simulation {i} ended.")
    print(f"Rescued victims: {simulation.poi.rescued_victims}")
    print(f"Scared victims: {simulation.poi.scared_victims}")
    print(f"Damage points: {simulation.damage_points}")
    print(f"Game {'won' if simulation.win else 'lost'}\n")

    rescued += simulation.poi.rescued_victims
    dead += simulation.poi.scared_victims
    damage += simulation.damage_points
    if simulation.win:
        wins += 1

print(f"Total rescued victims: {rescued}")
print(f"Total dead victims: {dead}")
print(f"Total damage points: {damage}")
print(f"Total wins: {wins} out of 1000 ({wins/1000 * 100}%)")