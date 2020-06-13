import engine, json

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
  result = engine.make_move(state, move, team)
  return json.dumps(result)

if __name__ == "__main__":
  app.run(host = "0.0.0.0", port = 5729, debug = True)