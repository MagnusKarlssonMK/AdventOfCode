from day10 import Maze

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''.....
.S-7.
.|.|.
.L-J.
.....'''
    test_input = Maze(test_string)
    assert test_input.get_farpoint_length() == 4

def test_part1_2() -> None:
    test_string = '''..F7.
.FJ|.
SJ.L7
|F--J
LJ...'''
    test_input = Maze(test_string)
    assert test_input.get_farpoint_length() == 8

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........'''
    test_input = Maze(test_string)
    assert test_input.get_enclosed_count() == 4

def test_part2_2() -> None:
    test_string = '''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''
    test_input = Maze(test_string)
    assert test_input.get_enclosed_count() == 8

def test_part2_3() -> None:
    test_string = '''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L'''
    test_input = Maze(test_string)
    assert test_input.get_enclosed_count() == 10
