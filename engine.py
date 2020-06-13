from mind import move
from utils import *

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

def clone_state(state):
  return [[[col for col in row] for row in state[0]], [[col for col in row] for row in state[1]], state[2]]

def commit(state, *move):
  team = team_of(state[0][move[0]][move[1]])
  if len(move) == 4:
    w, x, y, z = move
  elif len(move) == 5:
    w, x, y, z, p = move
  if state[0][w][x][0] == "P":
    if x == z and abs(w - y) == 2:
      state[2] = x
    else:
      state[2] = -1
      if state[0][y][z] == "" and x != z:
        state[0][w][z] = ""
  state[0][y][z] = state[0][w][x]
  state[0][w][x] = ""
  state[1][w][x] = state[1][y][z] = False
  if len(move) == 5:
    if 0 <= p < 4 and state[0][y][z][0] == "P" and y in [0, 7]:
      state[0][y][z] = "NBRQ"[p] + state[0][y][z][1]
    elif p == 4:
      state[0][w][0] = ""
      state[0][w][2] = "R" + team
      state[1][w][0] = False
    elif p == 5:
      state[0][w][7] = ""
      state[0][w][5] = "R" + team
      state[1][w][7] = False

def make_move(state, move, team):
  move = tuple(move)
  print(move, team, state[2])
  render(state)
  clone = clone_state(state)
  if move in non_check_moves(clone, team):
    print("move made:", notate(clone, move))
    commit(clone, *move)
    return clone
  print("invalid move; valid moves are:", *[notate(clone, m) for m in non_check_moves(clone, team)])
  return False

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

def notate(state, move):
  if state[0][move[0]][move[1]] == "":
    return ""
  piece, team = state[0][move[0]][move[1]]
  valid_moves = categorized_moves(state, team)
  departures = []
  for valid in valid_moves[piece]:
    if valid[2] == move[2] and valid[3] == move[3]:
      departures.append((valid[0], valid[1]))
  notation = ""
  if len(departures) == 0:
    return ""
  elif len(move) >= 5 and move[4] >= 4:
    if move[4] == 4:
      notation = "O-O-O"
    elif move[4] == 5:
      notation = "O-O"
    else:
      return ""
  elif len(departures) == 1:
    if piece == "P" and team_of(state[0][move[2]][move[3]]) != "N":
      disambiguator = "abcdefgh"[move[1]]
    else:
      disambiguator = ""
  else:
    if len({x[1] for x in departures}) == len(departures):
      disambiguator = "abcdefgh"[move[1]]
    elif len({x[0] for x in departures}) == len(departures):
      disambiguator = str(move[0] + 1)
    else:
      disambiguator = "abcdefgh"[move[1]] + str(move[0] + 1)
  clone = clone_state(state)
  commit(clone, *move)
  promo = "NBRQ"[move[4]] if len(move) >= 5 and 0 <= move[4] < 4 else ""
  return (notation or ("" if piece == "P" else piece) + disambiguator + ("x" if state[0][move[2]][move[3]] else "") + "abcdefgh"[move[3]] + str(move[2] + 1) + promo) + ("#" if is_checkmated(clone, opp(team)) else "+" if is_checked(clone, opp(team)) else "")

def categorized_moves(state, team):
  categories = {x: [] for x in "PNBRQK"}
  for move in list_moves(state, team):
    categories[state[0][move[0]][move[1]][0]].append(move)
  return categories

def list_moves(state, team):
  forward = 1 if team == "W" else -1
  for r in range(8):
    for f in range(8):
      if team_of(state[0][r][f]) == team:
        p = state[0][r][f][0]
        # Pawn
        if p == "P":
          if not 0 <= r + forward < 8: continue
          # Double Move
          if state[1][r][f]:
            if state[0][r + forward][f] == state[0][r + forward * 2][f] == "":
              yield (r, f, r + forward * 2, f)
          # Standard Move
          if state[0][r + forward][f] == "":
            # To End Rank / Promotion
            if r + forward in [0, 7]:
              for promo in range(4):
                yield (r, f, r + forward, f, promo)
            # Normal Move
            else:
              yield (r, f, r + forward, f)
          # Captures
          for fd in [-1, 1]:
            if 0 <= f + fd < 8:
              # Normal Capture
              if team_of(state[0][r + forward][f + fd]) == opp(team):
                if r + forward in [0, 7]:
                  for promo in range(4):
                    yield (r, f, r + forward, f + fd, promo)
                else:
                  yield (r, f, r + forward, f + fd)
              # E.P.
              if team_of(state[0][r][f + fd]) == opp(team) and state[0][r][f + fd][0] == "P" and state[2] == f + fd:
                yield (r, f, r + forward, f + fd)
        # Knight
        elif p == "N":
          # Standard Move
          for dr, df in [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]:
            if 0 <= r + dr < 8 > f + df >= 0 and team_of(state[0][r + dr][f + df]) != team:
              yield (r, f, r + dr, f + df)
        # King
        elif p == "K":
          # Standard Move
          for dr in range(-1, 2):
            for df in range(-1, 2):
              if dr == df == 0:
                continue
              if 0 <= r + dr < 8 > f + df >= 0 and team_of(state[0][r + dr][f + df]) != team:
                yield (r, f, r + dr, f + df)
          # O-O-O
          if state[1][r][f] and state[1][r][0] and state[0][r][1] == state[0][r][2] == state[0][r][3] == "":
            yield (r, f, r, 2, 4)
          # O-O
          if state[1][r][f] and state[1][r][7] and state[0][r][5] == state[0][r][6] == "":
            yield (r, f, r, 6, 5)
        # Bishop, Rook, Queen
        else:
          dir_list = []
          # Bishop / Queen
          if p == "B" or p == "Q":
            # Add Diagonals
            dir_list.extend([(1, 1), (-1, 1), (1, -1), (-1, -1)])
          # Rook / Queen
          if p == "R" or p == "Q":
            # Add V/H
            dir_list.extend([(1, 0), (-1, 0), (0, 1), (0, -1)])
          for dr, df in dir_list:
            for i in range(1, 8):
              if not 0 <= r + dr * i < 8 > f + df * i >= 0:
                break
              if team_of(state[0][r + dr * i][f + df * i]) == team:
                break
              yield (r, f, r + dr * i, f + df * i)
              if team_of(state[0][r + dr * i][f + df * i]) == opp(team):
                break

def non_check_moves(state, team):
  for move in list_moves(state, team):
    if len(move) >= 5:
      if move[4] == 4:
        if is_checked(state, team):
          continue
        clone = clone_state(state)
        for sub in [(move[0], 4, move[0], 3), (move[0], 3, move[0], 2), (move[0], 0, move[0], 3)]:
          commit(clone, *sub)
          if is_checked(clone, team):
            break
        else:
          yield move
        continue
      elif move[4] == 5:
        if is_checked(state, team):
          continue
        clone = clone_state(state)
        for sub in [(move[0], 4, move[0], 5), (move[0], 5, move[0], 6), (move[0], 7, move[0], 5)]:
          commit(clone, *sub)
          if is_checked(clone, team):
            break
        else:
          yield move
        continue
    clone = clone_state(state)
    commit(clone, *move)
    if not is_checked(clone, team):
      yield move

def is_checked(state, team):
  for move in list_moves(state, opp(team)):
    if state[0][move[2]][move[3]] == "K" + team:
      return True
  return False

def is_checkmated(state, team):
  if not is_checked(state, team):
    return False
  return len(list(non_check_moves(state, team))) == 0