from day02 import Warehouse

TEST_STRING_1 = '''abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab'''

TEST_STRING_2 = '''abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz'''

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Warehouse(TEST_STRING_1)
    assert test_input.get_checksum() == 12

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = Warehouse(TEST_STRING_2)
    assert test_input.get_common_letters() == "fgij"
