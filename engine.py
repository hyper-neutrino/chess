from mind import move
from utils import *

class Engine:
  def create_board():
    backrow = list("RNBQKBNR")
    whiterow = [x + "W" for x in backrow]
    blackrow = [x + "B" for x in backrow]
    return [whiterow, ["PW"] * 8, *[[""] * 8 for _ in range(4)], ["PB"] * 8, blackrow]
  
  """
  The `engine` value should be truthy for engine white and falsy for engine black.
  """
  def __init__(self, engine):
    self.board = Engine.create_board()
    self.player = True
    self.engine = engine
    self.last_dpawn = None
    self.moved = [[False] * 8 for _ in range(8)]
  
  def is_valid_move(self, move):
    if not all(0 <= x < 8 for x in move):
      return False
    if move[0] == move[2] and move[1] == move[3]:
      return False
    if self.board[move[0]][move[1]] == "":
      return False
    piece, team = self.board[move[0]][move[1]]
    endp, endt = self.board[move[2]][move[3]] or "XN"
    if endt == team:
      return False
    if (team == "W") != self.player:
      return False
    # Pawn
    if piece == "P":
      # initial double-move for white; requires pawn move 2 ranks and no pieces in either position
      if team == "W" and move[0] == 1:
        if move[2] == 3 and move[3] == move[1] and self.board[2][move[1]] == self.board[3][move[1]] == "":
          return 1
      # initial double-move for black
      if team == "B" and move[0] == 6:
        if move[2] == 4 and move[3] == move[1] and self.board[5][move[1]] == self.board[4][move[1]] == "":
          return 1
      # normal move for white; requires pawn move 1 rank and no piece there
      if team == "W" and move[2] == move[0] + 1:
        if move[3] == move[1] and self.board[move[2]][move[3]] == "":
          if move[2] == 7 and (len(move) < 5 or not 0 <= move[4] < 4):
            return False
          return True
      # normal move for black
      if team == "B" and move[2] == move[0] - 1:
        if move[3] == move[1] and self.board[move[2]][move[3]] == "":
          if move[2] == 0 and (len(move) < 5 or not 0 <= move[4] < 4):
            return False
          return True
      # capture for white; requires pawn move 1 rank and 1 file either way and enemy piece there
      if team == "W" and move[2] == move[0] + 1 and abs(move[3] - move[1]) == 1:
        if endp == "X":
          if move[2] == 5 and self.last_dpawn == move[3]:
            return 2
        else:
          if move[2] == 7 and (len(move) < 5 or not 0 <= move[4] < 4):
            return False
          return True
      # capture for black
      if team == "B" and move[2] == move[0] - 1 and abs(move[3] - move[1]) == 1:
        if endp == "X":
          if move[2] == 2 and self.last_dpawn == move[3]:
            return 2
        else:
          if move[2] == 0 and (len(move) < 5 or not 0 <= move[4] < 4):
            return False
          return True
    # knight
    if piece == "N":
      # move 2|1 or 1|2
      if abs(move[2] - move[0]) == 2 and abs(move[3] - move[1]) == 1 or abs(move[2] - move[0]) == 1 and abs(move[3] - move[1]) == 2:
        return True
    # bishop
    if piece == "B" or piece == "Q":
      # needs diagonal
      if abs(move[2] - move[0]) == abs(move[3] - move[1]):
        # check no blockers
        r = sign(move[2] - move[0])
        f = sign(move[3] - move[1])
        for i in range(1, abs(move[2] - move[0])):
          if self.board[move[0] + i * r][move[1] + i * f]:
            return False
        return True
    # rook
    if piece == "R" or piece == "Q":
      # must be lattice
      if not (move[2] - move[0] and move[3] - move[1]):
        # check no blockers
        r = sign(move[2] - move[0])
        f = sign(move[3] - move[1])
        for i in range(1, abs(move[2] - move[0])):
          if self.board[move[0] + i * r][move[1] + i * f]:
            return False
        return True
    # king
    if piece == "K":
      if -1 <= move[2] - move[0] <= 1 >= move[3] - move[1] >= -1 and (move[2] - move[0] or move[3] - move[1]):
        return True
      rank = 0 if team == "W" else 7
      if not (self.moved[rank][4] or self.moved[rank][7]):
        if move[2] == rank and move[3] == 6 and self.board[rank][5] == self.board[rank][6] == "":
          return 3
      if not (self.moved[rank][4] or self.moved[rank][0]):
        if move[2] == rank and move[3] == 2 and self.board[rank][1] == self.board[rank][2] == self.board[rank][3] == "":
          return 4
    return False
  
  def in_check(self):
    for r in range(8):
      for f in range(8):
        if self.board[r][f] == "K" + "BW"[self.player]:
          x, y = r, f
    self.player = not self.player
    for r in range(8):
      for f in range(8):
        if self.is_valid_move((r, f, x, y)):
          self.player = not self.player
          print("!!", r, f, x, y)
          return True
    self.player = not self.player
    return False
  
  def clone(self):
    return [[piece for piece in row] for row in self.board]
  
  def advance(self, *inp):
    step = move(self.board) if self.player == self.engine else inp[0]
    valid = self.is_valid_move(step)
    rb = self.clone()
    self.board[step[2]][step[3]] = self.board[step[0]][step[1]]
    self.board[step[0]][step[1]] = ""
    check = self.in_check()
    self.board = rb
    print(valid, not check)
    if valid and not check:
      self.moved[step[0]][step[1]] = True
      self.board[step[2]][step[3]] = self.board[step[0]][step[1]]
      self.board[step[0]][step[1]] = ""
      if valid is 1:
        self.last_dpawn = step[1]
      else:
        if valid is 2:
          self.board[3 + self.player][self.last_dpawn] = ""
        elif valid is 3:
          self.moved[step[0]][7] = True
          self.board[step[0]][7] = ""
          self.board[step[0]][5] = "R" + "BW"[self.player]
        elif valid is 4:
          self.moved[step[0]][7] = True
          self.board[step[0]][0] = ""
          self.board[step[0]][3] = "R" + "BW"[self.player]
        self.last_dpawn = -1
      self.player = not self.player
      return True
    return False