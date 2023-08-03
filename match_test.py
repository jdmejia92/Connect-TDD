import pytest
from player import Player
from match import *

xavier = Player('Prof. Xavier')
otto = Player('Dr. Octopus')

def test_different_players_have_different_chars():
  t = Match(xavier, otto)

  assert xavier.char != otto.char

def test_no_player_with_none_char():
  t = Match(xavier, otto)
  assert xavier.char != None
  assert otto.char != None

def test_next_player_is_round_robbin():
  t = Match(otto, xavier)
  p1 = t.next_player
  p2 = t.next_player
  assert p1 != p2

def test_player_are_opponents():
  t = Match(otto, xavier)
  x = t.next_player
  o = t.next_player
  assert o.opponent == x
  assert x.opponent == o

