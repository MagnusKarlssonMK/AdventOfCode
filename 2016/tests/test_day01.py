from day01 import WalkingSimulator

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = WalkingSimulator("R2, L3")
    assert test_input.get_shortest_distance() == 5

def test_part1_2() -> None:
    test_input = WalkingSimulator("R2, R2, R2")
    assert test_input.get_shortest_distance() == 2

def test_part1_3() -> None:
    test_input = WalkingSimulator("R5, L5, R5, R3")
    assert test_input.get_shortest_distance() == 12

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = WalkingSimulator("R8, R4, R4, R8")
    assert test_input.get_shortest_distance(True) == 4
