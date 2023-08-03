import pytest
from list_util import *

def test_find_one():
    needle = 1
    none = [0, 0, 5, 's']
    beginning = [1, None, 9, 6, 0, 0]
    end = ['X', '0', 1]
    several = [0, 0, 3, 4, 1, 3, 2, 1, 3, 4]

    assert find_one(none, needle) == False
    assert find_one(beginning, needle)
    assert find_one(end, needle)
    assert find_one(several, needle)

def test_find_n():
  assert find_n([2, 3, 4, 5, 6], 2, -1) == False
  assert find_n([1, 2, 3, 4, 5], 42, 2) == False
  assert find_n([1, 2, 3, 4, 5], 1, 2) == False
  assert find_n([1, 2, 3, 2, 4, 5], 2, 2)
  assert find_n([1, 2, 3, 4, 5, 4, 6, 4, 7, 4, 6], 4, 2)
  assert find_n([1, 2, 3, 4], 'x', 0)

def test_find_streak():
  assert find_streak([1, 2, 3, 4, 5], 4, -1) == False
  assert find_streak([1, 2, 3, 4, 5], 42, 2) == False
  assert find_streak([1, 2, 3, 4], 4, 1)
  assert find_streak([1, 2, 3, 1, 2], 2, 2) == False
  assert find_streak([1, 2, 3, 4, 5, 5, 5], 5, 3)
  assert find_streak([5, 5, 5, 1, 2, 3, 4], 5, 3)
  assert find_streak([1, 2, 5, 5, 5, 3, 4], 5, 3)
  assert find_streak([1, 2, 3, 4, 5, 5, 5], 5, 4) == False

def test_first_elements():
  original = [[0,7,3], [4,0,1]]
  empty_list_of_lists = [[], []]
  middle_empty_list = [[0,7,3], [None,], [], [4,0,1]]

  assert first_elements(original) == [0, 4]
  assert first_elements(empty_list_of_lists) == [None, None]
  assert first_elements(middle_empty_list) == [0, None, None, 4]

def test_nth_elements():
  original = [[0,7,3], [4,0,1]]
  empty_list_of_lists = [[], []]
  middle_empty_list = [[0,7,3], [None,], [], [4,0,1]]

  assert nth_elements(original, 0) == [0, 4]
  assert nth_elements(middle_empty_list, 0) == [0, None, None, 4]
  assert nth_elements(empty_list_of_lists, 2) == [None, None]
  

def test_transpose():
  original = [[0,7,3], [4,0,1]]
  transposed = [[0,4], [7,0], [3,1]]
  error = [[2,0], [3,1,5]]

  assert transpose(original) == transposed
  assert transpose(transpose(original)) == original
  with pytest.raises(ValueError):
    transpose(error)

def test_zero_distance_displace():
  l1 = [1, 2, 3, 4, 5, 6]
  l2 = [1]
  l3 = [[4, 5], ['x', 'o', 'c']]

  assert displace([], 0) == []
  assert displace(l1, 0) == l1
  assert displace(l2, 0) == l2
  assert displace(l3, 0) == l3

def test_positive_distance_displace():

  l1 = [1, 2, 3, 4, 5, 6]
  l2 = [1]
  l3 = [[4, 5], ['x', 'o', 'c']]
  l4 = [9, 6, 5]

  assert displace([], 2) == []
  assert displace(l1, 2) == [None, None, 1, 2, 3, 4]
  assert displace(l2, 3, '-') == ['-']
  assert displace(l3, 1, '#') == ['#', [4, 5]]
  assert displace(l4, 3, 0) == [0, 0, 0]

def test_negative_distance_displace():
  l1 = [1, 2, 3, 4, 5, 6]
  l2 = [1]
  l3 = [[4, 5], ['x', 'o', 'c']]
  l4 = [9, 6, 5]

  assert displace([], -2) == []
  assert displace(l1, -2) == [3, 4, 5, 6, None, None]
  assert displace(l2, -3, '-') == ['-']
  assert displace(l3, -1, '#') == [['x', 'o', 'c'], '#']
  assert displace(l4, -3, 0) == [0, 0, 0]

def test_reverse_list():
  assert reverse_list([]) == []
  assert reverse_list([1,2,3,4,5,6]) == [6,5,4,3,2,1]

def test_reverse_matrix():
  assert reverse_matrix([]) == []
  assert reverse_matrix([[0,1,2,3], [0,1,2,3]]) == [[3,2,1,0], [3,2,1,0]]