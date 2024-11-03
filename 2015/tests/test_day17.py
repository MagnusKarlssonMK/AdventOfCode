from day17 import ContainerList

# ----------- Part 1 & 2 ------------

def test_part12_1() -> None:
    test_string = '''20
15
10
5
5'''
    test_input = ContainerList(test_string)
    assert test_input.get_combination_count(25) == 4
    assert test_input.get_min_combination_count() == 3
