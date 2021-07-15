def create_game_state():
  return [
    [
      ["RW", "NW", "BW", "QW", "KW", "BW", "NW", "RW"],
      ["PW", "PW", "PW", "PW", "PW", "PW", "PW", "PW"],
      [""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  ],
      [""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  ],
      [""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  ],
      [""  , ""  , ""  , ""  , ""  , ""  , ""  , ""  ],
      ["PB", "PB", "PB", "PB", "PB", "PB", "PB", "PB"],
      ["RB", "NB", "BB", "QB", "KB", "BB", "NB", "RB"]
    ],
    [[True] * 8 for _ in range(8)],
    -1
  ]

def clone_board(board):
  return [[col for col in row] for row in board]

def clone_state(state):
  return [clone_board(state[0]), [[col for col in row] for row in state[1]], state[2]]

def sign(value):
  if value < 0:
    return -1
  if value > 0:
    return 1
  return 0

def team_of(piece):
  return piece[1] if piece else "N"

def opp(team):
  if team == "W":
    return "B"
  if team == "B":
    return "W"
  raise RuntimeError("Team must be B/W")

def render(state, move = (-1, -1, -1, -1)):
  for r in range(7, -1, -1):
    for f in range(9):
      if r == move[0] and f == move[1] or r == move[2] and f - 1 == move[3]:
        print(end = "<")
      elif r == move[2] and f == move[3] or r == move[0] and f - 1 == move[1]:
        print(end = ">")
      else:
        print(end = "|")
      if f == 8:
        print()
      else:
        team = team_of(state[0][r][f])
        if team == "N":
          print(end = " ")
        elif team == "W":
          print(end = "\033[7m\033[1m%s\033[0m" % state[0][r][f][0])
        else:
          print(end = state[0][r][f][0])