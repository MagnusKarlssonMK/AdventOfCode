from day10 import Map

# ----------- Parts 1 & 2 ------------

def test_parts1_2_1() -> None:
    test_string = '''0123
1234
8765
9876'''
    test_input = Map(test_string)
    p1, _ = test_input.get_score_and_rating()
    assert p1 == 1

def test_parts1_2_2() -> None:
    test_string = '''89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732'''
    test_input = Map(test_string)
    p1, p2 = test_input.get_score_and_rating()
    assert p1 == 36
    assert p2 == 81
