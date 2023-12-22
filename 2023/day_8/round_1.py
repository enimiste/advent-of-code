"""
--- Day 8: Haunted Wasteland ---
You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning you about ghosts a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
"""
example1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

example2="""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


from typing import Tuple, Union, Dict

def read_input() -> list[str]:
  from os import path
  base_dir = path.dirname(__file__)
  lines = []
  with open(base_dir + '/input.txt', 'r') as inputFile:
    lines =  inputFile.readlines()
  return lines

def parse_lines(lines: list[str]) -> Tuple[list[str], Dict[str, Tuple[str, str]]]:
  instructions = dict()
  for line in lines[2:]:
    ps = line.split("=")
    k = ps[0].strip()
    d = ps[1].replace("(", "").replace(")", "").split(",")
    instructions[k] = tuple([x.strip() for x in d])
  return (list(lines[0][::]), instructions)

def steps_count(maps: Dict[str, Tuple[str, str]], instructions: list[str]) -> int:
  import time
  next_node = 'AAA'
  curr_instruction_index = 0
  steps_count_acc = 0

  st_time = time.time()
  while True:
    instruction = instructions[curr_instruction_index]
    next_node = maps[next_node][0 if instruction=='L' else 1]
    
    if next_node=='ZZZ':
      return steps_count_acc + 1
    curr_instruction_index = (curr_instruction_index+1)%len(instructions)
    steps_count_acc+=1
    
    if time.time()-st_time>10:#10sec, in case it doesn't converge to ZZZ
      raise RuntimeError("Timeout Execution Limit (10sec)")
  
  return steps_count_acc

if __name__=="__main__":
  #lines = example1.splitlines()
  #lines = example2.splitlines()
  lines = read_input()
  instructions, maps = parse_lines(lines)
  print(steps_count(maps, instructions))
  # 2 (example 1), 
  # 6 (example 2), 
  # 17009 (input) ==> KO