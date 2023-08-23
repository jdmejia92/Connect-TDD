from enum import Enum
from copy import deepcopy
from settings import BOARD_LENGTH
from square_board import SquareBoard

class ColumnClassification(Enum):
  def __str__(self) -> str:
    return self.name.lower()  

  FULL = -1 # Impossible
  BAD = 1 # Very undesirable
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
  
  def no_good_options(self, board, player):
    """
    Detect that all classifications are BAD or FULL
    """
    # Get all the classifications
    columnRecommendation = self.get_recommendation(board, player)
    # Check all the classifications are the correct type
    result = True
    for rec in columnRecommendation:
      if (rec.classification == ColumnClassification.WIN) or (rec.classification == ColumnClassification.MAYBE):
        result = False
        break
    return result
  
  # methods that are to be rewrite in the other classes
  def update_to_bad(self, move):
    pass

  def backtrack(self, list_of_moves):
    pass


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
        recommendation.classification = ColumnClassification.BAD
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
  

class MemoizingOracle(SmartOracle):
  """
  The method get_recommendation it's now memorize
  """
  def __init__(self) -> None:
    super().__init__()
    self._past_recommendations = {}

  def _make_key(self, board_code, player):
    """
    The key must merge the board an player, in the most simple way
    """
    return f'{board_code.raw_code}@{player.char}'

  def get_recommendation(self, board, player):
    # Create the key
    key = self._make_key(board.as_code(), player)

    # Look the cache: if there is not, make the calculation and save
    if key not in self._past_recommendations:
      self._past_recommendations[key] = super().get_recommendation(board, player)

    # Return what is save in cache
    return self._past_recommendations[key]
  
class LearningOracle(MemoizingOracle):
  
  def update_to_bad(self, move):
    # Create key
    key = self._make_key(move.board_code, move.player)
    # Get the wrong classification
    recommendation = self.get_recommendation(SquareBoard.fromBoardCode(move.board_code), move.player)
    # Correct it
    recommendation[move.position] = ColumnRecommendation(move.position, ColumnClassification.BAD)
    # Replace it
    self._past_recommendations[key] = recommendation

  def backtrack(self, list_of_moves):
    """
    Review all the plays and if it find one where everything was lost
    it means that the last move has to be update to BAD
    """
    # The moves are backwards (the first one is the last one)
    print('learning...')
    # For each move
    for move in list_of_moves:
      # Change it to BAD
      self.update_to_bad(move)
      
      # Check if everything was loss after the classification
      board = SquareBoard.fromBoardCode(move.board_code)
      if not self.no_good_options(board, move.player):
        # If not all was lost, break, if not, keep going
        break

    print(f'Size of knowledgebase: {len(self._past_recommendations)}')