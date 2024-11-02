"""
Recursive solution to break down the string into smaller parts.
"""
import time
from pathlib import Path


class Stream:
    def __init__(self, rawstr: str) -> None:
        self.__s = rawstr
        self.__garbagecount = 0

    def __get_group_score(self, startidx: int, level: int) -> tuple[int, int]:  # stopidx, score
        i = startidx
        ignored = False
        garbage = False
        score = 0
        while i < len(self.__s):
            if ignored:
                ignored = False
            elif garbage:
                if self.__s[i] == '>':
                    garbage = False
                elif self.__s[i] == '!':
                    ignored = True
                else:
                    self.__garbagecount += 1
            else:
                match self.__s[i]:
                    case '{':
                        i, new_score = self.__get_group_score(i + 1, level + 1)
                        score += new_score
                    case '}':
                        return i, score + level
                    case '<':
                        garbage = True
                    case '!':
                        ignored = True
            i += 1
        return -1, -1

    def get_total_score(self) -> int:
        return self.__get_group_score(1, 1)[1]

    def get_total_garbage(self) -> int:
        return self.__garbagecount


def main(aoc_input: str) -> None:
    stream = Stream(aoc_input)
    print(f"Part 1: {stream.get_total_score()}")
    print(f"Part 2: {stream.get_total_garbage()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day09.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
