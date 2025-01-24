from day10 import Device

TEST_DATA_1 = '''16
10
15
5
1
11
7
19
6
12
4'''

TEST_DATA_2 = '''28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3'''

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = Device(TEST_DATA_1)
    assert test_input.get_jolt_differences() == 7*5

def test_part1_2() -> None:
    test_input = Device(TEST_DATA_2)
    assert test_input.get_jolt_differences() == 22*10

# ----------- Part 2 ------------
def test_part2_1() -> None:
    test_input = Device(TEST_DATA_1)
    assert test_input.get_nbr_adapter_arrangements() == 8

def test_part2_2() -> None:
    test_input = Device(TEST_DATA_2)
    assert test_input.get_nbr_adapter_arrangements() == 19208
