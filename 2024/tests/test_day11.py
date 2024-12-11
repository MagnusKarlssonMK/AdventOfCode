from day11 import Stones

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''0 1 10 99 999'''
    test_input = Stones(test_string)
    p1, _ = test_input.get_stone_count(1, 2)
    assert p1 == 7

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''125 17'''
    test_input = Stones(test_string)
    p1, p2 = test_input.get_stone_count(6, 25)
    assert p1 == 22
    assert p2 == 55312
