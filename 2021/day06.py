"""
Solution - rather than storing each and every lantern fish individually, simply store a list of internal timer states
0 - 8 and how many fish are in each state. When stepping a day, simply pop the first element in the list corresponding
to state-0 and add that number to state-6 and also append that number to state-8.
"""
import time
from pathlib import Path


class Fishies:
    def __init__(self, rawstr: str):
        nbrs = list(map(int, rawstr.split(',')))
        self.__states = [0 for _ in range(9)]
        for nbr in nbrs:
            self.__states[nbr] += 1

    def get_answers(self) -> tuple[int, int]:
        p1 = 0
        for n in range(256):
            state_0 = self.__states.pop(0)
            self.__states[6] += state_0
            self.__states.append(state_0)
            if n == 79:
                p1 = sum(self.__states)
        return p1, sum(self.__states)


def main(aoc_input: str) -> None:
    fishies = Fishies(aoc_input)
    p1, p2 = fishies.get_answers()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day06.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
