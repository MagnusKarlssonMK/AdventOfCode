import sys


def ismirror(patternlist, candidate, wildcardused):
    if candidate >= (len(patternlist) - 1) or candidate < 0:
        return True if wildcardused else False
    elif patternlist[candidate] == patternlist[candidate + 1]:
        newlist = [item for z, item in enumerate(patternlist) if (z < candidate) or z > (candidate + 1)]
        return ismirror(newlist, candidate - 1, wildcardused)
    elif not wildcardused:
        if bin(patternlist[candidate] ^ patternlist[candidate + 1]).count("1") == 1:
            newlist = [item for z, item in enumerate(patternlist) if (z < candidate) or z > (candidate + 1)]
            return ismirror(newlist, candidate - 1, True)
    return False


def getmirrorscore(patternlist, usewildcard: bool):
    for index in range(0, len(patternlist) - 1):
        if ismirror(patternlist, index, usewildcard):
            return index + 1
    return 0


class Pattern:
    def __init__(self, lineinput: list[str]):
        rows = []
        self.binrows = []
        self.bincolumns = []
        # Convert input to a string of binary characters '0' and '1'
        for line in lineinput:
            convertedstr = ""
            for char in line:
                convertedstr += "0" if char == "." else "1"
            rows.append(convertedstr)
            self.binrows.append(int(convertedstr, 2))

        for i, _ in enumerate(rows[0]):
            convertedstr = ""
            for tmprow in rows:
                convertedstr += tmprow[i]
            self.bincolumns.append(int(convertedstr, 2))

    def getscore(self, wildcard: bool) -> int:
        retval = 0
        retval += 100 * getmirrorscore(self.binrows, wildcard)
        retval += getmirrorscore(self.bincolumns, wildcard)
        return retval


def main() -> int:
    with open("../Inputfiles/aoc13.txt", "r") as file:
        patterns = file.read().strip("\n").split("\n\n")

    totalscore_p1 = 0
    totalscore_p2 = 0

    for pattern in patterns:
        newpattern = Pattern(pattern.split('\n'))
        totalscore_p1 += newpattern.getscore(True)
        totalscore_p2 += newpattern.getscore(False)
    print("Part1: ", totalscore_p1)
    print("Part2: ", totalscore_p2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
