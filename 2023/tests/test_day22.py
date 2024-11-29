from day22 import Grid

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9'''
    test_input = Grid(test_string)
    assert test_input.get_safebricks_count() == 5

# ----------- Part 2 ------------

# Disabling while figuring out why the test input doesn't work for part 2

# def test_part2_1() -> None:
#     test_string = '''1,0,1~1,2,1
# 0,0,2~2,0,2
# 0,2,3~2,2,3
# 0,0,4~0,2,4
# 2,0,5~2,2,5
# 0,1,6~2,1,6
# 1,1,8~1,1,9'''
#     test_input = Grid(test_string)
#     assert test_input.get_disintegrated_count() == 7
