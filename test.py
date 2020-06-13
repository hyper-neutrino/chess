from engine import *

state = create_game_state()

team = 1

while True:
  render(state)
  print()
  while True:
    move = tuple(map(int, input("[move for %s]: " % ["Black", "White"][team]).split()))
    value = make_move(state, move, "BW"[team])
    if value is False:
      print("Invalid Move!")
      print("Valid Moves:", *[notate(state, move) for move in non_check_moves(state, "BW"[team])])
    else:
      print(notate(state, move))
      state = value
      team = 1 - team
      break