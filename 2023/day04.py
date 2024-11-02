"""
Basically decodes the input into a Scratchcard class, and then counts the scores according to the rules.
"""
import time
from pathlib import Path
import re


class Scratchcard:
    def __init__(self, inputstring: str) -> None:
        cardstr, reststr = inputstring.split(":")
        self.cardid = int(re.findall(r"\d+", cardstr)[0])
        winstr, drawstr = reststr.split(" | ")
        winningnumbers = set(map(int, [nbr for nbr in winstr.split()]))
        drawnumbers = set(map(int, [nbr for nbr in drawstr.split()]))
        self.wincount = len(winningnumbers & drawnumbers)
        self.score = 2 ** (self.wincount - 1) if self.wincount > 0 else 0


class Cardpile:
    def __init__(self, rawstr: str) -> None:
        self.__cards = [Scratchcard(line) for line in rawstr.splitlines()]

    def get_totalpoints(self) -> int:
        return sum([card.score for card in self.__cards])

    def get_cardcount(self) -> int:
        total_nbr = 0
        copylist = [0 for _ in range(10)]
        for card in self.__cards:
            newcardcount = 1 + copylist.pop(0)
            total_nbr += newcardcount
            copylist.append(0)
            for i, _ in enumerate(copylist):
                if i < card.wincount:
                    copylist[i] += newcardcount
        return total_nbr


def main(aoc_input: str) -> None:
    pile = Cardpile(aoc_input)
    print(f"Part 1: {pile.get_totalpoints()}")
    print(f"Part 2: {pile.get_cardcount()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2023/day04.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
