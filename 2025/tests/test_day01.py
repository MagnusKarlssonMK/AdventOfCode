from day01 import InputData

TEST_STRING = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""

# ----------- Part 1 ------------


def test_part1_1() -> None:
    test_input = InputData(TEST_STRING)
    assert test_input.get_p1() == 3


# ----------- Part 2 ------------


def test_part2_1() -> None:
    test_input = InputData(TEST_STRING)
    assert test_input.get_p2() == 6
