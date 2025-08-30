from day14 import ReflectorDish


TEST_DATA = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = ReflectorDish(TEST_DATA)
    assert test_input.get_part_1() == 136

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = ReflectorDish(TEST_DATA)
    assert test_input.get_part_2() == 64
