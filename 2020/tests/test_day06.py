from day06 import Forms

TEST_DATA_1 = '''abcx\nabcy\nabcz'''
TEST_DATA_2 = '''abc\n
a\nb\nc\n
ab\nac\n
a\na\na\na\n
b'''

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Forms(TEST_DATA_1)
    assert test_input.get_yes_count() == 6

def test_part1_2() -> None:
    test_input = Forms(TEST_DATA_2)
    assert test_input.get_yes_count() == 11

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_data = "BBFFBBFRLL"
    test_input = Forms(TEST_DATA_2)
    assert test_input.get_yes_count(True) == 6
