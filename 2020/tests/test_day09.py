from day09 import XMAS

TEST_DATA_1 = '''35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576'''

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = XMAS(TEST_DATA_1)
    assert test_input.get_invalid_nbr() == 127
# ----------- Part 2 ------------
    assert test_input.get_encryption_weakness() == 62
