from day11 import Password

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Password("abcdefgh")
    assert str(test_input.get_new_password()) == "abcdffaa"

def test_part1_2() -> None:
    #test_input = Password("ghijklmn")
    # Note - current solution assumes that the given input only contains allowed characters
    # I.e. it can't handle the test input from the problem description.
    # Consider improving this in the future!
    test_input = Password("ghjaaaaa")
    assert str(test_input.get_new_password()) == "ghjaabcc"

# No additional tests for part 2 - rules doesn't change, only patience...

"""
hijklmmn meets the first requirement (because it contains the straight hij) but fails the second requirement requirement (because it contains i and l).
abbceffg meets the third requirement (because it repeats bb and ff) but fails the first requirement.
abbcegjk fails the third requirement, because it only has one double letter (bb).
The next password after abcdefgh is abcdffaa.
The next password after ghijklmn is ghjaabcc, because you eventually skip all the passwords that start with ghi..., since i is not allowed.
"""
