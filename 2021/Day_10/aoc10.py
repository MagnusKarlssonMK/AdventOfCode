"""
Solve with recursive function.
Define a class for it to avoid having to pass the line throughout all function calls.
"""
import sys

OpeningBrackets = ('(', '{', '<', '[')
BracketMap = {'(': ')', '{': '}', '<': '>', '[': ']'}


def getbracketscore(char: str) -> int:
    scoretable = {')': 3, ']': 57, '}': 1197, '>': 25137}
    if char in list(scoretable.keys()):
        return scoretable[char]
    return 0


class NavigationLine:
    def __init__(self, newline: str):
        self.line = newline

    def validatechunk(self, startidx: int = 0) -> tuple[int, int]:
        if self.line[startidx] not in OpeningBrackets:
            return 2, getbracketscore(self.line[startidx])
        if startidx >= len(self.line) - 1:
            return 1, startidx + 1
        if self.line[startidx + 1] == BracketMap[self.line[startidx]]:
            return 0, startidx + 1
        currentidx = startidx + 1
        while currentidx < len(self.line):
            result = self.validatechunk(currentidx)
            if result[0] == 0:
                if result[1] + 1 >= len(self.line):
                    return 1, result[1]
                if self.line[result[1] + 1] == BracketMap[self.line[startidx]]:
                    return 0, result[1] + 1
                elif self.line[result[1] + 1] not in OpeningBrackets:
                    return 2, getbracketscore(self.line[result[1] + 1])
                currentidx = result[1] + 1
            else:
                return result
        return 1, currentidx


def main() -> int:
    with open('../Inputfiles/aoc10.txt', 'r') as file:
        lines = file.read().strip('\n').splitlines()
    p1_score = 0
    for line in lines:
        newline = NavigationLine(line)
        # result, score = newline.validateline()
        result, score = newline.validatechunk()
        if result == 2:
            p1_score += score
    print("Part 1: ", p1_score)
    return 0


if __name__ == "__main__":
    sys.exit(main())
