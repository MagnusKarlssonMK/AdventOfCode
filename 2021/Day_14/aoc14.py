"""
Solution: rather than storing the actual string, store the developed polymer as a dict of pairs with a counter.
For every step, expand each pair into two new pairs and inherit the counter value for both.
"""
import sys
from collections import Counter


class Polymer:
    def __init__(self, template: str, rules: list[tuple[str, str]]):
        self.template = template
        self.rules: dict[str: str] = {}
        self.paircount: dict[str: int] = {}
        for left, right in rules:
            self.rules[left] = right
        self.reset()

    def reset(self):
        self.paircount.clear()
        for i in range(len(self.template) - 1):
            pair = self.template[i] + self.template[i + 1]
            self.__addpair(pair, 1)

    def __addpair(self, pair: str, count: int):
        if pair in self.paircount:
            self.paircount[pair] += count
        else:
            self.paircount[pair] = count

    def takesteps(self, count: int):
        for _ in range(count):
            buffer = []
            for key in self.paircount:
                buffer.append((key[0] + self.rules[key], self.paircount[key]))
                buffer.append((self.rules[key] + key[1], self.paircount[key]))
            self.paircount.clear()
            [self.__addpair(*b) for b in buffer]

    def getscore(self) -> int:
        countlist = Counter()
        for pair in list(self.paircount.keys()):
            countlist[pair[0]] += self.paircount[pair]
        countlist[self.template[-1]] += 1
        return max(countlist.values()) - min(countlist.values())


def main() -> int:
    with open('../Inputfiles/aoc14.txt', 'r') as file:
        template, r = file.read().strip('\n').split('\n\n')
    rules = [(left, right) for left, right in [line.split(' -> ') for line in r.splitlines()]]
    poly = Polymer(template, rules)
    poly.takesteps(10)
    print(f"Part 1: {poly.getscore()}")
    poly.reset()
    poly.takesteps(40)
    print(f"Part 2: {poly.getscore()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
