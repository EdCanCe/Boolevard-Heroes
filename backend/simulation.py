import requests

BASE_URL = "http://127.0.0.1:5000"  # Adjust if your Flask server runs elsewhere

total_minus_ones = 0

for sim in range(100):
    # Start a new simulation
    requests.get(f"{BASE_URL}/start/naive")
    print(f"Simulation {sim+1} started.")
    while True:
        resp = requests.get(f"{BASE_URL}/turn")
        if resp.status_code != 200:
            print("Simulation not started or error.")
            break
        data = resp.json()
        if not data:  # If the returned JSON is null or empty
            print(f"Simulation {sim+1} ended.")
            break
        # Count -1 in walls[].status
        minus_ones = sum(1 for wall in data.get("walls", []) if wall.get("status") == -1)
        total_minus_ones += minus_ones

print(f"Total times -1 appeared in walls[].status across 100 simulations: {total_minus_ones}")