"""
Solution: rather than storing the actual string, store the developed polymer as a dict of pairs with a counter.
For every step, expand each pair into two new pairs and inherit the counter value for both.
"""
import sys
from collections import Counter


class Polymer:
    def __init__(self, rawstr: str) -> None:
        self.__template, r = rawstr.split('\n\n')
        rules = [(left, right) for left, right in [line.split(' -> ') for line in r.splitlines()]]
        self.__rules: dict[str: str] = {}
        self.__paircount: dict[str: int] = {}
        for left, right in rules:
            self.__rules[left] = right
        self.reset()

    def reset(self) -> None:
        self.__paircount.clear()
        for i in range(len(self.__template) - 1):
            pair = self.__template[i] + self.__template[i + 1]
            self.__addpair(pair, 1)

    def __addpair(self, pair: str, count: int) -> None:
        if pair in self.__paircount:
            self.__paircount[pair] += count
        else:
            self.__paircount[pair] = count

    def takesteps(self, count: int) -> None:
        for _ in range(count):
            buffer = []
            for key in self.__paircount:
                buffer.append((key[0] + self.__rules[key], self.__paircount[key]))
                buffer.append((self.__rules[key] + key[1], self.__paircount[key]))
            self.__paircount.clear()
            [self.__addpair(*b) for b in buffer]

    def getscore(self) -> int:
        countlist = Counter()
        for pair in list(self.__paircount.keys()):
            countlist[pair[0]] += self.__paircount[pair]
        countlist[self.__template[-1]] += 1
        return max(countlist.values()) - min(countlist.values())


def main() -> int:
    with open('../Inputfiles/aoc14.txt', 'r') as file:
        poly = Polymer(file.read().strip('\n'))
    poly.takesteps(10)
    print(f"Part 1: {poly.getscore()}")
    poly.reset()
    poly.takesteps(40)
    print(f"Part 2: {poly.getscore()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())