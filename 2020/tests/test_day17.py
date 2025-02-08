from day17 import ConwayCubes

TEST_DATA_1 = '''.#.
..#
###'''

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = ConwayCubes(TEST_DATA_1)
    assert test_input.get_nbr_active_cubes() == 112

# ----------- Part 2 ------------
def test_part2_1() -> None:
    test_input = ConwayCubes(TEST_DATA_1)
    assert test_input.get_nbr_active_cubes(True) == 848
