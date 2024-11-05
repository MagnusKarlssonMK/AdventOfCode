from day05 import CPU

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''0
3
0
1
-3'''
    test_input = CPU(test_string)
    assert test_input.get_exit_step_count() == 5

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''0
3
0
1
-3'''
    test_input = CPU(test_string)
    assert test_input.get_exit_step_count(True) == 10
