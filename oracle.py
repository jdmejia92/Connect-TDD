from enum import Enum, auto

class ColumnClassification(Enum):
  FULL = auto()
  MAYBE = auto()

class ColumnRecommendation():
  def __init__(self, index, classification):
    self.index = index
    self.classification = classification

  # Dunders
  def __eq__(self, other):
    # If they're from different objects, they're different
    if not isinstance(other, self.__class__):
      return False
    # If they're from the same class, compare the properties of both
    else:
      return (self.index, self.classification) == (other.index, other.classification)
    
  def __hash__(self) -> int:
    return hash((self.index, self.classification))

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