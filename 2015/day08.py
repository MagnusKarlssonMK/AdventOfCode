"""
Trying to avoid using literal eval to find a solution that can be transferred to other languages.
So pretty much scan the lines for special characters and;
- For part 1, count number of positions that does not represent an actual character.
- For part 2, count the characters that needs to be escaped.
"""
import sys


class SantaList:
    def __init__(self, rawstr: str) -> None:
        self.__literals = rawstr.splitlines()

    def get_unchar_count(self) -> int:
        count = 0
        for line in self.__literals:
            count += 2  # Add 2 for the surrounding double quotes
            i = 1
            while i < len(line) - 1:
                if line[i] == '\\':
                    if line[i + 1] == '\"' or line[i + 1] == '\\':
                        count += 1
                        i += 1
                    elif line[i + 1] == 'x':
                        count += 3
                        i += 3
                i += 1
        return count

    def get_encoded_diff(self) -> int:
        count = 0
        for line in self.__literals:
            count += 2  # Surrounding double quotes will expand by one character each
            for c in line:
                if c == '\"' or c == '\\':
                    count += 1
        return count


def main() -> int:
    with open('../Inputfiles/aoc8.txt', 'r') as file:
        santalist = SantaList(file.read().strip('\n'))
    print(f"Part 1: {santalist.get_unchar_count()}")
    print(f"Part 2: {santalist.get_encoded_diff()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
