"""
Basically import an MD5 lib and brute force the solution...
Could perhaps shave off some ms by merging p1 and p2 without restarting from zero again, although that will also add
some extra checks to execute in the loop.
"""
import sys
from pathlib import Path
from hashlib import md5

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2015/day04.txt')


class MD5Miner:
    def __init__(self, rawstr: str) -> None:
        self.__inputstr = rawstr

    def get_lowest_nbr(self, nbr_zeroes: int = 5) -> int:
        try_nbr = 0
        while True:
            try_key = md5((self.__inputstr + str(try_nbr)).encode()).hexdigest()[:nbr_zeroes]
            if int(try_key, 16) == 0:
                return try_nbr
            try_nbr += 1


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        miner = MD5Miner(file.read().strip('\n'))
    print(f"Part 1: {miner.get_lowest_nbr()}")
    print(f"Part 2: {miner.get_lowest_nbr(6)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
