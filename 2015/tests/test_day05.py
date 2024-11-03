from day05 import SantaText

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = SantaText("ugknbfddgicrmopn")
    assert test_input.get_nice_count() == 1

def test_part1_2() -> None:
    test_input = SantaText("aaa")
    assert test_input.get_nice_count() == 1

def test_part1_3() -> None:
    test_input = SantaText("jchzalrnumimnmhp")
    assert test_input.get_nice_count() == 0

def test_part1_4() -> None:
    test_input = SantaText("haegwjzuvuyypxyu")
    assert test_input.get_nice_count() == 0

def test_part1_5() -> None:
    test_input = SantaText("dvszwmarrgswjxmb")
    assert test_input.get_nice_count() == 0

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = SantaText("qjhvhtzxzqqjkmpb")
    assert test_input.get_nice_count(True) == 1

def test_part2_2() -> None:
    test_input = SantaText("xxyxx")
    assert test_input.get_nice_count(True) == 1

def test_part2_3() -> None:
    test_input = SantaText("uurcxstgmygtbstg")
    assert test_input.get_nice_count(True) == 0

def test_part2_4() -> None:
    test_input = SantaText("ieodomkazucvgmuy")
    assert test_input.get_nice_count(True) == 0
