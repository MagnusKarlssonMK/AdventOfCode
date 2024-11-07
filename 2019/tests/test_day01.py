from day01 import calc_mass

# ----------- Part 1 ------------

def test_part1_1() -> None:
    assert calc_mass(int("12")) == 2
    assert calc_mass(int("14")) == 2
    assert calc_mass(int("1969")) == 654
    assert calc_mass(int("100756")) == 33583

# ----------- Part 2 ------------

def test_part2_1() -> None:
    assert calc_mass(int("14"), True) == 2
    assert calc_mass(int("1969"), True) == 966
    assert calc_mass(int("100756"), True) == 50346
