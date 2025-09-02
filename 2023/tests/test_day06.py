from day06 import InputData


TEST_DATA = """Time:      7  15   30
Distance:  9  40  200"""


# ----------- Part 1 ------------


def test_part1_1() -> None:
    test_input = InputData(TEST_DATA)
    assert test_input.solve_part1() == 288


# ----------- Part 2 ------------


def test_part2_1() -> None:
    test_input = InputData(TEST_DATA)
    assert test_input.solve_part2() == 71503
