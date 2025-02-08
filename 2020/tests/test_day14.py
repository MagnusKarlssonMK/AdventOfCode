from day14 import Computer

TEST_DATA_1 = '''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0'''

TEST_DATA_2 = '''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1'''

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Computer(TEST_DATA_1)
    assert test_input.get_memorysum() == 165

# ----------- Part 2 ------------
def test_part2_1() -> None:
    test_input = Computer(TEST_DATA_2)
    assert test_input.get_memorysum_v2() == 208
