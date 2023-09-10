from oracle import *
from square_board import SquareBoard
from player import Player
from settings import BOARD_LENGTH


def test_base_oracle():
  board = SquareBoard.fromList([[None, None, None, None, None],
                                ['x', 'o', 'x', 'o', 'o'],
                                ['o', 'o', 'x', 'x', 'x'],
                                ['o', None, None, None, None],
                                ['x', 'o', None, None, None]])
  
  expected = [ColumnRecommendation(0, ColumnClassification.MAYBE),
              ColumnRecommendation(1, ColumnClassification.FULL),
              ColumnRecommendation(2, ColumnClassification.FULL),
              ColumnRecommendation(3, ColumnClassification.MAYBE),
              ColumnRecommendation(4, ColumnClassification.MAYBE)]
  
  rappel = BaseOracle()

  assert len(rappel.get_recommendation(board, None)) == len(expected)
  assert rappel.get_recommendation(board, None) == expected

def test_equality():
  cr = ColumnRecommendation(2, ColumnClassification.MAYBE)

  assert cr == cr # they're the same
  assert cr == ColumnRecommendation(2, ColumnClassification.MAYBE) # they're equivalent

  # they're not equivalent (because the classification is different)
  assert cr != ColumnRecommendation(2, ColumnClassification.FULL)
  assert cr != ColumnRecommendation(3, ColumnClassification.FULL)

def test_same_hash():
  c_hash = ColumnRecommendation(2, ColumnClassification.MAYBE)

  assert hash(c_hash) == hash(c_hash)
  assert hash(c_hash) != hash(ColumnRecommendation(1, ColumnClassification.MAYBE))
  assert hash(c_hash) != hash(ColumnRecommendation(2, ColumnClassification.FULL))
  assert hash(c_hash) != hash(ColumnRecommendation(3, ColumnClassification.FULL))

def test_is_winning_move():
  winner = Player('Xavier', 'x')
  loser = Player('Otto', 'o')

  empty = SquareBoard()
  almost = SquareBoard.fromList([['o', 'x', 'o', None, None], 
                                ['o', 'x', 'o', None, None],
                                ['x', None, None, None, None],
                                ['o', 'x', None, None, None],
                                [None, None, None, None, None]])
  
  oracle = SmartOracle()

  # About the empty board
  for i in range(0, BOARD_LENGTH):
    assert oracle._is_winning_move(empty, i, winner) == False
    assert oracle._is_winning_move(empty, i, loser) == False

  # About the almost board
  for i in range(0, BOARD_LENGTH):
    assert oracle._is_winning_move(almost, i, loser) == False
  
  assert oracle._is_winning_move(almost, 2, winner)

def test_no_good_options():
  x = Player('xavier', char='x')
  o = Player('Otto', char='o', opponent=x)

  oracle = SmartOracle()

  maybe = SquareBoard.fromBoardCode('.....|o....|.....|.....|.....')
  bad_and_full = SquareBoard.fromBoardCode('xx...|ooo..|o....|xoxox|xoxxo')
  all_bad = SquareBoard.fromBoardCode('xxo..|ooo..|oox..|oxx..|.....')

  assert oracle.no_good_options(maybe, x) == False
  assert oracle.no_good_options(bad_and_full, x)
  assert oracle.no_good_options(all_bad, x)