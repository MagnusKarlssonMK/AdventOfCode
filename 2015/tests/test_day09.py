from day09 import LocationMap

# ----------- Part 1 & 2 ------------

def test_part12_1() -> None:
    distances = '''London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141'''
    test_input = LocationMap(distances)
    shortest, longest = test_input.get_route_lengths()
    assert shortest == 605
    assert longest == 982
