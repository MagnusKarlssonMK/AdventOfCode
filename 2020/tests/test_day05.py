from day05 import Scanner

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_data = "BFFFBBFRRR"
    test_input = Scanner(test_data)
    assert test_input.get_highest_seat() == 567

def test_part1_2() -> None:
    test_data = "FFFBBBFRRR"
    test_input = Scanner(test_data)
    assert test_input.get_highest_seat() == 119

def test_part1_3() -> None:
    test_data = "BBFFBBFRLL"
    test_input = Scanner(test_data)
    assert test_input.get_highest_seat() == 820

# ----------- Part 2 ------------
