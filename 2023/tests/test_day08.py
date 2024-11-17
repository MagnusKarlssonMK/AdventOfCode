from day08 import NodeNetwork

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)'''
    test_input = NodeNetwork(test_string)
    assert test_input.stepcount_zzz() == 2

def test_part1_2() -> None:
    test_string = '''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''
    test_input = NodeNetwork(test_string)
    assert test_input.stepcount_zzz() == 6

# ----------- Part 2 ------------

def test_part2_1() -> None:
    test_string = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''
    test_input = NodeNetwork(test_string)
    assert test_input.stepcount_atoz() == 6
