"""
--- Part Two ---
The Elf says they've stopped producing snow because they aren't getting any water! He isn't sure why the water stopped; however, he can show you how to get to the water source to check it out for yourself. It's just up ahead!

As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
Game 4 required at least 14 red, 3 green, and 15 blue cubes.
Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
"""
example = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

from typing import Tuple, Union

def read_input() -> list[str]:
  from os import path
  base_dir = path.dirname(__file__)
  lines = []
  with open(base_dir + '/input.txt', 'r') as inputFile:
    lines =  inputFile.readlines()
  return lines

def parse_games(lines: list[str]) -> list[(int, set[(int, int, int)])] :
  import re
  pattern = r"^Game (\d+): (?(\d+) blue,)*;(?)$" #TODO
  def parse_game(lineIdx: int, line: str) -> Union[Tuple[int, set[Tuple[int, int, int]]], None]:
    def split_game_parts(line: str) -> Union[Tuple[str, set[str]], None]:
      """
      ex : Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
      """
      if len(line)==0:
        return None
      parts = line.split(";")
      if len(parts)<2:
        return None
      ps = parts[0].split(":")
      if len(ps)<2:
        return None
      game = ps[0]#Game 1
      sets = set([ps[1]] + parts[1:])
      return (game, sets)

    def extractGameId(game: str) -> int:
      """
      ex : Game 1
      """
      return int(game.split(" ")[1].strip())

    def extractCubes(game_set: str) -> Tuple[int, int, int]:
      """
      ex :
      8 green, 6 blue, 20 red
      3 blue, 4 red
      2 green
      """
      colors_idx = {"red": 0,"green": 1,"blue": 2}
      colors = [0,0,0]
      for color_str in game_set.split(","):
        ps = color_str.strip().split(" ")
        colors[colors_idx[ps[1].strip()]]=int(ps[0].strip())

      return tuple(colors)

    sp = split_game_parts(line)
    if sp is None:
      return None
    game_id, game_sets = sp
    return (extractGameId(game_id), {extractCubes(gs) for gs in game_sets})
  
  return [x for x in [parse_game(idx, line) for idx, line in enumerate(lines)] if x is not None]

def power(games: list[(int, set[(int, int, int)])]) -> list[Tuple[int, int]]:
  def prod(iter) -> int:
    p = 1
    for i in iter:
      if i!=0:
        p *= i
    return p
  def min_cubes_set(g_sets: set[(int, int, int)]) -> Tuple[int, int, int]:
    maxs = [0,0,0]
    for s in g_sets:
      maxs[0] = max(maxs[0], s[0])
      maxs[1] = max(maxs[1], s[1])
      maxs[2] = max(maxs[2], s[2])
    return maxs
  
  return [(id, prod(min_cubes_set(game_sets))) for (id, game_sets) in games]

def power_over_all_games(powers: list[Tuple[int, int]]) -> int:
  return sum([power for (_, power) in powers])

if __name__=="__main__":
  lines = example.splitlines()
  games = parse_games(lines)
  print(power_over_all_games(power(games)))

