"""
Represents the grid as a binary bitmask, and pre-configures the neighbor graph also in the form of bitmasks, one set
of neighbor masks (current, inner and outer level) for each bit in the grid.
For future cleanup: I started out the parsing and neighbor relation mapping aiming to do it dynamically based on the
size of the input, but when filling in the bits for other levels for part 2 I just assumed a 5x5 grid.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day24.txt')


class Eris:
    def __init__(self, rawstr: str) -> None:
        lines = rawstr.splitlines()
        cols = len(lines[0])
        self.__startbugs = ''.join(['1' if c == '#' else '0' for line in lines for c in line])
        self.__neighbormasks: dict[int: set[tuple[int, str]]] = {}  # bit: relative level, mask
        for i, c in enumerate(self.__startbugs):
            mask = ['0' for _ in enumerate(self.__startbugs)]
            outermask = ['0' for _ in enumerate(self.__startbugs)]
            innermask = ['0' for _ in enumerate(self.__startbugs)]
            # Left
            if i % cols != 0:
                mask[i - 1] = '1'
                if i - 1 == 12:
                    innermask[4] = innermask[9] = innermask[14] = innermask[19] = innermask[24] = '1'
            else:
                outermask[11] = '1'
            # Right
            if i % cols != cols - 1:
                mask[i + 1] = '1'
                if i + 1 == 12:
                    innermask[0] = innermask[5] = innermask[10] = innermask[15] = innermask[20] = '1'
            else:
                outermask[13] = '1'
            # Up
            if i >= cols:
                mask[i - cols] = '1'
                if i - cols == 12:
                    innermask[20] = innermask[21] = innermask[22] = innermask[23] = innermask[24] = '1'
            else:
                outermask[7] = '1'
            # Down
            if i < len(self.__startbugs) - cols:
                mask[i + cols] = '1'
                if i + cols == 12:
                    innermask[0] = innermask[1] = innermask[2] = innermask[3] = innermask[4] = '1'
            else:
                outermask[17] = '1'
            self.__neighbormasks[i] = {(0, ''.join(mask))}
            if outermask.count('1') > 0:
                self.__neighbormasks[i].add((-1, ''.join(outermask)))
            if innermask.count('1') > 0:
                self.__neighbormasks[i].add((1, ''.join(innermask)))

    def get_first_repetition_diveristy(self) -> int:
        current = self.__startbugs
        seen = {current}
        minutes = 0
        while True:
            nextminute = ''
            minutes += 1
            for i, c in enumerate(current):
                for level, mask in self.__neighbormasks[i]:
                    if level != 0:
                        continue
                    neighbors = bin(int(mask, 2) & int(current, 2)).count('1')
                    if (c == '1' and neighbors == 1) or (c == '0' and 1 <= neighbors <= 2):
                        nextminute += '1'
                    else:
                        nextminute += '0'
            if nextminute not in seen:
                seen.add(nextminute)
            else:
                return int(nextminute[::-1], 2)
            current = nextminute

    def get_recursive_bugs_count(self, minutes: int = 200) -> int:
        current = {0: self.__startbugs}
        empty = ''.join(['0' for _ in range(len(self.__startbugs))])
        upper = lower = 0
        for t in range(minutes):
            # Add outer levels in both directions if current outer is not empty
            if current[upper] != empty:
                upper += 1
                current[upper] = empty
            if current[lower] != empty:
                lower -= 1
                current[lower] = empty
            nextminute = {}

            for level in current:
                nextminute[level] = ''
                for i, c in enumerate(current[level]):
                    if i == 12:
                        nextminute[level] += '0'
                        continue
                    neighbors = 0
                    for d_level, mask in self.__neighbormasks[i]:
                        if level + d_level in current:
                            neighbors += bin(int(mask, 2) & int(current[level + d_level], 2)).count('1')
                    if (c == '1' and neighbors == 1) or (c == '0' and 1 <= neighbors <= 2):
                        nextminute[level] += '1'
                    else:
                        nextminute[level] += '0'
            current = nextminute
        return sum([level.count('1') for level in current.values()])


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        eris = Eris(file.read().strip('\n'))
    print(f"Part 1: {eris.get_first_repetition_diveristy()}")
    print(f"Part 2: {eris.get_recursive_bugs_count()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
