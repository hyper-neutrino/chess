from utils import *

"""
The chessboard will be given as a list of three values.

The first is an 8x8 array with A1 at [0][0] and A8 at [0][7]. Each element will be the empty string
to indicate a blank, or two characters indicating the piece (P = pawn, R = rook, N = knight, B = bishop, Q = queen,
K = king) and the team (W = white, B = black).

The second is an 8x8 array in the same format. Each element is true if the square has not been touched and false otherwise (just used for castling
and pawn double-moves).

The third is an integer. If the last move had a pawn make a double-move, it is the file of that pawn. Otherwise, it is -1 (used for en passant).

The second parameter is a list of moves in the return format. If it is empty, you have lost, but this should never happen in theory.

Your function `move([str[][] board, bool[][] original, int dfile], move[] moves): (int, int, int, int, [int])` must return a tuple `(w, x, y, z, [p])` representing a
move of the piece on `(w, x)` to `(y, z)`. If this move is invalid you will immediately lose. If a pawn reaches the end
rank, p represents the promotion: 0 for knight, 1 for bishop, 2 for rook, 3 for queen. This value is only checked on
promotion; it can be omitted in other cases. Finally, p should equal 4 for queen-side castle and 5 for king-side castle.
"""

import random

def move(state, moves):
  return random.choice(moves)
  return tuple(map(int, input("[engine move]: ").split()))