"""
The chessboard will be given as an 8x8 array with A1 at [0][0] and A8 at [0][7]. Each element will be the empty string
to indicate a blank, or two characters indicating the piece (P = pawn, R = rook, N = knight, B = bishop, Q = queen,
K = king) and the team (W = white, B = black).

Your function `move(str[][] board): (int, int, int, int, [int])` must return a tuple `(w, x, y, z, [p])` representing a
move of the piece on `(w, x)` to `(y, z)`. If this move is invalid you will immediately lose. If a pawn reaches the end
rank, p represents the promotion: 0 for knight, 1 for bishop, 2 for rook, 3 for queen. This value is only checked on
promotion; it can be omitted in other cases.
"""

def move(board):
  for row in board:
    print("-" * 25)
    print("|".join(["", *[x or "  " for x in row], ""]))
  print("-" * 25)
  return tuple(map(int, input("[engine move]: ").split()))