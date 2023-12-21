"""
--- Day 7: Camel Cards ---
Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.

"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree automatically.

Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?
"""
example = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


from typing import Tuple, Union

def read_input() -> list[str]:
  from os import path
  base_dir = path.dirname(__file__)
  lines = []
  with open(base_dir + '/input.txt', 'r') as inputFile:
    lines =  inputFile.readlines()
  return lines

def parse_lines(lines: list[str]) -> list[Tuple[str, int]]:
  rs=list()
  for line in lines:
    parts = line.split(" ")
    rs.append((parts[0].strip(), int(parts[1].strip())))
  return rs


def total_winings(hands: list[Tuple[str, int]]) -> int:
  class Hand(object):
    """
    https://python-course.eu/oop/magic-methods.php
    """

    CARDS_OPTIONS = {'2': 2,'3': 3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'K':12,'Q':13,'A':14}
    CARDS_OPTIONS_SET = set(CARDS_OPTIONS.keys())

    FIVE_OF_K = (100, "Five of Kind")
    FOUR_OF_K = (90, "Four of Kind")
    FULL_HOUSE = (80, "Full House")
    THREE_OF_K = (70, "Three of Kind")
    TWO_PAIR = (60, "Two Pair")
    ONE_PAIR = (50, "One Pair")
    HIGH_CARD = (40, "High Card")

    def __init__(self, cards: str, bid: int) -> None:
      if len(cards) != 5:
        raise RuntimeError("Invalid Hand : 5 cards")
      
      if not set(cards[::1]).issubset(Hand.CARDS_OPTIONS_SET):
        raise RuntimeError(f"Invalid Hand : {set(cards[::1])} should be subset of {Hand.CARDS_OPTIONS_SET}")
      self.cards = cards
      self.bid = bid
      self.hand_type = Hand._parse_hand_type(cards)
    
    def _check_invariant(__value: object) -> None:
      if __value is None or not isinstance(__value, Hand):
        raise RuntimeError("Invalid operation")
      
    def __eq__(self, __value: object) -> bool:
      Hand._check_invariant(__value)
      return __value.cards==self.cards
      
    def __lt__(self, __value: object) -> bool:
      Hand._check_invariant(__value)
      return __value.hand_type[0]<self.hand_type[0] or (
        __value.hand_type[0]==self.hand_type[0] and Hand._compare_cards(__value.cards, self.cards)<0
      )

    def __le__(self, __value: object) -> bool:
      Hand._check_invariant(__value)
      return self.__eq__(__value) or self.__lt__(__value)
    
    def __repr__(self) -> str:
      return f"(cards={self.cards}, type={self.hand_type[1]}, \tbid={self.bid})"
    
    def _compare_cards(cards_a: str, cards_b: str) -> int:
      if len(cards_a)<len(cards_b):
        return -1
      elif len(cards_a)>len(cards_b):
        return 1
      if cards_a==cards_b:
        return 0
      for a, b in zip(cards_a, cards_b):
        if Hand.CARDS_OPTIONS[a]<Hand.CARDS_OPTIONS[b]:
          return -1
        if Hand.CARDS_OPTIONS[a]>Hand.CARDS_OPTIONS[b]:
          return 1
        
      return 0
    
    def _parse_hand_type(hand: str) -> Tuple[int, str]:
      # Frequencies
      freq = dict()
      for c in hand:
        if c not in freq:
          freq[c]=0
        freq[c]+=1

      len_freq=len(freq)
      freq_values = set(freq.values())

      if len_freq==1:
        return Hand.FIVE_OF_K
      
      if len_freq==2:
        if 4 in freq_values:
          return Hand.FOUR_OF_K
        if 3 in freq_values:
          return Hand.FULL_HOUSE
        
      if len_freq==3:
        if 3 in freq_values:
          return Hand.THREE_OF_K
        if 2 in freq_values:
          return Hand.TWO_PAIR
        
      if len_freq==4:
        if 2 in freq_values:
          return Hand.ONE_PAIR
        
      if len_freq==5:
        return Hand.HIGH_CARD
      
      raise RuntimeError(f"Unknown Card Type for : {hand}")
  #-----------------------
  hs = [Hand(c, b) for c, b in hands]
  hs.sort()
  r = 0
  for rank, hand in zip(range(len(hs), 0, -1), hs):
    print(f"{rank} \t: {hand}")
    r += rank * hand.bid
  return r

if __name__=="__main__":
  #lines = example.splitlines()
  lines = read_input()
  #lines = input.splitlines()
  hands = parse_lines(lines)
  print(total_winings(hands))
  # 6440 (example)
  # 252702232 (input) ==> KO