from day18 import Homework

TEST_DATA_1 = "1 + 2 * 3 + 4 * 5 + 6"
TEST_DATA_2 = "1 + (2 * 3) + (4 * (5 + 6))"
TEST_DATA_3 = "2 * 3 + (4 * 5)"
TEST_DATA_4 = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
TEST_DATA_5 = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
TEST_DATA_6 = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Homework(TEST_DATA_1)
    assert test_input.get_value_sum() == 71

def test_part1_2() -> None:
    test_input = Homework(TEST_DATA_2)
    assert test_input.get_value_sum() == 51

def test_part1_3() -> None:
    test_input = Homework(TEST_DATA_3)
    assert test_input.get_value_sum() == 26

def test_part1_4() -> None:
    test_input = Homework(TEST_DATA_4)
    assert test_input.get_value_sum() == 437

def test_part1_5() -> None:
    test_input = Homework(TEST_DATA_5)
    assert test_input.get_value_sum() == 12240

def test_part1_6() -> None:
    test_input = Homework(TEST_DATA_6)
    assert test_input.get_value_sum() == 13632

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = Homework(TEST_DATA_1)
    assert test_input.get_value_sum(True) == 231

def test_part2_2() -> None:
    test_input = Homework(TEST_DATA_2)
    assert test_input.get_value_sum(True) == 51

def test_part2_3() -> None:
    test_input = Homework(TEST_DATA_3)
    assert test_input.get_value_sum(True) == 46

def test_part2_4() -> None:
    test_input = Homework(TEST_DATA_4)
    assert test_input.get_value_sum(True) == 1445

def test_part2_5() -> None:
    test_input = Homework(TEST_DATA_5)
    assert test_input.get_value_sum(True) == 669060

def test_part2_6() -> None:
    test_input = Homework(TEST_DATA_6)
    assert test_input.get_value_sum(True) == 23340
