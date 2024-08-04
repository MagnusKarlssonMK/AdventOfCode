import sys
from pathlib import Path
import re

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day13.txt')


def get_cbi(inputstr: str) -> int:
    """Analyzes a string starting with '[' in the first character and returns the Closing Bracket Index of the
    corresponding closing ']' bracket. Returns -1 if not found in string or first character is not a bracket."""
    if len(inputstr) < 2 or inputstr[0] != '[':
        return -1
    count = 0
    for idx, c in enumerate(inputstr):
        if c == '[':
            count += 1
        elif c == ']':
            count -= 1
        if count == 0:
            return idx
    return -1


class ElfList:
    """Constructor takes the AOC input in string format and parses it into list data. Comparison operators can be used
    to compare different list objects according to the AOC rules."""
    def __init__(self, strlist: str) -> None:
        """Assumes that the string has '[' in the first character and ']' in the last."""
        self.list = []
        i = 1
        while i < (len(strlist) - 1):
            if strlist[i] == '[':
                cbi = i + get_cbi(strlist[i:])
                self.list.append(ElfList(strlist[i:1+cbi]))
                i = cbi
            elif strlist[i].isdigit():
                nbr = re.findall(r"\d+", strlist[i:])[0]
                self.list.append(int(nbr))
                i += len(nbr)
            else:
                i += 1

    def issmallerthan(self, other) -> int:
        for i in range(min(len(self.list), len(other.list))):
            if isinstance(self.list[i], int):
                if isinstance(other.list[i], int):
                    if self.list[i] < other.list[i]:
                        return 1
                    if self.list[i] > other.list[i]:
                        return -1
                else:
                    newlist = ElfList('['+str(self.list[i])+']')
                    test = newlist.issmallerthan(other.list[i])
                    if test != 0:
                        return test
            elif isinstance(other.list[i], int):
                newlist = ElfList('['+str(other.list[i])+']')
                test = self.list[i].issmallerthan(newlist)
                if test != 0:
                    return test
            else:
                test = self.list[i].issmallerthan(other.list[i])
                if test != 0:
                    return test
        if len(self.list) < len(other.list):
            return 1
        if len(self.list) > len(other.list):
            return -1
        return 0

    def __lt__(self, other) -> bool:
        return self.issmallerthan(other) != -1

    def __repr__(self):
        return str(self.list)


def main() -> int:
    pairs: list[tuple[ElfList, ElfList]] = []
    with open(INPUT_FILE, 'r') as file:
        for pair in file.read().strip('\n').split('\n\n'):
            left, right = pair.split('\n')
            pairs.append((ElfList(left), ElfList(right)))

    print(f"Part 1: {sum([idx + 1 for idx, pair in enumerate(pairs) if pair[0] < pair[1]])}")

    allpacketlist = []
    for packet in pairs:
        allpacketlist.append(packet[0])
        allpacketlist.append(packet[1])
    divider_two = ElfList('[[2]]')
    divider_six = ElfList('[[6]]')
    allpacketlist.append(divider_two)
    allpacketlist.append(divider_six)
    allpacketssorted = sorted(allpacketlist)

    print(f"Part 2: {(allpacketssorted.index(divider_two) + 1) * (allpacketssorted.index(divider_six) + 1)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
