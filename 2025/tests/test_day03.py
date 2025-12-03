from day03 import InputData

TEST_STRING = """987654321111111
811111111111119
234234234234278
818181911112111"""

# ----------- Part 1 ------------


def test_part1_1() -> None:
    test_input = InputData(TEST_STRING)
    assert test_input.get_p1() == 357


# ----------- Part 2 ------------


def test_part2_1() -> None:
    test_input = InputData(TEST_STRING)
    assert test_input.get_p2() == 3121910778619
