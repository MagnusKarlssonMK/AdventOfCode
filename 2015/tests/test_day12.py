from day12 import JSON

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input_1 = JSON("[1,2,3]")
    assert test_input_1.get_number_sum() == 6
    test_input_2 = JSON('''{"a":2,"b":4}''')
    assert test_input_2.get_number_sum() == 6

def test_part1_2() -> None:
    test_input_1 = JSON("[[[3]]]")
    assert test_input_1.get_number_sum() == 3
    test_input_2 = JSON('''{"a":{"b":4},"c":-1}''')
    assert test_input_2.get_number_sum() == 3

def test_part1_3() -> None:
    test_input_1 = JSON('''{"a":[-1,1]}''')
    assert test_input_1.get_number_sum() == 0
    test_input_2 = JSON('''[-1,{"a":1}]''')
    assert test_input_2.get_number_sum() == 0

def test_part1_4() -> None:
    test_input_1 = JSON("[]")
    assert test_input_1.get_number_sum() == 0
    test_input_2 = JSON("{}")
    assert test_input_2.get_number_sum() == 0

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_input = JSON("[1,2,3]")
    assert test_input.get_number_sum('red') == 6

def test_part2_2() -> None:
    test_input = JSON('''[1,{"c":"red","b":2},3]''')
    assert test_input.get_number_sum('red') == 4

def test_part2_3() -> None:
    test_input = JSON('''{"d":"red","e":[1,2,3,4],"f":5}''')
    assert test_input.get_number_sum('red') == 0

def test_part2_4() -> None:
    test_input = JSON('''[1,"red",5]''')
    assert test_input.get_number_sum('red') == 6
