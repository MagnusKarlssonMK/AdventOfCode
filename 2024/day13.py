import time
from pathlib import Path
import re


class Machine:
    def __init__(self, rawstr: str):
        lines = rawstr.splitlines()
        self.__a = tuple([int(c) for c in re.findall(r"\d+", lines[0])])
        self.__b = tuple([int(c) for c in re.findall(r"\d+", lines[1])])
        self.__p = tuple([int(c) for c in re.findall(r"\d+", lines[2])])

    def get_win_tokens(self, extra: int) -> int:
        p_x = self.__p[0] + extra
        p_y = self.__p[1] + extra
        i = (self.__b[0] * p_y - self.__b[1] * p_x) // (self.__a[1] * self.__b[0] - self.__a[0] * self.__b[1])
        j = (p_x - i * self.__a[0]) // self.__b[0]
        if ((p_x - i * self.__a[0]) % self.__b[0] == 0 and
            (self.__b[0] * p_y - self.__b[1] * p_x) % (self.__a[1] * self.__b[0] - self.__a[0] * self.__b[1]) == 0):
            return 3 * i + j
        return 0


class Arcade:
    def __init__(self, rawstr: str) -> None:
        self.__machines = [Machine(block) for block in rawstr.split('\n\n')]

    def get_fewest_tokens(self) -> int:
        return sum([m.get_win_tokens(0) for m in self.__machines])

    def get_fewest_tokens_advanced(self) -> int:
        return sum([m.get_win_tokens(10_000_000_000_000) for m in self.__machines])


def main(aoc_input: str) -> None:
    arcade = Arcade(aoc_input)
    print(f"Part 1: {arcade.get_fewest_tokens()}")
    print(f"Part 2: {arcade.get_fewest_tokens_advanced()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/day13.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
