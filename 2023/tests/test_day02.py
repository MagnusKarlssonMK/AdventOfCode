from day02 import InputData


TEST_DATA = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


# ----------- Part 1 ------------


def test_part1_1() -> None:
    test_input = InputData(TEST_DATA)
    assert test_input.solve_part1() == 8


# ----------- Part 2 ------------


def test_part2_1() -> None:
    test_input = InputData(TEST_DATA)
    assert test_input.solve_part2() == 2286
