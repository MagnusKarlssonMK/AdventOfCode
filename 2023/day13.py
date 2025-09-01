import time
from pathlib import Path


def ismirror(patternlist: list[int], candidate: int, wildcardused: bool) -> bool:
    if candidate >= (len(patternlist) - 1) or candidate < 0:
        return True if wildcardused else False
    elif patternlist[candidate] == patternlist[candidate + 1]:
        newlist = [item for z, item in enumerate(patternlist) if (z < candidate) or z > (candidate + 1)]
        return ismirror(newlist, candidate - 1, wildcardused)
    elif not wildcardused:
        if bin(patternlist[candidate] ^ patternlist[candidate + 1]).count("1") == 1:
            newlist = [item for z, item in enumerate(patternlist) if (z < candidate) or z > (candidate + 1)]
            return ismirror(newlist, candidate - 1, True)
    return False


def getmirrorscore(patternlist: list[int], usewildcard: bool) -> int:
    for index in range(0, len(patternlist) - 1):
        if ismirror(patternlist, index, usewildcard):
            return index + 1
    return 0


class Pattern:
    def __init__(self, rawstr: str) -> None:
        rows: list[str] = []
        self.__binrows: list[int] = []
        self.__bincolumns: list[int] = []
        # Convert input to a string of binary characters '0' and '1'
        for line in rawstr.splitlines():
            convertedstr = ''.join(['0' if c == '.' else '1' for c in line])
            rows.append(convertedstr)
            self.__binrows.append(int(convertedstr, 2))

        for i, _ in enumerate(rows[0]):
            convertedstr = ''.join([r[i] for r in rows])
            self.__bincolumns.append(int(convertedstr, 2))

    def getscore(self, wildcard: bool) -> int:
        retval = 0
        retval += 100 * getmirrorscore(self.__binrows, wildcard)
        retval += getmirrorscore(self.__bincolumns, wildcard)
        return retval


class PatternList:
    def __init__(self, rawstr: str) -> None:
        self.__patterns = [Pattern(block) for block in rawstr.split('\n\n')]

    def get_totalscore(self, wildcardused: bool = True) -> int:
        return sum([p.getscore(wildcardused) for p in self.__patterns])


def main(aoc_input: str) -> None:
    patterns = PatternList(aoc_input)
    print(f"Part 1: {patterns.get_totalscore()}")
    print(f"Part 2: {patterns.get_totalscore(False)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2023/day13.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
