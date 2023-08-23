import pyfiglet
from enum import Enum, auto
from match import Match
from player import Player, HumanPlayer, ReportingPlayer
from square_board import SquareBoard
from list_util import reverse_matrix
from beautifultable import BeautifulTable
from settings import BOARD_LENGTH
from oracle import *


class RoundType(Enum):
  COMPUTER_VS_COMPUTER = auto()
  COMPUTER_VS_HUMAN = auto()

class DifficultyLevel(Enum):
  LOW = auto()
  MEDIUM = auto()
  HIGH = auto()


class Game:
  
  def __init__(self, round_type = RoundType.COMPUTER_VS_COMPUTER, match = Match(ReportingPlayer('Chip'), ReportingPlayer('Chop'))) -> None:
    # Store received values
    self.round_type = round_type
    self.match = match

    # empty board where to play
    self.board = SquareBoard()

  def start(self):
    # print the game's name or logo
    self.print_logo()

    # Set up the game
    self._configure_by_user()

    # run the main loop
    self._start_game_loop()
    
  def print_logo(self):
    logo = pyfiglet.Figlet(font='stop')
    print(logo.renderText('Connecta'))

  def _start_game_loop(self):
    # Infinity Loop
    while True:
      # Get the current player
      current_player = self.match.next_player
      # Make it play
      ask_help = current_player.play(self.board)
      # Check if the player asked for help
      while ask_help:
        # Display help
        self.display_help(ask_help)
        # Make the player play
        another_help = current_player.play(self.board)
        if type(another_help) != list:
          break
      # Show the play
      self.display_move(current_player)
      # Print the board
      self.display_board()
      # If the game has ended
      if self._is_game_over():
        # Show the final result
        self.display_result()
        # End the loop
        break

  def display_help(self, list_help):
    bt = BeautifulTable()
    bt.rows.append(list_help)
    bt.columns.header = [str(i) for i in range(BOARD_LENGTH)]
    print(bt)
  
  def display_move(self, player):
    print(f'\n{player.name} ({player.char}) has moved in column #{player.last_moves[0].position}\n')

  def display_board(self):
    """
    Print the board in its current status
    """
    # Get a matrix of char from the board
    matrix = self.board.as_matrix()
    matrix = reverse_matrix(matrix)

    # Create a board with beautifultable
    bt = BeautifulTable()
    for col in matrix:
      bt.columns.append(col)
    bt.columns.header = [str(i) for i in range(BOARD_LENGTH)]

    # Print
    print(bt)

  def display_result(self):
    winner = self.match.get_winner(self.board)
    if winner != None:
      print(f'\n{winner.name} ({winner.char}) wins!!!')
    else:
      print(f'\nA tie between {self.match.get_player("x").name} (x) and {self.match.get_player("o")} (o)')

  def _is_game_over(self):
    """
    The game is over when there's a winner or a tie
    """
    winner = self.match.get_winner(self.board)
    if winner != None:
      winner.on_win()
      winner.opponent.on_lose()
      return True # There's a winner
    elif self.board.is_full():
      # Tie
      return True
    else:
      return False

  def _configure_by_user(self):
    """
    Ask the player the values that he wants to type and difficulty of the game
    """
    # Define type of game (asking the user)
    self.round_type = self._get_round_type()

    # Ask the difficulty level
    if self.round_type == RoundType.COMPUTER_VS_HUMAN:
      self._difficulty_level = self._get_difficulty_level()

    # Create the game
    self.match = self._make_match()

  def _get_difficulty_level(self):
    """
    Ask the player how smart wanted his opponent to be
    """
    print("""
    Chose your opponent, human:
    
    1) Bender: for clowns and wimps
    2) T-800: you may regret it
    3) T-1000: Don't even think about it!
    """)
    while True:
      response = input('Please type 1, 2 or 3: ').strip()
      if response == '1':
        level = DifficultyLevel.LOW
        break
      elif response == '2':
        level = DifficultyLevel.MEDIUM
        break
      else:
        level = DifficultyLevel.HIGH
        break
    return level

  def _get_round_type(self):
    """
    Ask the user
    """
    print("""
    Select type of round:
          
          1) Computer vs Computer
          2) Computer vs Human
    """)
    response = ""
    while response != "1" and response != "2":
      response = input('Please type either 1 or 2: ')
    if response == "1":
      return RoundType.COMPUTER_VS_COMPUTER
    else:
      return RoundType.COMPUTER_VS_HUMAN
    
  def _make_match(self):
    """
    Player 1 always robot
    """
    _levels = {DifficultyLevel.LOW : BaseOracle(),
              DifficultyLevel.MEDIUM : SmartOracle(),
              DifficultyLevel.HIGH : LearningOracle()}
    
    if self.round_type == RoundType.COMPUTER_VS_COMPUTER:
      # Both players robotics
      player1 = ReportingPlayer('T-X', oracle=LearningOracle())
      player2 = ReportingPlayer('T-1000', oracle=LearningOracle())
    else:
      # Computer vs human
      player1 = ReportingPlayer('T-800', oracle=_levels[self._difficulty_level])
      player2 = HumanPlayer(name=input('Enter your name, puny human: '))

    return Match(player1, player2)