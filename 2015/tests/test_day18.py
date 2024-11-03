from day18 import Grid

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''.#.#.#
...##.
#....#
..#...
#.#..#
####..'''
    test_input = Grid(test_string)
    assert test_input.get_lights_after_steps(False, 4) == 4

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''##.#.#
...##.
#....#
..#...
#.#..#
####.#'''
    test_input = Grid(test_string)
    assert test_input.get_lights_after_steps(True, 5) == 17
