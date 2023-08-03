from oracle import *

class Player():
  def __init__(self, name, char = None, opponent = None, oracle = BaseOracle()) -> None:
    self.name = name
    self.char = char
    self._oracle = oracle
    self.opponent = opponent

  def play(self, board):
    """
    Pick the best column from the recommended ones
    """
    # Ask the oracle
    (best, recommendations) = self._ask_oracle(board)

    # Play in the best
    self._play_on(board, best.index)

  def _play_on(self, board, position):
    # Play in the position
    board.add(self.char, position)

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
    # Select the best option in the recommendation list
    return valid[0]
  
class HumanPlayer(Player):
  def __init__(self, name, char):
    super().__init__(name, char)

  def _ask_oracle(self, board):
    """
    Ask the human that is the oracle
    """
    while True:
      # Ask column to the human
      raw = input('Select a column, puny human: ')
      # Verified the answer
      if _is_int(raw) and _is_within_column_range(board, int(raw)) and _is_non_full_column(board, int(raw)):

        # if is_valid, made the play and break the while
        pos = int(raw)
        return (ColumnRecommendation(pos, None), None)
  
def _is_within_column_range(board, num):
  return num >= 0 and num < len(board)

def _is_non_full_column(board, num):
  return not board._columns[num].is_full()

def _is_int(char):
  try:
    number = int(char)
    return True
  except:
    return False