import pytest

from game import Game
from square_board import SquareBoard

def test_creation():
  g = Game()
  assert g != None

def test_is_game_over():
  game = Game()
  win_x = SquareBoard.fromList([['x', 'o', None, None, None],
                                ['o', 'x', None, None, None],
                                ['x', 'o', 'x', 'o', None],
                                ['x', 'o', 'o', 'x', None],
                                [None, None, None, None, None]])
  
  win_o = SquareBoard.fromList([['x', 'o', 'x', 'o', None],
                                ['x', 'x', 'o', None, None],
                                ['o', 'o', None, None, None],
                                ['o', 'x', None, None, None],
                                [None, None, None, None, None]])
  
  tie = SquareBoard.fromList([['o', 'x', 'x', 'o', 'o'],
                              ['x', 'o', 'o', 'x', 'x'],
                              ['o', 'x', 'x', 'o', 'o'],
                              ['x', 'o', 'o', 'x', 'x'],
                              ['x', 'o', 'x', 'x', 'o']])
  
  unfinished = SquareBoard.fromList([['o', 'x', 'x', 'o', None],
                                    [None, None, None, None, None],
                                    [None, None, None, None, None],
                                    [None, None, None, None, None],
                                    [None, None, None, None, None]])
  
  game.board = win_x
  assert game._has_winner_or_tie() == True

  game.board = win_o
  assert game._has_winner_or_tie() == True

  game.board = tie
  assert game._has_winner_or_tie() == True

  game.board = unfinished
  assert game._has_winner_or_tie() == False