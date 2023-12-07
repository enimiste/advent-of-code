"""

"""
example = """

"""


from typing import Tuple, Union

def read_input() -> list[str]:
  from os import path
  base_dir = path.dirname(__file__)
  lines = []
  with open(base_dir + '/input.txt', 'r') as inputFile:
    lines =  inputFile.readlines()
  return lines

# TODO

if __name__=="__main__":
  lines = example.splitlines()
  #lines = read_input()
  # TODO