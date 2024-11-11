from day06 import Fishies

# ----------- Part 1 & 2 ------------

def test_part12_1() -> None:
    test_input = Fishies("3,4,3,1,2")
    p1, p2 = test_input.get_answers()
    assert p1 == 5934
    assert p2 == 26984457539

def test_part1_2() -> None:
    test_input = Fishies("3,4,3,1,2")
    p1, _ = test_input.get_answers(18)
    assert p1 == 26
