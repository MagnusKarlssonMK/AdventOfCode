from day03 import InputData


TEST_DATA = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

# Home made test to cover items in the rightmost column
TEST_DATA_CUSTOM = """.23+..4.
.......*
11.....7
*.5..+..
3..2..*6"""

# ----------- Part 1 ------------


def test_part1_1() -> None:
    test_input = InputData(TEST_DATA)
    assert test_input.solve_part1() == 4361


def test_part1_2() -> None:
    test_input = InputData(TEST_DATA_CUSTOM)
    assert test_input.solve_part1() == 54


# ----------- Part 2 ------------


def test_part2_1() -> None:
    test_input = InputData(TEST_DATA)
    assert test_input.solve_part2() == 467835


def test_part2_2() -> None:
    test_input = InputData(TEST_DATA_CUSTOM)
    assert test_input.solve_part2() == 61
