from day06 import Competition

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''Time:      7  15   30
Distance:  9  40  200'''
    test_input = Competition(test_string)
    assert test_input.get_race_product() == 288

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''Time:      7  15   30
Distance:  9  40  200'''
    test_input = Competition(test_string)
    assert test_input.get_megarace_score() == 71503
