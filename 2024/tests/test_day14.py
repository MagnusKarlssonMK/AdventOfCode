from day14 import Security

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3'''
    test_input = Security(test_string, 11, 7)
    assert test_input.get_safety_factor() == 12
    assert test_input.get_egg_seconds() == 1
