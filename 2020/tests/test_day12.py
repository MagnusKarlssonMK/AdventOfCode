from day12 import Ship

TEST_DATA_1 = '''F10
N3
F7
R90
F11'''

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Ship(TEST_DATA_1)
    assert test_input.get_distance() == 25

# ----------- Part 2 ------------
def test_part2_1() -> None:
    test_input = Ship(TEST_DATA_1)
    assert test_input.get_distance(True) == 286
