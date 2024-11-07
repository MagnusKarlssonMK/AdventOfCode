from day03 import Diagnostics

# ----------- Part 1 ------------

def test_part1_1() -> None:
    teststring = '''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010'''
    test_input = Diagnostics(teststring)
    assert test_input.getpowerconsumption() == 198

# ----------- Part 2 ------------

def test_part2_1() -> None:
    teststring = '''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010'''
    test_input = Diagnostics(teststring)
    assert test_input.getlifesupportrating() == 230
