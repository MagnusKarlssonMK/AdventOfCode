from day03 import Supplies

# ----------- Part 1 ------------

def test_part1_1() -> None:
    teststring = '''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw'''
    test_input = Supplies(teststring)
    assert test_input.get_total_prio_both_compartments() == 157

# ----------- Part 2 ------------

def test_part2_1() -> None:
    teststring = '''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw'''
    test_input = Supplies(teststring)
    assert test_input.get_total_prio_group() == 70
