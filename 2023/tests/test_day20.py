from day20 import CommunicationSystem

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_string = '''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''
    test_input = CommunicationSystem(test_string)
    assert test_input.get_push_1000() == 32000000

def test_part1_2() -> None:
    test_string = '''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''
    test_input = CommunicationSystem(test_string)
    assert test_input.get_push_1000() == 11687500

# No test input given for part 2
