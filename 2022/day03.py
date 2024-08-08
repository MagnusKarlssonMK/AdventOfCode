import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day03.txt')


class Supplies:
    __RANGELIST = ((range(ord('a'), ord('z') + 1), 1), (range(ord('A'), ord('Z') + 1), 27))

    def __init__(self, rawstr: str) -> None:
        self.__rucksacks = rawstr.splitlines()

    def get_total_prio_both_compartments(self) -> int:
        result = 0
        for rucksack in self.__rucksacks:
            left, right = rucksack[:len(rucksack) // 2], rucksack[len(rucksack) // 2:]
            if len(shared := ''.join(set(left) & set(right))) > 0:
                result += sum([ord(shared[0]) - r0.start + r1 for r0, r1 in Supplies.__RANGELIST
                               if ord(shared[0]) in r0])
        return result

    def get_total_prio_group(self) -> int:
        result = 0
        for r in range(0, len(self.__rucksacks), 3):
            s0, s1, s2 = self.__rucksacks[r: r + 3]
            if len(shared := ''.join(set(s0) & set(s1) & set(s2))) > 0:
                result += sum([ord(shared[0]) - r0.start + r1 for r0, r1 in Supplies.__RANGELIST
                               if ord(shared[0]) in r0])
        return result


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        supplies = Supplies(file.read().strip('\n'))
    print(f"Part 1: {supplies.get_total_prio_both_compartments()}")
    print(f"Part 2: {supplies.get_total_prio_group()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
