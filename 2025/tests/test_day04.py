from day04 import InputData

TEST_STRING = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

# ----------- Part 1 ------------


def test_part1_1() -> None:
    test_input = InputData(TEST_STRING)
    assert test_input.get_p1() == 13


# ----------- Part 2 ------------


def test_part2_1() -> None:
    test_input = InputData(TEST_STRING)
    assert test_input.get_p2() == 43
