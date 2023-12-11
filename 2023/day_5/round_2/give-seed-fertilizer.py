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
import re

def composite_function(func: list, reverse=False):
  if reverse:
    func = list(reversed(func))
  def compose(f, g): 
      return lambda x : f(g(x))  
  return reduce(compose, func, lambda x : x) 
def memoized(func):
  cache = dict()
  def fn(args):
    if args in cache:
      return cache[args]
    else:
      v = func(args)
      cache[args]=v
      return v
  return fn 
# MAP ITEM = (destination range start, the source range start, the range length)
def map_def(items: list[Tuple[int, int, int]]) -> callable:
  """
  :rtype Function[int, Union[int, None]]
  """
  def map_item_def(dest: int, start: int, interval: int) -> callable:
    """
    :rtype Function[int, Union[int, None]]
    """
    def eval_fn(val: Union[int, None]) -> Union[int, None]:
      if val is None:
        return None
      if start<=val<start+interval:
        return dest+(val-start)
    return eval_fn

  FUNCS = [map_item_def(d, s, itrv) for d, s, itrv in items]
  def eval_fn(val: Union[int, None]) -> Union[int, None]:
    if val is None:
      return None
    for fn in FUNCS:
      r = fn(val)
      if r is not None:
        return r
    return val
  return eval_fn

def parse_input(lines: list[str]) -> Tuple[list[int], list[list[int]]]:
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

def min_location(lines: list[str]) -> int:
  seeds_config, map_config = parse_input(lines)
  print(seeds_config)
  print(map_config)
  cs = composite_function([map_def(mc) for mc in map_config if len(mc)>0], reverse=True)
  min_ = None
  for i in range(0, len(seeds_config), 2):
    for seed in range(seeds_config[i], seeds_config[i]+seeds_config[i+1]):
      tmp_min = cs(seed)
      if min_ is None:
        min_ = tmp_min
      else:
        min_ = min(min_, tmp_min)

  return min_


if __name__=="__main__":
  #lines = example.splitlines()
  lines = read_input()
  print(min_location(lines))# timeout on colab
