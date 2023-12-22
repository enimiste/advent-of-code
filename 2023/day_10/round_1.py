"""
--- Day 10: Pipe Maze ---
You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....
If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....
In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF
In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....
You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....
In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...
Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?
"""
example1 = """-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

example2 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""


from typing import Tuple, Union

def read_input() -> list[str]:
  from os import path
  base_dir = path.dirname(__file__)
  lines = []
  with open(base_dir + '/input.txt', 'r') as inputFile:
    lines =  inputFile.readlines()
  return lines

def parse_lines(lines: list[str]) -> Tuple[Tuple[int,int, str], set[Tuple[int,int, str]]]:
  res = set()
  S = None
  for i in range(0, len(lines)):
    line = lines[i]
    for j in range(0, len(line)):
      cell = line[j]
      if not cell == '.':
        if cell == 'S':
          S = (i,j,cell)
        res.add((i,j,cell))
  return (S, res)

def find_main_loop(starting_point: Tuple[int,int, str], grid: set[Tuple[int,int, str]]) -> list[Tuple[int,int]]:
  cell_dir_mp = {(i, j):c for i,j,c in grid}
  cells = {(i, j) for i,j,c in grid}

  def neighbors(cell: Tuple[int,int]) -> set[Tuple[int,int]]:
    return {(cell[0]-1, cell[1]), (cell[0]+1, cell[1]), (cell[0], cell[1]-1), (cell[0], cell[1]+1)}

  def next_hope(from_cell: Tuple[int, int], via_cell: Tuple[int, int], direction: str) -> Union[Tuple[int, int], None]:
    #TODO
    pass

  def find_main_loop_recur(current_point: Tuple[int,int], 
                           grid: set[Tuple[int,int]],
                           loop: list[Tuple[int,int]]) -> list[Tuple[int,int]]:
    #TODO
    pass
  
  return find_main_loop_recur(tuple(list(starting_point)[:2]), cells, [])

def steps_from_starting_to_farthest(loop: list[Tuple[int,int]]) -> int:
  return len(loop)//2

if __name__=="__main__":
  lines = example1.splitlines()
  #lines = example2.splitlines()
  #lines = read_input()
  starting_point, grid = parse_lines(lines)
  print(steps_from_starting_to_farthest(find_main_loop(starting_point, grid)))
  # 4 (example1),
  # 8 (example2),
  # ___ (input)