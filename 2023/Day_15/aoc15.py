import sys
import re
from dataclasses import dataclass


def algo(mystring: str) -> int:
    retval = 0
    for char in mystring:
        retval += ord(char)
        retval *= 17
        retval %= 256
    return retval


@dataclass(frozen=True)
class Box:
    label: str
    focuslen: int


class Lightmachine:
    def __init__(self, rawstr: str) -> None:
        self.__boxes: dict[int: list[Box]] = {}
        self.__words = rawstr.split(',')
        for word in self.__words:
            label, operation, foc_len = re.findall(r"(\w+)([-|=])(\d+)?", word)[0]
            hash_val = algo(label)
            match operation:
                case '=':
                    if hash_val in self.__boxes:
                        for idx, box in enumerate(self.__boxes[hash_val]):
                            if box.label == label:
                                self.__boxes[hash_val][idx] = Box(label, int(foc_len))
                                break
                        else:
                            self.__boxes[hash_val].append(Box(label, int(foc_len)))
                    else:
                        self.__boxes[hash_val] = [Box(label, int(foc_len))]
                case '-':
                    if hash_val in self.__boxes:
                        for idx, box in enumerate(self.__boxes[hash_val]):
                            if box.label == label:
                                self.__boxes[hash_val].pop(idx)

    def get_initialization_sum(self) -> int:
        return sum([algo(word) for word in self.__words])

    def get_lenspower(self) -> int:
        retval = 0
        for hash_val in self.__boxes:
            retval += sum(box.focuslen * (i + 1) * (hash_val + 1) for i, box in enumerate(self.__boxes[hash_val]))
        return retval


def main() -> int:
    with open('../Inputfiles/aoc15.txt', 'r') as file:
        mymachine = Lightmachine(file.read().strip('\n'))
    print(f"Part 1: {mymachine.get_initialization_sum()}")
    print(f"Part 2: {mymachine.get_lenspower()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
