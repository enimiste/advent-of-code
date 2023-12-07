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
      'o': {
          'n': {
              'e': {
                  'e_o_w': True,
                  'value': '1'
              }
          }
      },
      't': {
          'w': {
              'o': {
                  'e_o_w': True,
                  'value': '2'
              }
          },
          'h': {
            'r': {
                'e': {
                  'e': {
                      'e_o_w': True,
                      'value': '3'
                  }
                }
            }
        },
      },
      'f': {
          'o': {
              'u': {
                'r': {
                    'e_o_w': True,
                    'value': '4'
                }
              }
          },
          'i': {
              'v': {
                'e': {
                    'e_o_w': True,
                    'value': '5'
                }
              }
          }
      },
      's': {
          'i': {
              'x': {
                  'e_o_w': True,
                  'value': '6'
              }
          },
          'e': {
              'v': {
                'e': {
                  'n': {
                      'e_o_w': True,
                      'value': '7'
                  }
                }
              }
          }
      },
      'e': {
          'i': {
            'g': {
              'h': {
                  't': {
                      'e_o_w': True,
                      'value': '8'
                  }
              }
            }
          }
      },
      'n': {
          'i': {
              'n': {
                'e': {
                    'e_o_w': True,
                    'value': '9'
                }
              }
          }
      },
    #'one': '1',
    #'two': '2',
    #'three': '3',
    #'four': '4',
    #'five': '5',
    #'six': '6',
    #'seven': '7',
    #'eight': '8',
    #'nine': '9',
  }

  def replace_letters_by_digit(line: str, start_index: int) -> str:
    N = len(line)
    if start_index>=N:
      return line
    i = start_index
    ds = letters_to_digit
    number = None
    while i<N:
      c = line[i]
      if c in ds:
        ds = ds[c]
        if 'e_o_w' in ds:
          number = ds['value']
          break
        else:
          i+=1
      else:
        break
    if i>=N:
      return line
    elif number is not None:
      return replace_letters_by_digit(line[0:start_index] + number + line[i+1:], start_index+1)
    return replace_letters_by_digit(line, start_index+1)

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
  return [calib for calib in [parse_line(replace_letters_by_digit(line, 0)) for line in lines if len(line)>0] if calib is not None]


if __name__=="__main__":
  lines = example.splitlines()
  #lines = read_input()
  calibs = calibrations(lines)
  print(calibs)# 29, 83, 13, 24, 42, 14, and 76
  print(sum(calibs))# 56042
