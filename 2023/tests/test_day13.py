from day13 import PatternList

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''
    test_input = PatternList(test_string)
    assert test_input.get_totalscore() == 405

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''
    test_input = PatternList(test_string)
    assert test_input.get_totalscore(False) == 400
