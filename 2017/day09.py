"""
Recursive solution to break down the string into smaller parts.
"""
import sys


class Stream:
    def __init__(self, rawstr: str) -> None:
        self.__s = rawstr
        self.__garbagecount = 0

    def __get_group_score(self, startidx: int, level: int) -> tuple[int, int]:  # stopidx, score
        i = startidx
        ignored = False
        garbage = False
        score = 0
        while i < len(self.__s):
            if ignored:
                ignored = False
            elif garbage:
                if self.__s[i] == '>':
                    garbage = False
                elif self.__s[i] == '!':
                    ignored = True
                else:
                    self.__garbagecount += 1
            else:
                match self.__s[i]:
                    case '{':
                        i, new_score = self.__get_group_score(i + 1, level + 1)
                        score += new_score
                    case '}':
                        return i, score + level
                    case '<':
                        garbage = True
                    case '!':
                        ignored = True
            i += 1
        return -1, -1

    def get_total_score(self) -> int:
        return self.__get_group_score(1, 1)[1]

    def get_total_garbage(self) -> int:
        return self.__garbagecount


def main() -> int:
    with open('../Inputfiles/aoc9.txt', 'r') as file:
        stream = Stream(file.read().strip('\n'))
    print(f"Part 1: {stream.get_total_score()}")
    print(f"Part 2: {stream.get_total_garbage()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
