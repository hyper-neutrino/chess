from engine import *

e = Engine(True)

while True:
  while not e.advance(): pass
  print("-" * 23)
  for row in e.board:
    print(*[x or "  " for x in row])
  print("-" * 23)
  while not e.advance(tuple(map(int, input().split()))): pass