from typing import Any
from settings import BOARD_LENGTH, VICTORY_STRIKE
from list_util import find_streak

class LinearBoard():
  """
  Class that represent a board of just one column
  x:: one player
  o:: another player
  None:: an empty space
  """

  @classmethod
  def fromList(cls, list):
    # Exception for len of list
    for i in range(BOARD_LENGTH - len(list)): list.append(None)
    board = cls()
    board._column = list
    return board

  def __init__(self):
    """
    A list of None
    """
    self._column = [None for i in range(BOARD_LENGTH)]
  
  def __eq__(self, other) -> bool:
    if not isinstance(other, self.__class__):
      return False
    else:
      return (self._column) == (other._column)
    
  def __hash__(self) -> int:
    return hash((self._columns))
  
  def add(self, play):
    """
    Plays in the first position available
    """
    # Adding if there is an available place
    if not self.is_full():
      # We search for the first position available (None)
      i = self._column.index(None)
      # Change it for the play
      self._column[i] = play
  
  def is_full(self):
    return self._column[-1] != None
  
  def is_victory(self, player):
    return find_streak(self._column, player, VICTORY_STRIKE)

  def is_tie(self, player1, player2):
    """
    Evaluate there's not victory of player1 or player 2
    """
    return (self.is_victory(player1) == False) and (self.is_victory(player2) == False)