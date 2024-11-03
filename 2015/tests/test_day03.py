from day03 import Santa

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Santa(">")
    assert test_input.get_uniquehouses_count() == 2

def test_part1_2() -> None:
    test_input = Santa("^>v<")
    assert test_input.get_uniquehouses_count() == 4

def test_part1_3() -> None:
    test_input = Santa("^v^v^v^v^v")
    assert test_input.get_uniquehouses_count() == 2

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = Santa("^v")
    assert test_input.get_uniquehouses_count(True) == 3

def test_part2_2() -> None:
    test_input = Santa("^>v<")
    assert test_input.get_uniquehouses_count(True) == 3

def test_part2_3() -> None:
    test_input = Santa("^v^v^v^v^v")
    assert test_input.get_uniquehouses_count(True) == 11
