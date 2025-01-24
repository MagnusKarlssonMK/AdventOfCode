from day08 import Console

TEST_DATA_1 = '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6'''

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Console(TEST_DATA_1)
    assert test_input.get_boot_accumulator_value() == 5

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = Console(TEST_DATA_1)
    assert test_input.repair() == 8
