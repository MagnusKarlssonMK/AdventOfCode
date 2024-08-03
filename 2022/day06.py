import sys


def main() -> int:
    with open('../Inputfiles/aoc6.txt') as file:
        line = file.read().strip('\n')

    # Part 1
    for idx in range(len(line) - 3):
        if len(set(line[idx:idx+4])) == 4:
            print(f"Part1: {idx + 4}")
            break

    # Part 2
    for idx in range(len(line) - 13):
        if len(set(line[idx:idx+14])) == 14:
            print(f"Part2: {idx + 14}")
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
