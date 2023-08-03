import pytest

from game import Game

def test_creation():
  g = Game()
  assert g != None