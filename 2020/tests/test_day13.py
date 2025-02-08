from day13 import BusSchedule

TEST_DATA_1 = '''939
7,13,x,x,59,x,31,19'''

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = BusSchedule(TEST_DATA_1)
    assert test_input.get_minwaitscore() == 295

# ----------- Part 2 ------------
def test_part2_1() -> None:
    test_input = BusSchedule(TEST_DATA_1)
    assert test_input.get_contesttimestamp() == 1068781
