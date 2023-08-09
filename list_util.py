def find_one(list_to_search, needle):
  """
  Return True if one needle's occurrence is found in list_to_search
  """
  return find_n(list_to_search, needle, 1)

def find_n(list_to_search, needle, occurrence):
  """
  Return True if needle's occurrences are found one or more times in list_to_search
  False if there's less needle's occurrences or occurrence < 0
  """
  if occurrence >= 0:
    count = 0
    index = 0
    while count < occurrence and index < len(list_to_search):
      count += 1 if needle == list_to_search[index] else 0
      index += 1
    return count >= occurrence
  else:
    return False

def find_streak(list_to_search, needle, streak):
  """
  Return True if needle's occurrences are found in one or more streaks in list_to_search
  False if there's less needle's occurrences or occurrence < 0
  """
  if streak >= 0:
    in_streak = False
    count = 0
    index = 0
    while count < streak and index < len(list_to_search):
      if needle == list_to_search[index]:
        count += 1
        in_streak = True
      else:
        count = 0
        in_streak = False
      index += 1
    return count >= streak and in_streak
  else:
    return False
  
def first_elements(list_of_lists):
  """
  Return a list with the first elements from a list of lists
  """
  return nth_elements(list_of_lists, 0)

def nth_elements(list_of_lists, n):
  """
  Return a list with the n elements from a list of lists
  """
  return list(map(lambda x : x[n] if x else None, list_of_lists))

def transpose(matrix):
  """
  Transpose a given matrix
  """
  length = len(next(iter(matrix)))
  if not all(len(l) == length for l in matrix):
    raise ValueError("not all lists have the same length!!!")
  else:
    """ transpose_matrix = []
    for i in range(len(matrix[0])):
      transpose_matrix.append(nth_elements(matrix, i)) """
    return list(map(lambda x, i: nth_elements(matrix, i), matrix[0], range(len(matrix[0]))))
  
def displace(list, distance, filler=None):
  if distance == 0:
    return list
  elif distance > 0:
    filling = [filler] * distance
    res = filling + list
    res = res[:-distance]
    return res
  else:
    filling = [filler] * abs(distance)
    res = list + filling
    res = res[abs(distance):]
    return res
  
def displace_matrix(list_of_lists, filler=None):
  return list(map(lambda x, i: displace(x, i - 1, filler), list_of_lists, range(len(list_of_lists))))

def reverse_list(l):
  return list(reversed(l))

def reverse_matrix(matrix):
  return list(map(lambda x: reverse_list(x), matrix))

def all_same(test_list):
  """
  Return True if all the elements in the list are the same or empty
  """
  return all(test_list[0] == value for value in test_list)