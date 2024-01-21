import re
import sys


def algo(mystring: str) -> int:
    retval = 0
    for char in mystring:
        retval += ord(char)
        retval *= 17
        retval %= 256
    return retval


class Lightmachine:
    def __init__(self):
        self.boxtable: dict[int: tuple[str, int]] = {}

    def insertelement(self, lensstring: str) -> None:
        label, operation, foc_len = re.findall(r"(\w+)([-|=])(\d+)?", lensstring)[0]
        hashed = algo(label)
        match operation:
            case '=':
                if hashed in list(self.boxtable.keys()):
                    for idx, item in enumerate(self.boxtable[hashed]):
                        if label == item[0]:
                            self.boxtable[hashed][idx] = label, int(foc_len)
                            break
                    else:
                        self.boxtable[hashed].append((label, int(foc_len)))
                else:
                    self.boxtable[hashed] = [(label, int(foc_len))]
            case '-':
                if hashed in list(self.boxtable.keys()):
                    for idx, item in enumerate(self.boxtable[hashed]):
                        if label == item[0]:
                            self.boxtable[hashed].pop(idx)

    def getlenspower(self) -> int:
        retval = 0
        for key in list(self.boxtable.keys()):
            retval += sum(lens[1] * (i + 1) * (key + 1) for i, lens in enumerate(self.boxtable[key]))
        return retval


def main() -> int:
    with open("aoc15.txt", "r") as file:
        words = file.readline().strip("\n").split(",")

    # Part 1
    totalsum_p1 = sum([algo(word) for word in words])
    print("Part1: ", totalsum_p1)

    # Part 2
    mymachine = Lightmachine()
    [mymachine.insertelement(word) for word in words]
    print("Part2: ", mymachine.getlenspower())
    return 0


if __name__ == "__main__":
    sys.exit(main())
