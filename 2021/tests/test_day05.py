from day05 import Seabottom

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''0,9 -> 5,9\n8,0 -> 0,8\n9,4 -> 3,4\n2,2 -> 2,1\n7,0 -> 7,4\n6,4 -> 2,0\n0,9 -> 2,9\n3,4 -> 1,4\n0,0 -> 8,8\n5,5 -> 8,2'''
    test_input = Seabottom(test_string)
    assert test_input.get_score() == 5
# ----------- Part 2 ------------
    assert test_input.get_score(True) == 12
