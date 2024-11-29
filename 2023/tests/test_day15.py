from day15 import Lightmachine

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''
    test_input = Lightmachine(test_string)
    assert test_input.get_initialization_sum() == 1320

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'''
    test_input = Lightmachine(test_string)
    assert test_input.get_lenspower() == 145
