"""
--- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.
The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:
seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.
Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.
In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.
Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
"""
example = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

from typing import Tuple, Union
from functools import reduce

def composite_function(func: list, reverse=False):
  if reverse:
    func = list(reversed(func))
  def compose(f, g):
      return lambda x : f(g(x))
  return reduce(compose, func, lambda x : x)

def read_input() -> list[str]:
  from os import path
  base_dir = path.dirname(__file__)
  lines = []
  with open(base_dir + '/input.txt', 'r') as inputFile:
    lines =  inputFile.readlines()
  return lines

def parse_input(lines: list[str]) -> Tuple[list[int], list[list[Tuple[int, int, int]]]]:
  seeds_config = []
  map_config=[]
  tmp = None
  for line in lines:
    if "seeds: " in line:
      #extracts seeds_config
      while not line[0].isnumeric():
        line = line[1:]
      seeds_config=[int(numb.strip()) for numb in line.split(" ")]
    elif len(line.strip())==0:
      tmp = []
      map_config.append(tmp)
    elif not line[0].isnumeric():
      continue
    else:
      tmp.append(tuple([int(numb.strip()) for numb in line.split(" ")]))
  return (seeds_config, map_config)

def map_def0(map_config: list[Tuple[int, int, int]]) -> callable:
  def gn(plage: Tuple[int, int], map_item: Tuple[int, int, int]) -> Tuple[set[Tuple[int, int]], set[Tuple[int, int]]]:
    """
    :rtype (mapped range, remaining range)
    """
    S, J=plage
    D, M, I=map_item

    E=S+J-1
    N=M+I-1

    if E<M or S>N:
      return (set(), {plage})
    if S>=M and E<=N:
      return ({(D+S-M, J)}, set())
    if S<M and E>=M and E<=N:
      return ({(D,E-M+1)}, {(S,M-S)})
    if S>=M and S<=N and E>N:
      return ({(D+S-M,N-S+1)}, {(N+1,E-N)})
    if S<M and E>N:
      return ({(D,I)}, {(S,M-S), (N+1,E-N)})

    return plage

  def fn(plages: set[Tuple[int, int]]) -> set[Tuple[int, int]]:
    if len(map_config)==0:
      return plages

    res = set()
    for plage in plages:
      mapped, no_mapped = gn(plage, map_config[0])
      for x in mapped:
          res.add(x)
      ys = no_mapped
      for map_c in map_config[1:]:
        ys_ = set()
        for y in ys:
          mapped_, no_mapped_ = gn(y, map_c)
          for x in mapped_:
              res.add(x)
          for z in no_mapped_:
            ys_.add(z)
        ys = ys_
      for y in ys:
            res.add(y)
    return res
  return fn

def make_seeds(config: list[int]) -> set[Tuple[int, int]]:
  if len(config)%2!=0:
    raise RuntimeError("Invalid config")
  return set(zip(config[::2], config[1::2]))

def min_location(lines: list[str]) -> int:
  seeds_config, map_config = parse_input(lines)
  cs = composite_function([map_def0(mc) for mc in map_config], reverse=True)
  seeds = make_seeds(seeds_config)
  rs = cs(seeds)
  return min([elem[0] for elem in rs], default=-1)


if __name__=="__main__":
  #lines = example.splitlines()
  lines = read_input()
  print(min_location(lines))# 34039469 (input)
