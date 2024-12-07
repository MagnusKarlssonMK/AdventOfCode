from day_template import Placeholder

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''3   4
4   3
2   5
1   3
3   9
3   3'''
    test_input = Placeholder(test_string)
    assert test_input.get_p1() == 1

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''3   4
4   3
2   5
1   3
3   9
3   3'''
    test_input = Placeholder(test_string)
    assert test_input.get_p2() == 2
