from day08 import CPU

# ----------- Part 1 ------------

def test_parts1_2_1() -> None:
    test_string = '''b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10'''
    test_input = CPU(test_string)
    p1, p2 = test_input.get_largest_reg_value()
    assert p1 == 1
    assert p2 == 10
