from day09 import get_numbers

# ----------- Part 1 & 2------------


def test_part12_1() -> None:
    test_string = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    p1, p2 = get_numbers(test_string)
    assert p1 == 114
    assert p2 == 2
