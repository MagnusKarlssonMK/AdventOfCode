from day02 import Spreadsheet

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''5 1 9 5
7 5 3
2 4 6 8'''
    test_input = Spreadsheet(test_string)
    assert test_input.get_checksum() == 18

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''5 9 2 8
9 4 7 3
3 8 6 5'''
    test_input = Spreadsheet(test_string)
    assert test_input.get_checksum(True) == 9
