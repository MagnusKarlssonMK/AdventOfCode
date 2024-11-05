from day04 import PassphraseList

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = PassphraseList("aa bb cc dd ee")
    assert test_input.get_valid_count() == 1

def test_part1_2() -> None:
    test_input = PassphraseList("aa bb cc dd aa")
    assert test_input.get_valid_count() == 0

def test_part1_3() -> None:
    test_input = PassphraseList("aa bb cc dd aaa")
    assert test_input.get_valid_count() == 1

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = PassphraseList("abcde fghij")
    assert test_input.get_valid_count(True) == 1

def test_part2_2() -> None:
    test_input = PassphraseList("abcde xyz ecdab")
    assert test_input.get_valid_count(True) == 0

def test_part2_3() -> None:
    test_input = PassphraseList("a ab abc abd abf abj")
    assert test_input.get_valid_count(True) == 1

def test_part2_4() -> None:
    test_input = PassphraseList("iiii oiii ooii oooi oooo")
    assert test_input.get_valid_count(True) == 1

def test_part2_5() -> None:
    test_input = PassphraseList("oiii ioii iioi iiio")
    assert test_input.get_valid_count(True) == 0
