from day07 import CamelCards

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''
    test_input = CamelCards(test_string)
    assert test_input.get_winnings() == 6440

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''
    test_input = CamelCards(test_string)
    assert test_input.get_winnings(True) == 5905
