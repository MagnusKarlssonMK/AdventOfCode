import sys


class Elf:
    def __init__(self, calories: list[int]):
        self.calories = calories
        self.totalcalories = sum(calories)

    def __str__(self):
        return f"{self.calories}"


def main() -> int:
    elf_list = []
    with open('../Inputfiles/aoc1.txt', 'r') as file:
        indata = file.read().split('\n\n')
    [elf_list.append(Elf(list(map(int, elf.strip('\n').split('\n'))))) for elf in indata]

    elf_list.sort(key=lambda tot: tot.totalcalories, reverse=True)

    print("Part1: ", elf_list[0].totalcalories)

    print("Part2: ", sum([elf_list[num].totalcalories for num in range(3)]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
