from day02 import PresentList

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = PresentList("2x3x4")
    assert test_input.get_paper_total() == 58

def test_part1_2() -> None:
    test_input = PresentList("1x1x10")
    assert test_input.get_paper_total() == 43

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = PresentList("2x3x4")
    assert test_input.get_ribbon_total() == 34

def test_part2_2() -> None:
    test_input = PresentList("1x1x10")
    assert test_input.get_ribbon_total() == 14
