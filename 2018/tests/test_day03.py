from day03 import Fabric

TEST_STRING_1 = '''#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2'''

# ----------- Parts 1 & 2 ------------

def test_part1_1() -> None:
    test_input = Fabric(TEST_STRING_1)
    p1, p2 = test_input.get_overlap_and_id()
    assert p1 == 4
    assert p2 == 3
