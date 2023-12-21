"""
--- Part Two ---
As the race is about to start, you realize the piece of paper with race times and record distances you got earlier actually just has very bad kerning. There's really only one race - ignore the spaces between the numbers on each line.

So, the example from before:

Time:      7  15   30
Distance:  9  40  200
...now instead means this:

Time:      71530
Distance:  940200
Now, you have to figure out how many ways there are to win this single race. In this example, the race lasts for 71530 milliseconds and the record distance you need to beat is 940200 millimeters. You could hold the button anywhere from 14 to 71516 milliseconds and beat the record, a total of 71503 ways!

How many ways can you beat the record in this one much longer race?
"""
example = """Time:      7  15   30
Distance:  9  40  200
"""


from typing import Tuple, Union

def read_input() -> list[str]:
  from os import path
  base_dir = path.dirname(__file__)
  lines = []
  with open(base_dir + '/input.txt', 'r') as inputFile:
    lines =  inputFile.readlines()
  return lines

def parse_lines(lines: list[str]) -> Tuple[int, int]:
  if len(lines)!=2:
    raise RuntimeError("There should be two lines max")
  def extract_values_from_prefixed_line(line: str, prefix: str) -> int:
    return int(line.replace(prefix, "").replace(" ", "").strip())
  
  time = extract_values_from_prefixed_line(lines[0], "Time:")
  distance = extract_values_from_prefixed_line(lines[1], "Distance:")

  return (time, distance)

def race_distance(time: int, distance_per_time: int) -> int:
  return time * distance_per_time

def count_race_ways(time: int, distance: int) -> int:
  count = 0
  for a in range(0, time+1):
    d = race_distance(time-a, a)
    if d>distance:
      count+=1
  return count

def error_marge(race: Tuple[int, int]) -> int:
  print(race)
  return count_race_ways(race[0], race[1])

if __name__=="__main__":
  #lines = example.splitlines()
  lines = read_input()
  print(error_marge(parse_lines(lines)))# 71503 (example), 30565288 (input)