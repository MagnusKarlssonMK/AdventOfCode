"""
"""
import time
from pathlib import Path
from enum import Enum
from dataclasses import dataclass


class Techniques(Enum):
    CUT = 'cut'
    DEAL_W_INC = 'deal with increment'
    DEAL_INTO_NEW = 'deal into new'


@dataclass(frozen=True)
class Shuffle:
    tech: Techniques
    value: int


class Spacedeck:
    def __init__(self, rawstr: str) -> None:
        self.__shuffle_process: list[Shuffle] = []
        for line in rawstr.splitlines():
            words = line.split()
            if Techniques.CUT.value in line:
                self.__shuffle_process.append(Shuffle(Techniques.CUT, int(words[-1])))
            elif Techniques.DEAL_W_INC.value in line:
                self.__shuffle_process.append(Shuffle(Techniques.DEAL_W_INC, int(words[-1])))
            elif Techniques.DEAL_INTO_NEW.value in line:
                self.__shuffle_process.append(Shuffle(Techniques.DEAL_INTO_NEW, -1))

    def get_card_pos(self, deck_size: int = 10_007, target: int = 2019) -> int:
        deck = list(range(deck_size))
        for s in self.__shuffle_process:
            match s.tech:
                case Techniques.CUT:
                    deck = deck[s.value:] + deck[:s.value]
                case Techniques.DEAL_W_INC:
                    newdeck = [0 for _ in enumerate(deck)]
                    for i, card in enumerate(deck):
                        newdeck[i * s.value % len(deck)] = card
                    deck = newdeck
                case Techniques.DEAL_INTO_NEW:
                    deck = deck[::-1]
        return deck.index(target)

    def get_giant_deck_card_pos(self, deck_size: int = 119315717514047, shuffle_count: int = 101741582076661,
                                target: int = 2020) -> int:
        a = 1
        b = 0
        for s in self.__shuffle_process:
            match s.tech:
                case Techniques.CUT:
                    b = (b + (a * s.value)) % deck_size
                case Techniques.DEAL_W_INC:
                    a = (a * pow(s.value, -1, deck_size)) % deck_size
                case Techniques.DEAL_INTO_NEW:
                    b = (b - a) % deck_size
                    a = (-a) % deck_size
        return ((target * pow(a, shuffle_count, deck_size) +
                ((1 - pow(a, shuffle_count, deck_size)) * pow(1 - a, -1, deck_size) * b)) % deck_size)


def main(aoc_input: str) -> None:
    deck = Spacedeck(aoc_input)
    print(f"Part 1: {deck.get_card_pos()}")
    print(f"Part 2: {deck.get_giant_deck_card_pos()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day22.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
