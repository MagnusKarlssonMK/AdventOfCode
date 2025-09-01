"""
Solution: rather than storing the actual string, store the developed polymer as a dict of pairs with a counter.
For every step, expand each pair into two new pairs and inherit the counter value for both.
"""
import time
from pathlib import Path
from collections import Counter


class Polymer:
    def __init__(self, rawstr: str) -> None:
        self.__template, r = rawstr.split('\n\n')
        rules = [(left, right) for left, right in [line.split(' -> ') for line in r.splitlines()]]
        self.__rules: dict[str, str] = {}
        self.__paircount: dict[str, int] = {}
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
            buffer: list[tuple[str, int]] = []
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


def main(aoc_input: str) -> None:
    poly = Polymer(aoc_input)
    poly.takesteps(10)
    print(f"Part 1: {poly.getscore()}")
    poly.reset()
    poly.takesteps(40)
    print(f"Part 2: {poly.getscore()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day14.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
