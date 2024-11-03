from day01 import Directions

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input_1 = Directions("(())")
    test_input_2 = Directions("()()")
    assert test_input_1.get_final_floor() == 0 and test_input_2.get_final_floor() == 0

def test_part1_2() -> None:
    test_input_1 = Directions("(((")
    test_input_2 = Directions("(()(()(")
    assert test_input_1.get_final_floor() == 3 and test_input_2.get_final_floor() == 3

def test_part1_3() -> None:
    test_input = Directions("))(((((")
    assert test_input.get_final_floor() == 3

def test_part1_4() -> None:
    test_input_1 = Directions("())")
    test_input_2 = Directions("))(")
    assert test_input_1.get_final_floor() == -1 and test_input_2.get_final_floor() == -1

def test_part1_5() -> None:
    test_input_1 = Directions(")))")
    test_input_2 = Directions(")())())")
    assert test_input_1.get_final_floor() == -3 and test_input_2.get_final_floor() == -3

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = Directions(")")
    assert test_input.get_basement_step() == 1

def test_part2_2() -> None:
    test_input = Directions("()())")
    assert test_input.get_basement_step() == 5

# Custom test to cover the case where basement is never reached
def test_part2_3() -> None:
    test_input = Directions("(((")
    assert test_input.get_basement_step() == -1
