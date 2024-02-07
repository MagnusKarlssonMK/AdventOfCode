"""
Part 1: Solve with recursive function.
Define a class for it to avoid having to pass the line throughout all function calls.
Part 2: Since we know the incomplete lines are not corrupt, i.e. no need to check validity anymore, we can simply
start from the back of the string, find the first closing bracket, find its corresponding opening bracket, then remove
that entire chunk (since we already know that interior has to be valid). Repeat that process until there are no more
closing brackets left, and the answer is found simply by reversing the order of the remaining opening brackets and
converting to their corresponding closing brackets.
"""
import sys

OpeningBrackets = ('(', '{', '<', '[')
BracketMap = {'(': ')', '{': '}', '<': '>', '[': ']'}


def getsyntaxscore(char: str) -> int:
    scoretable = {')': 3, ']': 57, '}': 1197, '>': 25137}
    if char in list(scoretable.keys()):
        return scoretable[char]
    return 0


def getautocompletescore(char: str) -> int:
    scoretable = {')': 1, ']': 2, '}': 3, '>': 4}
    if char in list(scoretable.keys()):
        return scoretable[char]
    return 0


class NavigationLine:
    def __init__(self, newline: str):
        self.line = newline

    def validateline(self) -> tuple[int, int]:
        idx = 0
        while idx < len(self.line):
            result = self.validatechunk(idx)
            if result[0] != 0:
                return result
            idx = result[1] + 1
        return 0, idx

    def validatechunk(self, startidx: int = 0) -> tuple[int, int]:
        if self.line[startidx] not in OpeningBrackets:
            return 2, getsyntaxscore(self.line[startidx])
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
                    return 2, getsyntaxscore(self.line[result[1] + 1])
                currentidx = result[1] + 1
            else:
                return result
        return 1, currentidx

    def autocomplete(self) -> int:
        line = [c for c in self.line]
        count = 0
        close_br = ""
        for idx in reversed(range(len(self.line))):
            if line[idx] not in OpeningBrackets:
                if count == 0:
                    close_br = line[idx]
                    count = 1
                elif line[idx] == close_br:
                    count += 1
                line.pop(idx)
            elif count > 0:
                if BracketMap[line[idx]] == close_br:
                    count -= 1
                line.pop(idx)
        resultlist = [getautocompletescore(BracketMap[c]) for c in reversed(line)]
        retval = 0
        for i in resultlist:
            retval *= 5
            retval += i
        return retval


def main() -> int:
    with open('../Inputfiles/aoc10.txt', 'r') as file:
        lines = file.read().strip('\n').splitlines()
    p1_score = 0
    incompletelines: list[NavigationLine] = []
    for line in lines:
        newline = NavigationLine(line)
        result, score = newline.validateline()
        if result == 2:
            p1_score += score
        elif result == 1:
            incompletelines.append(newline)
    print("Part 1: ", p1_score)
    p2_scores = sorted([inc_line.autocomplete() for inc_line in incompletelines])
    print("Part 2: ", p2_scores[len(p2_scores) // 2])
    return 0


if __name__ == "__main__":
    sys.exit(main())
