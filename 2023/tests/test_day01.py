from day01 import Document

# ----------- Part 1 ------------

def test_part1_1() -> None:
    teststring = '''1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet'''
    test_input = Document(teststring)
    assert test_input.get_calibration_sum() == 142

# ----------- Part 2 ------------

def test_part2_1() -> None:
    teststring = '''two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen'''
    test_input = Document(teststring)
    assert test_input.get_calibration_sum(True) == 281
