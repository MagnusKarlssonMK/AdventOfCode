import sys


def main() -> int:
    with open('../Inputfiles/aoc6.txt') as file:
        line = file.readline().strip('\n')

    # A
    for idx in range(len(line) - 3):
        if len(set(line[idx:idx+4])) == 4:
            print("Part1: ", idx + 4)
            break

    # B
    for idx in range(len(line) - 13):
        if len(set(line[idx:idx+14])) == 14:
            print("Part2: ", idx + 14)
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
