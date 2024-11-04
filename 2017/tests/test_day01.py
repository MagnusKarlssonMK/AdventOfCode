from day01 import Sequence

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Sequence("1122")
    assert test_input.get_captcha() == 3

def test_part1_2() -> None:
    test_input = Sequence("1111")
    assert test_input.get_captcha() == 4

def test_part1_3() -> None:
    test_input = Sequence("1234")
    assert test_input.get_captcha() == 0

def test_part1_4() -> None:
    test_input = Sequence("91212129")
    assert test_input.get_captcha() == 9

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = Sequence("1212")
    assert test_input.get_captcha(True) == 6

def test_part2_2() -> None:
    test_input = Sequence("1221")
    assert test_input.get_captcha(True) == 0

def test_part2_3() -> None:
    test_input = Sequence("123425")
    assert test_input.get_captcha(True) == 4

def test_part2_4() -> None:
    test_input = Sequence("123123")
    assert test_input.get_captcha(True) == 12

def test_part2_5() -> None:
    test_input = Sequence("12131415")
    assert test_input.get_captcha(True) == 4
