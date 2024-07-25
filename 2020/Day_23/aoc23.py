"""
Storing the cup list as a singly linked list in an array, to avoid slow list operations since we need to do a lot
of moves for part 2.
"""
import sys
from dataclasses import dataclass


@dataclass
class LinkList:
    cups: list[int]

    def get_next(self, val: int) -> int:
        return val - 1 if val > 1 else len(self.cups) - 1

    def get_order(self) -> str:
        value = 1
        return "".join([str(value := self.cups[value]) for _ in range(len(self.cups) - 2)])


class Crabcups:
    def __init__(self, rawstr: str) -> None:
        self.__inputnbrs = list(map(int, rawstr))
        self.__list = None
        self.__current = 0
        self.__reset()

    def __reset(self) -> None:
        self.__list = LinkList([0 for _ in range(max(self.__inputnbrs) + 1)])
        self.__current = self.__inputnbrs[0]
        previous = self.__inputnbrs[-1]
        for cup in self.__inputnbrs:
            self.__list.cups[previous] = cup
            previous = cup

    def __play_move(self) -> None:
        r = self.__current
        removed = [r := self.__list.cups[r] for _ in range(3)]
        destination = self.__list.get_next(self.__current)
        while destination in removed:
            destination = self.__list.get_next(destination)
        self.__list.cups[self.__current] = self.__list.cups[removed[-1]]
        self.__list.cups[removed[-1]] = self.__list.cups[destination]
        self.__list.cups[destination] = removed[0]
        self.__current = self.__list.cups[self.__current]

    def play_moves(self, moves: int = 100) -> int:
        for _ in range(moves):
            self.__play_move()
        return int(self.__list.get_order())

    def play_extended_moves(self, moves: int = 10_000_000) -> int:
        self.__reset()
        m = max(self.__inputnbrs)
        last = self.__inputnbrs[-1]
        self.__list.cups.extend(range(m + 2, 1_000_002))
        self.__list.cups[-1] = self.__list.cups[last]
        self.__list.cups[last] = m + 1
        for _ in range(moves):
            self.__play_move()
        return self.__list.cups[1] * self.__list.cups[self.__list.cups[1]]


def main() -> int:
    with open('../Inputfiles/aoc23.txt', 'r') as file:
        game = Crabcups(file.read().strip('\n'))
    print(f"Part 1: {game.play_moves()}")
    print(f"Part 2: {game.play_extended_moves()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
