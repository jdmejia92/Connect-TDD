class Match():
  
  def __init__(self, player1, player2) -> None:
    player1.char = 'x'
    player2.char = 'o'
    player1.opponent = player2

    self._players = {'x': player1, 'o': player2}
    self._round_robbin = [player1, player2]

  @property
  def next_player(self):
    next = self._round_robbin[0]
    self._round_robbin.reverse()
    return next
  
  def get_player(self, char):
    return self._players[char]
  
  def get_winner(self, board):
    """
    Return the winner and if there isn't one, return None
    """
    if board.is_victory('x'):
      return self.get_player('x')
    elif board.is_victory('o'):
      return self.get_player('o')
    else:
      return None