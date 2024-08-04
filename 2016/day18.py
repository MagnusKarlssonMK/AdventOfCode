"""
Super simple, but also not superfast for part 2.
Gets the job done in 5 seconds or so, but I can't help but wonder if there is some hidden trick to optimize it...
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2016/day18.txt')


class TrapRoom:
    __TRAP_MAP = ('^^.', '.^^', '..^', '^..')

    def __init__(self, rawstr: str) -> None:
        self.__startrow = rawstr

    def get_safetile_count(self, rows: int) -> int:
        # Represent safe tiles '.' as 1, trap tiles '^' as 0
        result = 0
        row = '.' + self.__startrow + '.'  # Add padding on the outsides to simplify handling of the edges
        for _ in range(rows):
            result += sum([1 for c in row if c == '.']) - 2  # Subtract 2 for the paddings
            newrow = ''
            for i in range(1, len(row) - 1):
                newrow += '^' if row[i-1: i+2] in TrapRoom.__TRAP_MAP else '.'
            row = '.' + newrow + '.'
        return result


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        room = TrapRoom(file.read().strip('\n'))
    print(f"Part 1: {room.get_safetile_count(40)}")
    print(f"Part 2: {room.get_safetile_count(400000)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
