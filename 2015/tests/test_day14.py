from day14 import Olympics

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.'''
    test_input = Olympics(test_string)
    assert test_input.get_winner_distance(False, 1000) == 1120

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.'''
    test_input = Olympics(test_string)
    assert test_input.get_winner_distance(True, 1000) == 689
