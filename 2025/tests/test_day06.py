from day06 import InputData

TEST_STRING = """123 328  51 64 \n 45 64  387 23 \n  6 98  215 314\n*   +   *   +  """

# ----------- Part 1 ------------


def test_part1_1() -> None:
    test_input = InputData(TEST_STRING)
    assert test_input.get_p1() == 4277556


# ----------- Part 2 ------------


def test_part2_1() -> None:
    test_input = InputData(TEST_STRING)
    assert test_input.get_p2() == 3263827
