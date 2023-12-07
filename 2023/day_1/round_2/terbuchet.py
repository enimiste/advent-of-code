"""
-- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
"""

example = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

from typing import Tuple, Union

def read_input() -> list[str]:
  from os import path
  base_dir = path.dirname(__file__)
  lines = []
  with open(base_dir + '/input.txt', 'r') as inputFile:
    lines =  inputFile.readlines()
  return lines

def calibrations(lines: list[str]) -> list[int]:
  letters_to_digit = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
  }
  def replace_letters_by_digit(line: str) -> str:
    # TODO
    pass
  def parse_line(line: str) -> Union[int, None]:
    s,e=(0,len(line)-1)
    start_digit_found, end_digit_found=False, False
    while s<=e:
      if not line[s].isnumeric():
        s+=1
      else:
        start_digit_found=True
      if not line[e].isnumeric():
        e-=1
      else:
        end_digit_found=True
      if start_digit_found and end_digit_found:
        return int(line[s] + line[e])
    
    return None
  return [calib for calib in [parse_line(replace_letters_by_digit(line)) for line in lines if len(line)>0] if calib is not None]

if __name__=="__main__":
  lines = example.splitlines()
  #lines = read_input()
  calibs = calibrations(lines)
  print(calibs)# 29, 83, 13, 24, 42, 14, and 76
  print(sum(calibs))# 56042