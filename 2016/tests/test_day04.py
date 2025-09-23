from day04 import InputData

# ----------- Part 1 ------------

def test_part1_1() -> None:
    TEST_DATA = '''aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]'''

    test_input = InputData(TEST_DATA)
    p1, _ = test_input.solve()
    assert p1 == 1514
