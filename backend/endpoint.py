from imports import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from walls import *
    from poi import *
    from map import *
    from hero import *
    from actions import *

app = Flask(__name__)

turns = []

@app.route("/start/<mode>")
def start(mode):
    global simulation
    if mode == "naive":
        simulation = Map(True)
    else:
        simulation = Map(False)
    return "Simulation created"

@app.route("/turn")
def turn():
    if not isinstance(simulation, Map):
        return "Simulation not started", 400
    current = jsonify(simulation.turn())
    turns.append(current)
    return current

@app.route("/turn/<id>")
def selected_turn(id):
    if not isinstance(simulation, Map):
        return "Simulation not started", 400
    return turns[int(id)]

if __name__ == "__main__":
    app.run(debug=True)