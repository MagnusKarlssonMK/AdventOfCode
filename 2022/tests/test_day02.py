from day02 import StrategyBook

# ----------- Part 1 ------------

def test_part1_1() -> None:
    teststring = '''A Y
B X
C Z'''
    test_input = StrategyBook(teststring)
    assert test_input.get_assumed_total_score() == 15

# ----------- Part 2 ------------

def test_part2_1() -> None:
    teststring = '''A Y
B X
C Z'''
    test_input = StrategyBook(teststring)
    assert test_input.get_correct_total_score() == 12
