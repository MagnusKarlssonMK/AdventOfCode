from day10 import LookAndSay

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = LookAndSay("1")
    assert test_input.get_generated_length(1) == 2

def test_part1_2() -> None:
    test_input = LookAndSay("11")
    assert test_input.get_generated_length(1) == 2

def test_part1_3() -> None:
    test_input = LookAndSay("21")
    assert test_input.get_generated_length(1) == 4

def test_part1_4() -> None:
    test_input = LookAndSay("1211")
    assert test_input.get_generated_length(1) == 6

def test_part1_5() -> None:
    test_input = LookAndSay("111221")
    assert test_input.get_generated_length(1) == 6

# No additional tests for part 2 - rules doesn't change, only patience...
