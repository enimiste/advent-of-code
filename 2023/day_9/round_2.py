"""
--- Part Two ---
Of course, it would be nice to have even more history included in your report. Surely it's safe to just extrapolate backwards as well, right?

For each history, repeat the process of finding differences until the sequence of differences is entirely zero. Then, rather than adding a zero to the end and filling in the next values of each previous sequence, you should instead add a zero to the beginning of your sequence of zeroes, then fill in new first values for each previous sequence.

In particular, here is what the third example history looks like when extrapolating back in time:

5  10  13  16  21  30  45
  5   3   3   5   9  15
   -2   0   2   4   6
      2   2   2   2
        0   0   0
Adding the new values on the left side of each sequence from bottom to top eventually reveals the new left-most history value: 5.

Doing this for the remaining example data above results in previous values of -3 for the first history and 0 for the second history. Adding all three new values together produces 2.

Analyze your OASIS report again, this time extrapolating the previous value for each history. What is the sum of these extrapolated values?
"""
example = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


from typing import Tuple, Union

def read_input() -> list[str]:
  from os import path
  base_dir = path.dirname(__file__)
  lines = []
  with open(base_dir + '/input.txt', 'r') as inputFile:
    lines =  inputFile.readlines()
  return lines

def parse_lines(lines: list[str]) -> list[list[int]]:
  return [list(map(int, line.split(" "))) for line in lines]

def next_sequence(sequence: list[int]) -> int:
  def differences(sequence: list[int]) -> list[int]:
    return [p[1]-p[0] for p in zip(sequence, sequence[1:])]

  seqs = [sequence]
  while not all([v==0 for v in sequence]):
    sequence = differences(sequence)
    seqs.append(sequence)
  
  for i in range(len(seqs)-2, -1, -1):
    seqs[i].insert(0, seqs[i][0] - seqs[i+1][0])
  
  return seqs[0][0]

def sum_expolated_values(sequences: list[list[int]]) -> int:
  return sum([next_sequence(sequence) for sequence in sequences])


if __name__=="__main__":
  #lines = example.splitlines()
  lines = read_input()
  print(sum_expolated_values(parse_lines(lines)))# 2 (example), 1005 (input)