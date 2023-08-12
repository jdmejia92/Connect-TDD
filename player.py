from oracle import *
import random
from list_util import *

class Player():
  def __init__(self, name, char = None, opponent = None, oracle = BaseOracle()) -> None:
    self.name = name
    self.char = char
    self._oracle = oracle
    self.opponent = opponent
    self.last_move = None

  @property
  def opponent(self):
    return self._opponent

  @opponent.setter
  def opponent(self, other):
    if other != None:
      self._opponent = other
      other._opponent = self

  def play(self, board):
    """
    Pick the best column from the recommended ones
    """
    # Ask the oracle
    (best, recommendations) = self._ask_oracle(board)
    if best == "h":
      return recommendations
    else:
      # Play in the best
      self._play_on(board, best.index)

  def _play_on(self, board, position):
    # Play in the position
    board.add(self.char, position)
    # Store the last move
    self.last_move = position

  def _ask_oracle(self, board):
    """
    Ask the oracle and return the best option
    """
    # Get the recommendations
    recommendations = self._oracle.get_recommendation(board, self)
    # Select the best
    best = self._choose(recommendations)

    return (best, recommendations)

  def _choose(self, recommendations):
    # We remove the additional
    valid = list(filter(lambda x : x.classification != ColumnClassification.FULL, recommendations))
    # Order by the value of classification
    valid = sorted(valid, key=lambda x : x.classification.value, reverse=True)
    # If all the choices are the same, pick one random
    if all_same(valid):
      return random.choice(valid)

    else:
    # If there're different, select the more valuable (which is going to be the first)
      return valid[0]
    
  def _get_help(self, board, oracle):
    """
    Return help for the player
    """
    return oracle.get_recommendation(board, self)
  
class HumanPlayer(Player):
  def __init__(self, name, char=None):
    super().__init__(name, char)

  def _ask_oracle(self, board):
    """
    Ask the human that is the oracle
    """
    while True:
      # Ask column to the human
      raw = input('Select a column, puny human (or h for help): ')
      # Verified the answer
      if _is_int(raw) and _is_within_column_range(board, int(raw)) and _is_non_full_column(board, int(raw)):
        # if is_valid, made the play and break the while
        pos = int(raw)
        return (ColumnRecommendation(pos, None), None)
      elif raw == 'h':
        return ('h', self._get_help(board, SmartOracle()))

def _is_within_column_range(board, num):
  return num >= 0 and num < len(board)

def _is_non_full_column(board, num):
  return not board._columns[num].is_full()

def _is_int(char):
  try:
    int(char)
    return True
  except:
    return False