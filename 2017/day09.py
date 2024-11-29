"""
"""
import time
from pathlib import Path


class Stream:
    def __init__(self, rawstr: str) -> None:
        self.__s = rawstr

    def get_score_and_garbage(self) -> tuple[int, int]:
        i = 0
        garbage_count = 0
        score = 0
        level = 1
        while i < len(self.__s):
            match self.__s[i]:
                case "<":
                    i += 1
                    while i < len(self.__s):
                        match self.__s[i]:
                            case "!":
                                i += 1
                            case ">":
                                break
                            case _:
                                garbage_count += 1
                        i += 1
                case "{":
                    score += level
                    level += 1
                case "}":
                    level -= 1
            i += 1
        return score, garbage_count


def main(aoc_input: str) -> None:
    stream = Stream(aoc_input)
    p1, p2 = stream.get_score_and_garbage()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day09.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
