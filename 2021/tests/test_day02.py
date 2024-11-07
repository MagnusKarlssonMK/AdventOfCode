from day02 import Submarine

# ----------- Part 1 ------------

def test_part1_1() -> None:
    teststring = '''forward 5
down 5
forward 8
up 3
down 8
forward 2'''
    test_input = Submarine(teststring)
    assert test_input.get_move_result() == 150

# ----------- Part 2 ------------

def test_part2_1() -> None:
    teststring = '''forward 5
down 5
forward 8
up 3
down 8
forward 2'''
    test_input = Submarine(teststring)
    assert test_input.get_aimed_move_result() == 900
