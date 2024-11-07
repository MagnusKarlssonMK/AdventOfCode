from day01 import Device

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Device("+1\n-2\n+3\n+1")
    assert test_input.get_frequency() == 3

def test_part1_2() -> None:
    test_input = Device("+1\n+1\n+1")
    assert test_input.get_frequency() == 3

def test_part1_3() -> None:
    test_input = Device("+1\n+1\n-2")
    assert test_input.get_frequency() == 0

def test_part1_4() -> None:
    test_input = Device("-1\n-2\n-3")
    assert test_input.get_frequency() == -6

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = Device("+1\n-2\n+3\n+1")
    assert test_input.get_calibration_value() == 2

def test_part2_2() -> None:
    test_input = Device("+1\n-1")
    assert test_input.get_calibration_value() == 0

def test_part2_3() -> None:
    test_input = Device("+3\n+3\n+4\n-2\n-4")
    assert test_input.get_calibration_value() == 10

def test_part2_4() -> None:
    test_input = Device("-6\n+3\n+8\n+5\n-6")
    assert test_input.get_calibration_value() == 5

def test_part2_5() -> None:
    test_input = Device("+7\n+7\n-2\n-7\n-4")
    assert test_input.get_calibration_value() == 14
