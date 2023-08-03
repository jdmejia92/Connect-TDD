from linear_board import LinearBoard
from list_util import transpose, displace_matrix, reverse_matrix
from settings import *

class SquareBoard():
  """
  Represent a square board make of multiple linear boards
  """

  @classmethod
  def fromList(cls, list_of_lists):
    """
    Transform a list of lists into a LinearBoard
    """
    # Exception for list of len > BOARD_LENGTH
    for i in range(BOARD_LENGTH - len(list_of_lists)): list_of_lists.append([])
    board = cls()
    board._columns = list(map(lambda element: LinearBoard.fromList(element), list_of_lists))
    return board

  # dunders
  def __init__(self):
    self._columns = [LinearBoard() for i in range(BOARD_LENGTH)]

  def __repr__(self) -> str:
    return f'{self.__class__}:{self._columns}'
  
  def __eq__(self, other) -> bool:
    if not isinstance(other, self.__class__):
      return False
    else:
      return (self._columns) == (other._columns)
    
  def __hash__(self) -> int:
    return hash((self._columns))
  
  def __len__(self):
    return len(self._columns)

  def is_full(self):
    """
    True is all the linear boards are full
    """
    result = True
    for lb in self._columns:
      result = result and lb.is_full()
    return result
  
  def as_matrix(self):
    """
    Return a representation in matrix form, a list of lists
    """
    return list(map(lambda x: x._column, self._columns))
  
  # Make a play in a column
  def add(self, play, column):
    self._columns[column].add(play)

  # Detecting victories
  def is_victory(self, play):
    return self._any_vertical_victory(play) or self._any_horizontal_victory(play) or self._any_rising_victory(play) or self._any_sinking_victory(play)
  
  def _any_vertical_victory(self, play):
    return any(lb.is_victory(play) for lb in self._columns)
  
  def _any_horizontal_victory(self, play):
    # Transpose _columns
    transpose_matrix = transpose(self.as_matrix())
    # Create a temp board with that matrix
    tmp = SquareBoard.fromList(transpose_matrix)
    # check the temp victory
    return tmp._any_vertical_victory(play)
  
  def _any_rising_victory(self, play):
    # Obtain the columns
    matrix = self.as_matrix()
    # inverted the columns
    r_matrix = reverse_matrix(matrix)
    # Create the temp board
    tmp = SquareBoard.fromList(r_matrix)
    # Return if it has a sinking victory
    return tmp._any_sinking_victory(play)
  
  def _any_sinking_victory(self, play):
    # Obtain the columns as a matrix
    matrix = self.as_matrix()
    # displace them
    displaced = displace_matrix(matrix)
    # created a temp board
    tmp = SquareBoard.fromList(displaced)
    # found out if there's a horizontal victory
    return tmp._any_horizontal_victory(play)
  