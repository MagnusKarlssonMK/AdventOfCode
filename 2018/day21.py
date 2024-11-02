"""
Like day 19, we now need to disassemble the program even further.
Again, trying to extract the data from the input file, but there is no guarantee that it will work without
modifications for other inputs too if there are shifts in the program lines.
"""
import time
from pathlib import Path


class ActivationSystem:
    def __init__(self, rawstr: str) -> None:
        lines = rawstr.splitlines()
        self.__program = [(r, int(a), int(b), int(c)) for r, a, b, c in
                          [line.split() for line in lines[1:]]]
        self.__ipreg = int(lines[0].split()[1])

    def get_lower_bound(self, startval: int = 0) -> int:
        v1 = self.__program[7][1]
        v2 = self.__program[11][2]
        v3 = startval | self.__program[6][2]
        result = v1
        while v3 != 0:
            result += v3 & self.__program[8][2]
            result &= self.__program[10][2]
            result *= v2
            result &= self.__program[12][2]
            v3 //= self.__program[19][2]
        return result

    def get_upper_bound(self) -> int:
        startval = 0
        count = 0
        result = {}
        while True:
            count += (startval << 8) + (startval << 16)
            startval = self.get_lower_bound(startval)
            if startval in result:
                return max(result, key=result.get)
            result[startval] = count


def main(aoc_input: str) -> None:
    system = ActivationSystem(aoc_input)
    print(f"Part 1: {system.get_lower_bound()}")
    print(f"Part 2: {system.get_upper_bound()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day21.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
