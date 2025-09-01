import time
from pathlib import Path
import math
import re
from collections.abc import Generator


class Monkey:
    def __init__(self, rawstr: str) -> None:
        lines = rawstr.splitlines()
        self.__startitems = tuple(map(int, re.findall(r"\d+", lines[1])))
        op = lines[2].split(' = ')[-1].split()
        self.__operation = op[1]
        self.__op_nbrs = (op[0], op[2])
        self.test = int(lines[3].split()[-1])
        self.__destination_pass = int(lines[4].split()[-1])
        self.__destination_fail = int(lines[5].split()[-1])
        self.__current_items = list(self.__startitems)
        self.inpection_count = 0

    def reset(self) -> None:
        self.__current_items = list(self.__startitems)
        self.inpection_count = 0

    def inspect(self, apply_relief: bool, lcm: int) -> Generator[tuple[int, int]]:  # Destination monkey ID, item level
        while self.__current_items:
            current_item = self.__current_items.pop(0)
            self.inpection_count += 1
            nbrs = [current_item if not n.isdigit() else int(n) for n in self.__op_nbrs]
            if self.__operation == '*':
                current_item = nbrs[0] * nbrs[1]
            elif self.__operation == '+':
                current_item = sum(nbrs)
            if apply_relief:
                current_item //= 3
            else:
                current_item %= lcm
            if current_item % self.test == 0:
                yield self.__destination_pass, current_item
            else:
                yield self.__destination_fail, current_item

    def catch_item(self, new_item: int) -> None:
        self.__current_items.append(new_item)


class KeepAway:
    def __init__(self, rawstr: str) -> None:
        self.__monkeys: dict[int, Monkey] = {}
        for i, block in enumerate(rawstr.split('\n\n')):
            self.__monkeys[i] = Monkey(block)

    def get_monkey_level(self, rounds: int = 20, apply_relief: bool = True) -> int:
        lcm = 1 if apply_relief else math.lcm(*[m.test for m in self.__monkeys.values()])
        for _ in range(rounds):
            for monkey in self.__monkeys:
                for destination, item in self.__monkeys[monkey].inspect(apply_relief, lcm):
                    self.__monkeys[destination].catch_item(item)
        result = sorted([m.inpection_count for m in self.__monkeys.values()], reverse=True)
        [self.__monkeys[m].reset() for m in self.__monkeys]
        return result[0] * result[1]


def main(aoc_input: str) -> None:
    game = KeepAway(aoc_input)
    print(f"Part 1: {game.get_monkey_level()}")
    print(f"Part 2: {game.get_monkey_level(10_000, False)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2022/day11.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
