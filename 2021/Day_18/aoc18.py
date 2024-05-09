"""

"""
import sys
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
            # print("After explode:")
            # print(self.__nbrs)
            changed = self.__split()
            # print("After split:")
            # print(self.__nbrs)

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
                return True
            i += 1
        return False

    def __add__(self, other) -> "Snailnumber":
        newnbr = Snailnumber("")
        for nbr in self.__nbrs:
            newnbr.__nbrs.append(SingleNbr(nbr.nbr, nbr.level + 1))
        for nbr in other.__nbrs:
            newnbr.__nbrs.append(SingleNbr(nbr.nbr, nbr.level + 1))
        # print("Before reduce:")
        # print(newnbr)
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
        print(sumvalue)
        # Calculate value
        return sumvalue.get_magnitude()


def main() -> int:
    with open('../Inputfiles/aoc18.txt', 'r') as file:
        lines = Calculator(file.read().strip('\n'))
    print(f"Part 1: {lines.get_finalsum()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
