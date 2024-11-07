from day01 import ExpenseReport

# ----------- Part 1 ------------

def test_part1_1() -> None:
    teststring = '''1721
979
366
299
675
1456'''
    test_input = ExpenseReport(teststring)
    assert test_input.get_2020_pair() == 514579

# ----------- Part 2 ------------

def test_part2_1() -> None:
    teststring = '''1721
979
366
299
675
1456'''
    test_input = ExpenseReport(teststring)
    assert test_input.get_2020_triplet() == 241861950
