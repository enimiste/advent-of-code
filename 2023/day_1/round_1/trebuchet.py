"""
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.
You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.
Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!
You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").
As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.
The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.
For example:
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.
Consider your entire calibration document. What is the sum of all of the calibration values?
"""
example = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
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
  return [calib for calib in [parse_line(line) for line in lines if len(line)>0] if calib is not None]

if __name__=="__main__":
  #lines = example.splitlines()
  lines = read_input()
  calibs = calibrations(lines)
  print(sum(calibs))# 56042
