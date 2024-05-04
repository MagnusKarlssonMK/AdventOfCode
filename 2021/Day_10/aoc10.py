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


def getsyntaxscore(char: str) -> int:
    scoretable = {')': 3, ']': 57, '}': 1197, '>': 25137}
    if char in scoretable:
        return scoretable[char]
    return 0


def getautocompletescore(char: str) -> int:
    scoretable = {')': 1, ']': 2, '}': 3, '>': 4}
    if char in scoretable:
        return scoretable[char]
    return 0


class NavigationLine:
    OPENING_BRACKETS = ('(', '{', '<', '[')
    BRACKET_MAP = {'(': ')', '{': '}', '<': '>', '[': ']'}

    def __init__(self, newline: str) -> None:
        self.line = newline

    def validateline(self) -> tuple[int, int]:
        idx = 0
        while idx < len(self.line):
            res, i = self.validatechunk(idx)
            if res != 0:
                return res, i
            idx = i + 1
        return 0, idx

    def validatechunk(self, startidx: int = 0) -> tuple[int, int]:
        if self.line[startidx] not in NavigationLine.OPENING_BRACKETS:
            return 2, getsyntaxscore(self.line[startidx])
        if startidx >= len(self.line) - 1:
            return 1, startidx + 1
        if self.line[startidx + 1] == NavigationLine.BRACKET_MAP[self.line[startidx]]:
            return 0, startidx + 1
        currentidx = startidx + 1
        while currentidx < len(self.line):
            res, i = self.validatechunk(currentidx)
            if res == 0:
                if i + 1 >= len(self.line):
                    return 1, i
                if self.line[i + 1] == NavigationLine.BRACKET_MAP[self.line[startidx]]:
                    return 0, i + 1
                elif self.line[i + 1] not in NavigationLine.OPENING_BRACKETS:
                    return 2, getsyntaxscore(self.line[i + 1])
                currentidx = i + 1
            else:
                return res, i
        return 1, currentidx

    def autocomplete(self) -> int:
        line = [c for c in self.line]
        count = 0
        close_br = ""
        for idx in reversed(range(len(self.line))):
            if line[idx] not in NavigationLine.OPENING_BRACKETS:
                if count == 0:
                    close_br = line[idx]
                    count = 1
                elif line[idx] == close_br:
                    count += 1
                line.pop(idx)
            elif count > 0:
                if NavigationLine.BRACKET_MAP[line[idx]] == close_br:
                    count -= 1
                line.pop(idx)
        resultlist = [getautocompletescore(NavigationLine.BRACKET_MAP[c]) for c in reversed(line)]
        retval = 0
        for i in resultlist:
            retval *= 5
            retval += i
        return retval


class NavigationSubsystem:
    def __init__(self, rawstr: str) -> None:
        self.__lines: list[str] = rawstr.splitlines()
        self.__incomplete_lines: list[NavigationLine] = []

    def get_corrupted_score(self) -> int:
        retval = 0
        for line in self.__lines:
            newline = NavigationLine(line)
            result, score = newline.validateline()
            if result == 2:
                retval += score
            elif result == 1:
                self.__incomplete_lines.append(newline)
        return retval

    def get_middle_score(self) -> int:
        scores = sorted([incomplete.autocomplete() for incomplete in self.__incomplete_lines])
        return scores[len(scores) // 2]


def main() -> int:
    with open('../Inputfiles/aoc10.txt', 'r') as file:
        mysystem = NavigationSubsystem(file.read().strip('\n'))
    print(f"Part 1: {mysystem.get_corrupted_score()}")
    print(f"Part 2: {mysystem.get_middle_score()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
