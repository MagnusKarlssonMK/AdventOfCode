from day07 import Tower

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)'''
    test_input = Tower(test_string)
    assert test_input.get_bottom_program_name() == "tknk"

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)'''
    test_input = Tower(test_string)
    assert test_input.get_correct_weight() == 60
