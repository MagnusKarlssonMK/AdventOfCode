from day02 import InputData

TEST_STRING = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"""

# ----------- Part 1 ------------


def test_part1_1() -> None:
    test_input = InputData(TEST_STRING)
    assert test_input.get_p1() == 1227775554


# ----------- Part 2 ------------


def test_part2_1() -> None:
    test_input = InputData(TEST_STRING)
    assert test_input.get_p2() == 4174379265
