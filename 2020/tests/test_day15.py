from day15 import MemoryGame

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = MemoryGame("0,3,6")
    assert test_input.playrounds(2020) == 436

def test_part1_2() -> None:
    test_input = MemoryGame("1,3,2")
    assert test_input.playrounds(2020) == 1

def test_part1_3() -> None:
    test_input = MemoryGame("2,1,3")
    assert test_input.playrounds(2020) == 10

def test_part1_4() -> None:
    test_input = MemoryGame("1,2,3")
    assert test_input.playrounds(2020) == 27

def test_part1_5() -> None:
    test_input = MemoryGame("2,3,1")
    assert test_input.playrounds(2020) == 78

def test_part1_6() -> None:
    test_input = MemoryGame("3,2,1")
    assert test_input.playrounds(2020) == 438

def test_part1_7() -> None:
    test_input = MemoryGame("3,1,2")
    assert test_input.playrounds(2020) == 1836

# Part 2 too slow to test, is anyway just the same function with more iterations.
