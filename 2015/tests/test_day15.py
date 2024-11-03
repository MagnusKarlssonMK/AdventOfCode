from day15 import Kitchen

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'''
    test_input = Kitchen(test_string)
    assert test_input.get_top_score() == 62842880

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'''
    test_input = Kitchen(test_string)
    assert test_input.get_top_score(True) == 57600000
