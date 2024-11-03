from day19 import NuclearPlant

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''H => HO
H => OH
O => HH

HOH'''
    test_input = NuclearPlant(test_string)
    assert test_input.get_molecule_count() == 4

def test_part1_2() -> None:
    test_string = '''H => HO
H => OH
O => HH

HOHOHO'''
    test_input = NuclearPlant(test_string)
    assert test_input.get_molecule_count() == 7

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''e => H
e => O
H => HO
H => OH
O => HH

HOH'''
    test_input = NuclearPlant(test_string)
    assert test_input.get_min_generation_time() == 3

def test_part2_2() -> None:
    test_string = '''e => H
e => O
H => HO
H => OH
O => HH

HOHOHO'''
    test_input = NuclearPlant(test_string)
    assert test_input.get_min_generation_time() == 6
