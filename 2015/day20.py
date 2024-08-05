"""
Seems kind of brute-force-y, but performs much better than attempts to build divisor generator solutions.
Basically simulates the present delivery by iterating over the elfs from 1 and up. Small optimization to keep track
of the lowest house found yet reaching the target to avoid iterating further over higher houses that have no chance of
winning.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2015/day20.txt')


class ElfDelivery:
    __ELF_PRESENTS = 10
    __LAZY_ELF_PRESENTS = 11
    __LAZY_ELF_CAPACITY = 50

    def __init__(self, rawstr: str) -> None:
        self.__target = int(rawstr)

    def get_lowest_house(self) -> int:
        houses = [10 for _ in range(self.__target // ElfDelivery.__ELF_PRESENTS)]
        # Note 1 - We are guaranteed to hit the target at t/10 since each elf delivers 10 times its number
        # Note 2 - Zero indexing houses, i.e. houses[0] == House_1
        # Note 3 - We know the first elf will visit all houses, so initialize houses to 10 to skip the first iteration
        upper_bound = len(houses)
        for elf in range(2, len(houses) + 1):
            for i in range(elf - 1, upper_bound, elf):
                houses[i] += ElfDelivery.__ELF_PRESENTS * elf
                if houses[i] >= self.__target:
                    upper_bound = min(upper_bound, i + 1)
        return upper_bound

    def get_lowest_house_lazy_elf(self) -> int:
        houses = [0 for _ in range(self.__target // ElfDelivery.__LAZY_ELF_PRESENTS)]
        upper_bound = len(houses)
        for elf in range(1, len(houses) + 1):
            presents = 0
            for i in range(elf - 1, upper_bound, elf):
                presents += 1
                houses[i] += ElfDelivery.__LAZY_ELF_PRESENTS * elf
                if houses[i] >= self.__target:
                    upper_bound = min(upper_bound, i + 1)
                if presents >= ElfDelivery.__LAZY_ELF_CAPACITY:
                    break
        return upper_bound


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        delivery = ElfDelivery(file.read().strip('\n'))
    print(f"Part 1: {delivery.get_lowest_house()}")
    print(f"Part 2: {delivery.get_lowest_house_lazy_elf()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
