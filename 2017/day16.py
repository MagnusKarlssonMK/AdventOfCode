"""
Part 1 is straightforward, just store the order of the programs in a list and perform the instructions.
The main challenge here is for part 2 - obviously we don't want to run 1B simulations, so instead, try to detect how
many rounds are needed until it starts over with the same value. When knowing that cycle length, we can use the stored
values to directly calculate what the value will be after 1B rounds.
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Move:
    op: str
    arg1: str = None
    arg2: str = None


class Dance:
    def __init__(self, rawstr: str) -> None:
        self.__moves = [Move(i[0], *i[1:].split('/')) for i in rawstr.split(',')]
        self.__programs = [chr(c) for c in range(ord('a'), ord('p') + 1)]
        self.__seen: list[str] = []

    def __perform_dance(self) -> str:
        for mv in self.__moves:
            match mv.op:
                case 's':
                    self.__programs = self.__programs[-int(mv.arg1):] + self.__programs[:-int(mv.arg1)]
                case 'x':
                    self.__programs[int(mv.arg1)], self.__programs[int(mv.arg2)] = (self.__programs[int(mv.arg2)],
                                                                                    self.__programs[int(mv.arg1)])
                case 'p':
                    i1, i2 = self.__programs.index(mv.arg1), self.__programs.index(mv.arg2)
                    self.__programs[i1], self.__programs[i2] = self.__programs[i2], self.__programs[i1]
                case _:
                    pass
        return ''.join(self.__programs)

    def get_one_round_order(self) -> str:
        new_order = self.__perform_dance()
        self.__seen.append(new_order)
        return new_order

    def get_one_billion_rounds_order(self) -> str:
        target_rounds = 1_000_000_000
        cycle_len = None
        while not cycle_len and len(self.__seen) < target_rounds:
            new_order = self.__perform_dance()
            if new_order == self.__seen[0]:
                cycle_len = len(self.__seen)
            self.__seen.append(new_order)
        if not cycle_len:
            # Just in case, let's hope we don't end up here! 1b loops without cycle would take a while...
            return self.__seen[-1]
        return self.__seen[(target_rounds - 1) % cycle_len]  # Target - 1 since initial value is not included in seen


def main(aoc_input: str) -> None:
    dance = Dance(aoc_input)
    print(f"Part 1: {dance.get_one_round_order()}")
    print(f"Part 2: {dance.get_one_billion_rounds_order()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day16.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
