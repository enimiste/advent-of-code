
# ------- TESTS
from round_1 import input, gear_ratios, is_symbole, next_number, number_has_adjacent_symbol, next_numbers_all


def test_dummy():
  assert True

def test_no_line():
  assert gear_ratios([])==0

def test_is_symbole_many_cases():
  assert is_symbole("3")==False
  assert is_symbole("0")==False
  assert is_symbole("#")==True
  assert is_symbole("*")==True
  assert is_symbole(".")==False
  try:
    is_symbole("")
    assert False
  except RuntimeError:
    assert True
  try:
    is_symbole(" ")
    assert False
  except RuntimeError:
    assert True
  try:
    is_symbole("22")
    is_symbole(".*")
    assert False
  except RuntimeError:
    assert True

def test_next_number_empty_str():
  assert next_number("", 0)==None

def test_next_number_only_symbole_str():
  assert next_number("#....*", 0)==None

def test_next_number_on_number():
  assert next_number("123", 0)==(123, 0, 2)

def test_next_number_neg_on_number():
  assert next_number("-123", 0)==(123, 1, 3)

def test_next_number_on_number_endswith_symbol():
  assert next_number("123*", 0)==(123, 0, 2)

def test_next_number_on_number_startswith_symbol():
  assert next_number("#123", 0)==(123, 1, 3)

def test_next_number_two_numbers():
  n1 = next_number("467..114..", 0)
  assert n1==(467, 0, 2)
  n2 = next_number("467..114..", n1[2]+1)
  assert n2==(114, 5, 7)

def test_next_number_two_numbers_with_neg_sign():
  n1 = next_number("467..-114..", 0)
  assert n1==(467, 0, 2)
  n2 = next_number("467..-114..", n1[2]+1)
  assert n2==(114, 6, 8)


def test_number_has_adjacent_symbol_one_line_no_symbole_adjacent():
  lines = [
    "467..114.."
  ]
  assert not number_has_adjacent_symbol(0, 0, 2, lines)

def test_number_has_adjacent_symbol_one_line():
  line = "467..114.."
  ns = next_numbers_all(line)
  assert [n for (n, _, _) in ns]==[467, 114]

def test_number_has_adjacent_symbol_one_line_from_big_example():
  line =  ".......+......110..735..........647....658.509*378..........-999............*....#225....937.............147.........778...868.....871..611."
  
  ns = next_numbers_all(line)
  assert [n for (n, _, _) in ns]==[110, 735, 647, 658, 509, 378, 999, 225, 937, 147, 778, 868, 871, 611]

def test_number_has_adjacent_symbol_one_line_without_symbole_adjacent_one_number():
  lines = [
    "467"
  ]
  assert not number_has_adjacent_symbol(0, 0, 2, lines)

def test_number_has_adjacent_symbol_one_line_with_symbole_adjacent():
  lines = [
    "467*..114.."
  ]
  assert number_has_adjacent_symbol(0, 0, 2, lines)

def test_number_has_adjacent_symbol_two_lines_with_symbole_adjacent_on_next_line():
  lines = [
    "467..114..",
    "...*......"
  ]
  assert number_has_adjacent_symbol(0, 0, 2, lines)

def test_number_has_adjacent_symbol_two_lines_with_symbole_not_adjacent_on_next_line():
  lines = [
    "467..114..",
    "....*....."
  ]
  assert not number_has_adjacent_symbol(0, 0, 2, lines)

def test_number_has_adjacent_symbol_two_lines_with_symbole_adjacent_on_previous_line():
  lines = [
    "...*......",
    "467..114.."
  ]
  assert number_has_adjacent_symbol(1, 0, 2, lines)

def test_one_line_no_symbole():
  assert gear_ratios([
    "123"
  ])==0

def test_one_line_one_number_with_adjacent_symbole_right():
  assert gear_ratios([
    "123#"
  ])==123

def test_one_line_one_number_with_adjacent_symbole_left():
  assert gear_ratios([
    "#123"
  ])==123

def test_example():
  assert gear_ratios([
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
  ])==4361

def test_big_example():
  assert gear_ratios(input.splitlines())==538046


