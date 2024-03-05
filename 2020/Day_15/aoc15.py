"""
Dictionary based solution, same for both Part 1 and Part 2.
P1 zips by fast, but P2 takes a handful of seconds.
"""
import sys


class MemoryGame:
    def __init__(self, nbrs: list[int]):
        self.__startlist = list(nbrs)

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


def main() -> int:
    with open('../Inputfiles/aoc15.txt', 'r') as file:
        mygame = MemoryGame([int(i) for i in file.read().strip('\n').split(',')])
    print("Part 1:", mygame.playrounds(2020))
    print("Part 2:", mygame.playrounds(30_000_000))
    return 0


if __name__ == "__main__":
    sys.exit(main())
