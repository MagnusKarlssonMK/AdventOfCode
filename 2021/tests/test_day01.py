from day01 import Report

# ----------- Part 1 ------------

def test_part1_1() -> None:
    teststring = '''199
200
208
210
200
207
240
269
260
263'''
    test_input = Report(teststring)
    assert test_input.count_depth_increase(1) == 7

# ----------- Part 2 ------------

def test_part2_1() -> None:
    teststring = '''199
200
208
210
200
207
240
269
260
263'''
    test_input = Report(teststring)
    assert test_input.count_depth_increase(3) == 5
