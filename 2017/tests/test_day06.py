from day06 import Memory

# ----------- Part 1 & 2 ------------

def test_part12_1() -> None:
    test_input = Memory("0 2 7 0")
    assert test_input.get_cycles_count() == 5
    assert test_input.get_cycles_count() == 4
