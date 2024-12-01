from day01 import Locations

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''3   4
4   3
2   5
1   3
3   9
3   3'''
    test_input = Locations(test_string)
    assert test_input.get_total_distance() == 11

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''3   4
4   3
2   5
1   3
3   9
3   3'''
    test_input = Locations(test_string)
    assert test_input.get_similarity_score() == 31
