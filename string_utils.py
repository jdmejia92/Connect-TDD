def explode_string(a_string):
  """
  Convert a string into a list of chars
  'Han' => ['H', 'a', 'n']
  """
  return list(a_string)

def explode_list_of_strings(list_of_strings):
  """
  Applied explode_string into each string of the list
  """
  return list(map(lambda x : explode_string(x), list_of_strings))