"""
Resisting the temptation to build a tree, instead storing the numbers as a flat list of tuples of value and level
(tuple represented by a dataclass to easier access and change the values). Pairs can then be identified by comparing
levels of adjacent entries when scanning the tuples from left to right. That way it becomes almost trivial to explode
and split numbers, compared to how it would have been in a tree.
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass
class SingleNbr:
    nbr: int
    level: int

    def __repr__(self):
        return f"{self.nbr}({self.level})"


class Snailnumber:
    def __init__(self, nbrstr: str) -> None:
        self.__nbrs: list[SingleNbr] = []
        level = 0
        for c in nbrstr:
            if c == '[':
                level += 1
            elif c == ']':
                level -= 1
            elif c.isdigit():
                self.__nbrs.append(SingleNbr(int(c), level))

    def __reducenbr(self) -> None:
        changed = True
        while changed:
            self.__explode()
            changed = self.__split()

    def __explode(self) -> None:
        i = 0
        while i < len(self.__nbrs) - 1:
            if self.__nbrs[i].level == self.__nbrs[i+1].level and self.__nbrs[i].level > 4:
                if i > 0:
                    self.__nbrs[i-1].nbr += self.__nbrs[i].nbr
                if i < len(self.__nbrs) - 2:
                    self.__nbrs[i+2].nbr += self.__nbrs[i+1].nbr
                self.__nbrs[i].nbr = 0
                self.__nbrs[i].level -= 1
                self.__nbrs.pop(i+1)
            i += 1

    def __split(self) -> bool:
        i = 0
        while i < len(self.__nbrs):
            if self.__nbrs[i].nbr > 9:
                left = SingleNbr(self.__nbrs[i].nbr // 2, self.__nbrs[i].level + 1)
                right = SingleNbr((self.__nbrs[i].nbr + 1) // 2, self.__nbrs[i].level + 1)
                self.__nbrs[i] = left
                self.__nbrs.insert(i+1, right)
                # Note: we need to run the explosion again after every single split, we can't do all splits in one go
                return True
            i += 1
        return False

    def __add__(self, other) -> "Snailnumber":
        newnbr = Snailnumber("")
        for nbr in self.__nbrs:
            newnbr.__nbrs.append(SingleNbr(nbr.nbr, nbr.level + 1))
        for nbr in other.__nbrs:
            newnbr.__nbrs.append(SingleNbr(nbr.nbr, nbr.level + 1))
        newnbr.__reducenbr()
        return newnbr

    def get_magnitude(self) -> int:
        crunchnumbers = list(self.__nbrs)
        i = 0
        while i < len(crunchnumbers) - 1:
            if crunchnumbers[i].level == crunchnumbers[i+1].level:
                crunchnumbers[i].nbr = (3 * crunchnumbers[i].nbr) + (2 * crunchnumbers[i+1].nbr)
                crunchnumbers[i].level -= 1
                crunchnumbers.pop(i+1)
                i = 0
            else:
                i += 1
        return crunchnumbers[0].nbr

    def __repr__(self):
        return f"{self.__nbrs}"


class Calculator:
    def __init__(self, rawstr: str) -> None:
        self.__nbrs = [Snailnumber(line) for line in rawstr.splitlines()]

    def get_finalsum(self) -> int:
        if len(self.__nbrs) < 2:
            return 0
        # Add all values
        sumvalue = self.__nbrs[0] + self.__nbrs[1]
        for i in range(2, len(self.__nbrs)):
            sumvalue += self.__nbrs[i]
        # Calculate value
        return sumvalue.get_magnitude()

    def get_maximum_magnitude(self) -> int:
        maxmag = 0
        for i in range(len(self.__nbrs)):
            for j in range(len(self.__nbrs)):
                if i == j:
                    continue
                val = self.__nbrs[i] + self.__nbrs[j]
                maxmag = max(maxmag, val.get_magnitude())
        return maxmag


def main(aoc_input: str) -> None:
    lines = Calculator(aoc_input)
    print(f"Part 1: {lines.get_finalsum()}")
    print(f"Part 2: {lines.get_maximum_magnitude()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day18.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
