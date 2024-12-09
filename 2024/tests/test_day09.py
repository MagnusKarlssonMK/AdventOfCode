from day09 import Disk

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''2333133121414131402'''
    test_input = Disk(test_string)
    assert test_input.get_fragmented_checksum() == 1928

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''2333133121414131402'''
    test_input = Disk(test_string)
    assert test_input.get_defragmented_checksum() == 2858
