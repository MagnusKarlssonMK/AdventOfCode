from day03 import Memory

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Memory(1)
    assert test_input.get_manhattan_distance() == 0

def test_part1_2() -> None:
    test_input = Memory(12)
    assert test_input.get_manhattan_distance() == 3

def test_part1_3() -> None:
    test_input = Memory(23)
    assert test_input.get_manhattan_distance() == 2

def test_part1_4() -> None:
    test_input = Memory(1024)
    assert test_input.get_manhattan_distance() == 31

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = Memory(750)
    assert test_input.get_larger_number() == 806
