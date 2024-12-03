from day03 import Program

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Program("xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))")
    assert test_input.get_basic_calculation() == 161

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = Program("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))")
    assert test_input.get_accurrate_calculation() == 48
