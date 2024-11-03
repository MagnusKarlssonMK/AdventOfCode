from day06 import LightGrid

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = LightGrid("turn on 0,0 through 999,999")
    assert test_input.get_lights_count() == 1000*1000

def test_part1_2() -> None:
    test_input = LightGrid("toggle 0,0 through 999,0")
    assert test_input.get_lights_count() == 1000

def test_part1_3() -> None:
    test_input = LightGrid("turn on 0,0 through 999,999\nturn off 499,499 through 500,500")
    assert test_input.get_lights_count() == 1000*1000 - 4

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = LightGrid("turn on 0,0 through 0,0")
    assert test_input.get_correct_lights_count() == 1

def test_part2_2() -> None:
    test_input = LightGrid("toggle 0,0 through 999,999")
    assert test_input.get_correct_lights_count() == 2000000

# Custom test to cover TURN OFF for part 2
def test_part2_3() -> None:
    test_input = LightGrid("toggle 0,0 through 999,999\nturn off 0,0 through 1,1")
    assert test_input.get_correct_lights_count() == 2000000 - 4
