from square_board import SquareBoard
from oracle import BaseOracle, SmartOracle, ColumnClassification, ColumnRecommendation
from player import _is_within_column_range, Player, _is_non_full_column, _is_int, HumanPlayer
from match import Match

def test_valid_column():
  board = SquareBoard.fromList([['x', None, None, None, None],
                                ['x', 'o', 'x', 'o', 'x'],
                                ['o', 'o', 'x', 'x', 'o'],
                                ['o', None, None, None, None],
                                ['x', 'x', None, None, None]])

  assert _is_within_column_range(board, 0)  
  assert _is_within_column_range(board, 1)
  assert _is_within_column_range(board, 2)
  assert _is_within_column_range(board, 3)
  assert _is_within_column_range(board, 4)
  assert _is_within_column_range(board, 5) == False
  assert _is_within_column_range(board, -10) == False
  assert _is_within_column_range(board, 10) == False


def test_is_non_full_column():
  board = SquareBoard.fromList([['x', None, None, None, None],
                                ['x', 'o', 'x', 'o', 'x'],
                                ['o', 'o', 'x', 'x', 'o'],
                                ['o', None, None, None, None],
                                [None, None, None, None, None]])
  
  assert _is_non_full_column(board, 0)
  assert _is_non_full_column(board, 1) == False
  assert _is_non_full_column(board, 2) == False
  assert _is_non_full_column(board, 3)

def test_is_int():
  assert _is_int('42')
  assert _is_int('0')
  assert _is_int('-32')
  assert _is_int('  32  ')
  assert _is_int('hola') == False
  assert _is_int('') == False
  assert _is_int('3.14') == False
