"""
Basically a brute-force solution, gets part 2 done in a second or so.
There are some fancier solutions out there, I might return to check those out some rainy day...
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2016/day16.txt')


def dragon_curve(a: str) -> str:
    b = ''.join(['1' if c == '0' else '0' for c in reversed(a)])
    return a + '0' + b


def checksum(a: str) -> str:
    if len(a) % 2 != 0:
        return a
    else:
        b = ''
        for i in range(0, len(a), 2):
            if a[i] == a[i + 1]:
                b += '1'
            else:
                b += '0'
        return checksum(b)


class Disk:
    def __init__(self, rawstr: str) -> None:
        self.__startdata = rawstr

    def get_checksum(self, disksize: int) -> str:
        data = self.__startdata
        while len(data) < disksize:
            data = dragon_curve(data)
        return checksum(data[0: disksize])


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        disk = Disk(file.read().strip('\n'))
    print(f"Part 1: {disk.get_checksum(272)}")
    print(f"Part 2: {disk.get_checksum(35651584)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
