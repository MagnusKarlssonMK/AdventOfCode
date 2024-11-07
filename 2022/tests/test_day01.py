from day01 import ElfGroup

# ----------- Part 1 ------------

def test_part1_1() -> None:
    teststring = '''1000
2000
3000

4000

5000
6000

7000
8000
9000

10000'''
    test_input = ElfGroup(teststring)
    assert test_input.get_maxcal() == 24000

# ----------- Part 2 ------------

def test_part2_1() -> None:
    teststring = '''1000
2000
3000

4000

5000
6000

7000
8000
9000

10000'''
    test_input = ElfGroup(teststring)
    assert test_input.get_topthree() == 45000
