from day02 import Reports

# ----------- Parts 1 & 2 ------------

def test_part1_1() -> None:
    test_string = '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9'''
    test_input = Reports(test_string)
    p1, p2 = test_input.get_safe_reports()
    assert p1 == 2
    assert p2 == 4
