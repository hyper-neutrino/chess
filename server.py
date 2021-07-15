import engine, json, mind

from flask import Flask, render_template, request
from flask_cors import CORS

app = Flask("chess")
CORS(app)

@app.route("/")
def serve_root():
  return render_template("index.html")

@app.route("/get-state")
def get_state():
  return json.dumps(engine.create_game_state())

@app.route("/api", methods = ["POST"])
def api():
  state = request.json["state"]
  move = request.json["move"]
  team = request.json["team"]
  if move == 0:
    move = mind.move(state, list(engine.non_check_moves(state, team)))
  result = engine.make_move(state, move, team)
  moves = list(engine.non_check_moves(result, engine.opp(team)))
  win = (1 if engine.is_checked(result, engine.opp(team)) else -1) if moves == [] else 0
  return json.dumps({"result": result, "win": win, "move": engine.notate(state, move)})

if __name__ == "__main__":
  app.run(host = "0.0.0.0", port = 5729, debug = True)