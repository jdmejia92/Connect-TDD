from oracle import *
from square_board import SquareBoard

def test_base_oracle():
  board = SquareBoard.fromList([[None, None, None, None],
                                ['x', 'o', 'x', 'o'],
                                ['o', 'o', 'x', 'x'],
                                ['o', None, None, None]])
  
  expected = [ColumnRecommendation(0, ColumnClassification.MAYBE),
              ColumnRecommendation(1, ColumnClassification.FULL),
              ColumnRecommendation(2, ColumnClassification.FULL),
              ColumnRecommendation(3, ColumnClassification.MAYBE)]
  
  rappel = BaseOracle()

  assert len(rappel.get_recommendation(board, None)) == len(expected)
  assert rappel.get_recommendation(board, None) == expected

def test_equality():
  cr = ColumnRecommendation(2, ColumnClassification.MAYBE)

  assert cr == cr # they're the same
  assert cr == ColumnRecommendation(2, ColumnClassification.MAYBE) # they're equivalent

  # they're not equivalent
  assert cr != ColumnRecommendation(1, ColumnClassification.MAYBE)
  assert cr != ColumnRecommendation(2, ColumnClassification.FULL)
  assert cr != ColumnRecommendation(3, ColumnClassification.FULL)

def test_same_hash():
  c_hash = ColumnRecommendation(2, ColumnClassification.MAYBE)

  assert hash(c_hash) == hash(c_hash)
  assert hash(c_hash) != hash(ColumnRecommendation(1, ColumnClassification.MAYBE))
  assert hash(c_hash) != hash(ColumnRecommendation(2, ColumnClassification.FULL))
  assert hash(c_hash) != hash(ColumnRecommendation(3, ColumnClassification.FULL))