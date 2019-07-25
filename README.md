
Function: ali.knightsmove(positions, occupied_spaces=None)

Calculate the shortest path of a knight on a chess board between two points with chess notation input/output with space delimitation. Apply constraints by listing occupied positions on board. For example, to traverse opposite corners of the board (with no other pieces in the way):
	>>> ali.knightsmove('A1 H8')
	> 'B3 A5 C4 E5 G6 H8'
Note that in general there is no unique solution for this type of problem. Consequently, the output given will typically be one of several possible equivalent shortest distances.


Installation Instructions:

1) Import ali_test.py in Python 3. Ensure path directory consistent with default file path.
	>>> import chess

2) Specify start and stop position as first argument in chess algebraic notation, with space delimitation. For example, to start at position A1 and end at position B4 write:
	>>> chess.move('A1 B4')
  > 'C2 B4'

3) (Optional) Specify constraints on movement by listing any places on the board that are occupied and cannot be landed upon. List each occupied position separated by a space. Alternatively, the starting positions can be specified by listing 'start'. For example, if positions A1, A3, and C2 are occupied, the shortest distance between A1 and B4 can be calculated by: 
	>>> chess.move('A1 B4', 'A1 A3 C2')
	> 'B3 A5 C6 B4'
 Or to avoid any pieces on the start position of the board for black side pieces, list 'start':
	>>>chess.move('A1 H8')
  > 'B3 A5 B7 D6 F7 H8'
  >>> chess.move('A1 H8', 'start')
  > 'B3 A5 C4 E5 G6 H8  Warning: End point occupied by other piece.'

Dependencies:

Pandas, Numpy, Re
