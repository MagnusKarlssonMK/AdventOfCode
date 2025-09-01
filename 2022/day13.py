import time
from pathlib import Path
import re


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

    def issmallerthan(self, other: "ElfList") -> int:
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

    def __lt__(self, other: "ElfList") -> bool:
        return self.issmallerthan(other) != -1

    def __repr__(self):
        return str(self.list)


class DistressSignal:
    def __init__(self, rawstr: str) -> None:
        self.__pairs: list[tuple[ElfList, ElfList]] = []
        for pair in rawstr.split('\n\n'):
            left, right = pair.split('\n')
            self.__pairs.append((ElfList(left), ElfList(right)))

    def get_correct_order_index_sum(self) -> int:
        return sum([idx + 1 for idx, pair in enumerate(self.__pairs) if pair[0] < pair[1]])

    def get_decoder_key(self) -> int:
        all_packet_list: list[ElfList] = []
        for p1, p2 in self.__pairs:
            all_packet_list.append(p1)
            all_packet_list.append(p2)
        divider_two = ElfList('[[2]]')
        divider_six = ElfList('[[6]]')
        all_packet_list.append(divider_two)
        all_packet_list.append(divider_six)
        all_packet_list.sort()
        return (all_packet_list.index(divider_two) + 1) * (all_packet_list.index(divider_six) + 1)


def main(aoc_input: str) -> None:
    signal = DistressSignal(aoc_input)
    print(f"Part 1: {signal.get_correct_order_index_sum()}")
    print(f"Part 2: {signal.get_decoder_key()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2022/day13.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
