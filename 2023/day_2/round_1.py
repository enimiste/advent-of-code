"""
--- Day 2: Cube Conundrum ---
You're launched high into the atmosphere! The apex of your trajectory just barely reaches the surface of a large island floating in the sky. You gently land in a fluffy pile of leaves. It's quite cold, but you don't see much snow. An Elf runs over to greet you.

The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow. He'll be happy to explain the situation, but it's a bit of a walk, so you have some time. They don't get many visitors up here; would you like to play a game in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. Each time you play this game, he will hide a secret number of cubes of each color in the bag, and your goal is to figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the bag, grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input). Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, three sets of cubes are revealed from the bag (and then put back again). The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?
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

def possible_games_ids(games: list[(int, set[(int, int, int)])]) -> set[int]:
  def is_possible(game_sets: set[(int, int, int)]) -> bool:
    def strategy(game_set: Tuple[int, int, int]) -> bool:
      BAG = (12, 13, 14)#(red, green, blue)
      (r, g, b) = game_set
      b = r<=BAG[0] and g<=BAG[1] and b<=BAG[2]
      return b
    for gs in game_sets:
      if not strategy(gs):
        return False
    return True
  
  return {id for (id, game_sets) in games if is_possible(game_sets)}

if __name__=="__main__":
  #lines = example.splitlines()
  lines = read_input()
  games = parse_games(lines)
  print(sum(possible_games_ids(games)))# 2265
