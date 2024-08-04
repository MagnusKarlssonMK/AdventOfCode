"""
Part 1: Store the memory banks in a class, and rebalance according to the description. Store the current configuration
in a set after every rebalancing and check if we have a repeated value.
Part 2: We saved the state of the memory banks after part 1, so simply run the checker again to get the answer for the
next cycle.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2017/day06.txt')


class Memory:
    def __init__(self, rawstr: str) -> None:
        self.__banks = list(map(int, rawstr.split()))

    def __rebalance(self) -> None:
        val = max(self.__banks)
        i = self.__banks.index(val)
        self.__banks[i] = 0
        while val > 0:
            i = (i + 1) % len(self.__banks)
            self.__banks[i] += 1
            val -= 1

    def get_cycles_count(self) -> int:
        seen_configs = {tuple(self.__banks)}
        while True:
            self.__rebalance()
            next_cfg = tuple(self.__banks)
            if next_cfg in seen_configs:
                return len(seen_configs)
            seen_configs.add(next_cfg)


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        memory = Memory(file.read().strip('\n'))
    print(f"Part 1: {memory.get_cycles_count()}")
    print(f"Part 2: {memory.get_cycles_count()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
