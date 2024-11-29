from day03 import TreeMap

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#'''
    test_input = TreeMap(test_string)
    assert test_input.get_treecount_simple() == 7

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#'''
    test_input = TreeMap(test_string)
    assert test_input.get_treecount_full() == 336
