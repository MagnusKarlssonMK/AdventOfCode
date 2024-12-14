from day12 import Garden

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''AAAA
BBCD
BBCC
EEEC'''
    test_input = Garden(test_string)
    p1, _ = test_input.get_costs()
    assert p1 == 140

def test_part1_2() -> None:
    test_string = '''OOOOO
OXOXO
OOOOO
OXOXO
OOOOO'''
    test_input = Garden(test_string)
    p1, _ = test_input.get_costs()
    assert p1 == 772

def test_part1_3() -> None:
    test_string = '''RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE'''
    test_input = Garden(test_string)
    p1, _ = test_input.get_costs()
    assert p1 == 1930

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''AAAA
BBCD
BBCC
EEEC'''
    test_input = Garden(test_string)
    _, p2 = test_input.get_costs()
    assert p2 == 80

def test_part2_2() -> None:
    test_string = '''EEEEE
EXXXX
EEEEE
EXXXX
EEEEE'''
    test_input = Garden(test_string)
    _, p2 = test_input.get_costs()
    assert p2 == 236

def test_part2_3() -> None:
    test_string = '''AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA'''
    test_input = Garden(test_string)
    _, p2 = test_input.get_costs()
    assert p2 == 368
