from day07 import CrabArmy

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = CrabArmy("16,1,2,0,4,2,7,1,2,14")
    assert test_input.get_calibration_cost() == 37

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = CrabArmy("16,1,2,0,4,2,7,1,2,14")
    assert test_input.get_calibration_cost(True) == 168
