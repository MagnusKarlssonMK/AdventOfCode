from day04 import MD5Miner

# ----------- Part 1 ------------

def test_part1_1() -> None:
    test_input = MD5Miner("abcdef")
    assert test_input.get_lowest_nbr() == 609043

def test_part1_2() -> None:
    test_input = MD5Miner("pqrstuv")
    assert test_input.get_lowest_nbr() == 1048970
