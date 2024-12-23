from day03 import Schematic

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''
    test_input = Schematic(test_string)
    assert test_input.get_partnumber_sum() == 4361

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''
    test_input = Schematic(test_string)
    assert test_input.get_gearratio_sum() == 467835
