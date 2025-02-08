from day16 import TicketData

TEST_DATA_1 = '''class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12'''

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = TicketData(TEST_DATA_1)
    assert test_input.get_invalidnearby() == 71
    assert test_input.get_departurescore() == 1
    # Not a useful input to test the p2 function, used just to run through the code at least
