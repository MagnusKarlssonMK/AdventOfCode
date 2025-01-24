from day11 import WaitingArea

TEST_DATA_1 = '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL'''

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = WaitingArea(TEST_DATA_1)
    assert test_input.get_steadystate_occupied() == 37

# ----------- Part 2 ------------
def test_part2_1() -> None:
    test_input = WaitingArea(TEST_DATA_1)
    assert test_input.get_steadystate_occupied(True) == 26
