from day11 import Hexgrid

# ----------- Parts 1 & 2 ------------

def test_parts1_2_1() -> None:
    test_input = Hexgrid("ne,ne,ne")
    p1, p2 = test_input.get_distance()
    assert p1 == 3
    assert p2 == 3

def test_parts1_2_2() -> None:
    test_input = Hexgrid("ne,ne,sw,sw")
    p1, p2 = test_input.get_distance()
    assert p1 == 0
    assert p2 == 2

def test_parts1_2_3() -> None:
    test_input = Hexgrid("ne,ne,s,s")
    p1, p2 = test_input.get_distance()
    assert p1 == 2
    assert p2 == 2

def test_parts1_2_4() -> None:
    test_input = Hexgrid("se,sw,se,sw,sw")
    p1, p2 = test_input.get_distance()
    assert p1 == 3
    assert p2 == 3
