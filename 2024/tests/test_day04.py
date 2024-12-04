from day04 import WordSearch

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX'''
    test_input = WordSearch(test_string)
    assert test_input.get_xmas() == 18

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX'''
    test_input = WordSearch(test_string)
    assert test_input.get_x_mas() == 9
