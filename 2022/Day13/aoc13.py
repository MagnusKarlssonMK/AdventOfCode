import sys


def ispairrightorder(left: str, right: str) -> bool:
    for idx in range(min(len(left), len(right))):
        pass
        # If first char in both are digits, start comparing. If inconclusive, strip any comma or closing bracket and recurse
        # If first char in both are left brackets, find closing brackets and recurse the interior
        # If only one side is left brackets, add brackets around the other side and retry
    return False


def main() -> int:
    with open('aoc13.txt', 'r') as file:
        indata: list[str] = file.read().strip('\n').split('\n\n')
    pairs: list[tuple[str, str]] = []
    for pair in indata:
        left, right = pair.split('\n')
        pairs.append((left, right))

    count = 0
    for pair in pairs:
        if ispairrightorder(pair[0], pair[1]):
            count += 1

    print("Part 1: ", count)

    return 0


if __name__ == "__main__":
    sys.exit(main())
