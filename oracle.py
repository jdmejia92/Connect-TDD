from enum import Enum, auto
from copy import deepcopy
from settings import BOARD_LENGTH

class ColumnClassification(Enum):
  def __str__(self) -> str:
    return self.name.lower()  

  FULL = -1 # Impossible
  LOSE = 1 # Very undesirable
  MAYBE = 10 # Undesirable
  WIN = 100 # The best choice: It win for a mile

class ColumnRecommendation():
  def __init__(self, index, classification):
    self.index = index
    self.classification = classification

  # Dunders
  def __eq__(self, other):
    # If they're from different objects, they're different
    if not isinstance(other, self.__class__):
      return False
    # Only matters the classification
    else:
      return self.classification == other.classification
    
  def __hash__(self) -> int:
    return hash((self.index, self.classification))
  
  def __repr__(self) -> str:
    return f'{self.classification}'

class BaseOracle():

  def get_recommendation(self, board, player):
    """
    Return a list of ColumnRecommendations
    """
    return list(map(lambda i : self._get_column_recommendation(board, i, player), range(len(board))))
  
  def _get_column_recommendation(self, board, index, player):
    """
    Classifies a column as either FULL or MAYBE and returns a ColumnRecommendation
    """
    classification = ColumnClassification.MAYBE
    if board._columns[index].is_full():
      classification = ColumnClassification.FULL
    return ColumnRecommendation(index, classification)
  
class SmartOracle(BaseOracle):
  def _get_column_recommendation(self, board, index, player):
    """
    Tune the classification of super and try to find win columns
    """
    recommendation = super()._get_column_recommendation(board, index, player)
    if recommendation.classification == ColumnClassification.MAYBE:
      # It can be improve
      if self._is_winning_move(board, index, player):
        recommendation.classification = ColumnClassification.WIN
      elif self._is_losing_move(board, index, player):
        recommendation.classification = ColumnClassification.LOSE
    return recommendation
  
  def _is_losing_move(self, board, index, player):
    """
    If player make a move in index, it will generate a winning move to the player in any other column?
    """
    tmp = self._play_on_tmp_board(board, index, player)

    will_lose = False
    for i in range(0, BOARD_LENGTH):
      if self._is_winning_move(tmp, i, player.opponent):
        will_lose = True
        break
    return will_lose

  
  def _is_winning_move(self, board, index, player):
    """
    Determinate if playing in a position, give a immediate victory
    """
    # Make a copy of the board
    # Play on it
    tmp = self._play_on_tmp_board(board, index, player)

    # Determinate if there's a player victory or not
    return tmp.is_victory(player.char)
  
  def _play_on_tmp_board(self, board, index, player):
    """
    Make a copy of the board and play on it
    """
    tmp = deepcopy(board)

    tmp.add(player.char, index)

    # Return the modifies copy
    return tmp