from day02 import Warehouse

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Warehouse("abcdef\nbababc\nabbcde\nabcccd\naabcdd\nabcdee\nababab")
    assert test_input.get_checksum() == 12

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = Warehouse("abcde\nfghij\nklmno\npqrst\nfguij\naxcye\nwvxyz")
    assert test_input.get_common_letters() == "fgij"
