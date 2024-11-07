from day04 import Assignments

# ----------- Part 1 ------------

def test_part1_1() -> None:
    teststring = '''2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8'''
    test_input = Assignments(teststring)
    assert test_input.get_assignments_contained() == 2

# ----------- Part 2 ------------

def test_part2_1() -> None:
    teststring = '''2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8'''
    test_input = Assignments(teststring)
    assert test_input.get_assignments_overlap() == 4
