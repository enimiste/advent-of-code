"""
Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.
It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.
"Aaah!"
You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.
The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.
The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)
Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.
Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""
import re

def read_input() -> list[str]:
  from os import path
  base_dir = path.dirname(__file__)
  lines = []
  with open(base_dir + '/input.txt', 'r') as inputFile:
    lines =  inputFile.readlines()
  return lines

def is_numeric(char: str) -> bool:
  return char in ['0','1','2','3','4','5','6','7','8','9']

def is_symbole(char: str) -> bool:
  if len(char)==0 or len(char)>1 or char==' ':
    raise RuntimeError
  
  return  char != '.' and not is_numeric(char)

def next_number(line: str, startIndex: int) -> (int, int, int): #(number, startIndex, endIndex) or None
  N = len(line)
  if N==0:
    return None
  if startIndex>= N:
    return None
  if not is_numeric(line[startIndex]):
    return next_number(line, startIndex+1)
  
  number = ""
  j = startIndex
  while j < N and is_numeric(line[j]):
    number+=line[j]
    j+=1

  if len(number)==0:
    return None
  return (int(number), startIndex, j-1)

def next_numbers_all(line: str, startIndex: int=0) -> list[(int, int, int)]:
  nums=[]
  next_num = next_number(line, startIndex)
  while next_num is not None:
    nums.append(next_num)
    next_num = next_number(line, next_num[2]+1)
  return nums

def number_has_adjacent_symbol(lineIndx:int, startIndex: int, endIndex: int, lines: list[str]) -> bool:
  NN = len(lines)
  curr_line = lines[lineIndx]
  # Same line
  if startIndex>0:
    if is_symbole(curr_line[startIndex-1]):
      return True
  if endIndex<len(curr_line)-1:
    if is_symbole(curr_line[endIndex+1]):
      return True
  # Next Line
  for i in (lineIndx-1, lineIndx+1):
    if i>=0 and i<NN:
      line = lines[i]
      N = len(line)
      for j in range(startIndex-1, endIndex+2):
        if j>=0 and j<N:
          if is_symbole(line[j]):
            return True
  return False

def gear_ratios(lines: list[str], write=False) -> int:
  from collections import defaultdict
  if write:
    found_nums_per_line = defaultdict(list)
  sum = 0
  for idx, line in enumerate(lines):
    all_next_nums = next_numbers_all(line, 0)
    for next_num in all_next_nums:
       if number_has_adjacent_symbol(idx, next_num[1], next_num[2], lines):
        sum += next_num[0]
        if write:
          found_nums_per_line[idx].append(next_num[0])

  if write:
    with open('output.txt', 'w') as fl:
      fl.write(f"Input lines count : {len(lines)}\n")
      fl.writelines([f"Line {k+1} : {str(found_nums_per_line[k])}\n" for k in found_nums_per_line.keys()])
  return sum
  

# ------- TESTS
def test_dummy():
  assert True

def test_input_file_readable():
  lines = read_input()
  assert len(lines)>0

def test_no_line():
  assert gear_ratios([])==0

def test_is_symbole_many_cases():
  assert is_symbole("3")==False
  assert is_symbole("0")==False
  assert is_symbole("#")==True
  assert is_symbole("*")==True
  assert is_symbole(".")==False
  try:
    is_symbole("")
    assert False
  except RuntimeError:
    assert True
  try:
    is_symbole(" ")
    assert False
  except RuntimeError:
    assert True
  try:
    is_symbole("22")
    is_symbole(".*")
    assert False
  except RuntimeError:
    assert True

def test_next_number_empty_str():
  assert next_number("", 0)==None

def test_next_number_only_symbole_str():
  assert next_number("#....*", 0)==None

def test_next_number_on_number():
  assert next_number("123", 0)==(123, 0, 2)

def test_next_number_neg_on_number():
  assert next_number("-123", 0)==(123, 1, 3)

def test_next_number_on_number_endswith_symbol():
  assert next_number("123*", 0)==(123, 0, 2)

def test_next_number_on_number_startswith_symbol():
  assert next_number("#123", 0)==(123, 1, 3)

def test_next_number_two_numbers():
  n1 = next_number("467..114..", 0)
  assert n1==(467, 0, 2)
  n2 = next_number("467..114..", n1[2]+1)
  assert n2==(114, 5, 7)

def test_next_number_two_numbers_with_neg_sign():
  n1 = next_number("467..-114..", 0)
  assert n1==(467, 0, 2)
  n2 = next_number("467..-114..", n1[2]+1)
  assert n2==(114, 6, 8)


def test_number_has_adjacent_symbol_one_line_no_symbole_adjacent():
  lines = [
    "467..114.."
  ]
  assert not number_has_adjacent_symbol(0, 0, 2, lines)

def test_number_has_adjacent_symbol_one_line():
  line = "467..114.."
  ns = next_numbers_all(line)
  assert [n for (n, _, _) in ns]==[467, 114]

def test_number_has_adjacent_symbol_one_line_from_big_example():
  line =  ".......+......110..735..........647....658.509*378..........-999............*....#225....937.............147.........778...868.....871..611."
  
  ns = next_numbers_all(line)
  assert [n for (n, _, _) in ns]==[110, 735, 647, 658, 509, 378, 999, 225, 937, 147, 778, 868, 871, 611]

def test_number_has_adjacent_symbol_one_line_without_symbole_adjacent_one_number():
  lines = [
    "467"
  ]
  assert not number_has_adjacent_symbol(0, 0, 2, lines)

def test_number_has_adjacent_symbol_one_line_with_symbole_adjacent():
  lines = [
    "467*..114.."
  ]
  assert number_has_adjacent_symbol(0, 0, 2, lines)

def test_number_has_adjacent_symbol_two_lines_with_symbole_adjacent_on_next_line():
  lines = [
    "467..114..",
    "...*......"
  ]
  assert number_has_adjacent_symbol(0, 0, 2, lines)

def test_number_has_adjacent_symbol_two_lines_with_symbole_not_adjacent_on_next_line():
  lines = [
    "467..114..",
    "....*....."
  ]
  assert not number_has_adjacent_symbol(0, 0, 2, lines)

def test_number_has_adjacent_symbol_two_lines_with_symbole_adjacent_on_previous_line():
  lines = [
    "...*......",
    "467..114.."
  ]
  assert number_has_adjacent_symbol(1, 0, 2, lines)

def test_one_line_no_symbole():
  assert gear_ratios([
    "123"
  ])==0

def test_one_line_one_number_with_adjacent_symbole_right():
  assert gear_ratios([
    "123#"
  ])==123

def test_one_line_one_number_with_adjacent_symbole_left():
  assert gear_ratios([
    "#123"
  ])==123

def test_example():
  assert gear_ratios([
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
  ])==4361

def test_big_example():
  lines = read_input()
  assert gear_ratios(lines, write=True)==539127


if __name__=='__main__':
  import sys
  from os import path

  if len(sys.argv)<=1:
      print("Usage : python test_gear-ration.py input/file/path")
      exit()

  input_file = sys.argv[1]
  if not path.exists(input_file):
      print("input path does'nt exist : " + input_file)
      exit()
  if not path.isfile(input_file):
      print("The input path should point to a txt file : " + input_file)
      exit()
  lines = []
  with open(input_file, 'r') as inputFile:
    lines =  inputFile.readlines()
  res = gear_ratios(lines)
  print(f"Sum is : {res}")