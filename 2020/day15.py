"""
Dictionary based solution, same for both Part 1 and Part 2.
P1 zips by fast, but P2 takes a handful of seconds.
"""
import time
from pathlib import Path


class MemoryGame:
    def __init__(self, rawstr: str) -> None:
        self.__startlist = [int(i) for i in rawstr.split(',')]

    def playrounds(self, rounds: int) -> int:
        nbrs: dict[int:int] = {}
        for i in range(len(self.__startlist) - 1):
            nbrs[self.__startlist[i]] = i
        lastspoken = self.__startlist[-1]
        for turn in range(len(self.__startlist), rounds):
            if lastspoken not in nbrs:
                nbrs[lastspoken] = turn - 1
                lastspoken = 0
            else:
                speak = turn - nbrs[lastspoken] - 1
                nbrs[lastspoken] = turn - 1
                lastspoken = speak
        return lastspoken


def main(aoc_input: str) -> None:
    mygame = MemoryGame(aoc_input)
    print(f"Part 1: {mygame.playrounds(2020)}")
    print(f"Part 2: {mygame.playrounds(30_000_000)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day15.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
