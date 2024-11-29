from day02 import Database

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc'''
    test_input = Database(test_string)
    assert test_input.get_valid_passwords_count() == 2

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc'''
    test_input = Database(test_string)
    assert test_input.get_valid_passwords_count(True) == 1
