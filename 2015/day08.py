"""
Trying to avoid using literal eval.
So pretty much scan the lines for special characters and;
- For part 1, count number of positions that does not represent an actual character.
- For part 2, count the characters that needs to be escaped.
"""
import time
from pathlib import Path


class SantaList:
    def __init__(self, rawstr: str) -> None:
        self.__literals = rawstr.splitlines()

    def get_unchar_count(self) -> int:
        count = 0
        for line in self.__literals:
            count += 2  # Add 2 for the surrounding double quotes
            i = 1
            while i < len(line) - 1:
                if line[i] == '\\':
                    if line[i + 1] == '\"' or line[i + 1] == '\\':
                        count += 1
                        i += 1
                    elif line[i + 1] == 'x':
                        count += 3
                        i += 3
                i += 1
        return count

    def get_encoded_diff(self) -> int:
        count = 0
        for line in self.__literals:
            count += 2  # Surrounding double quotes will expand by one character each
            for c in line:
                if c == '\"' or c == '\\':
                    count += 1
        return count


def main(aoc_input: str) -> None:
    santalist = SantaList(aoc_input)
    print(f"Part 1: {santalist.get_unchar_count()}")
    print(f"Part 2: {santalist.get_encoded_diff()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day08.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
