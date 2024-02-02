import sys


def get_most_and_least_common(inlist: list[str]) -> tuple[str, str]:
    gamma = [0 for _ in range(len(inlist[0]))]
    for line in inlist:
        for i, c in enumerate(line):
            gamma[i] += int(c)
    for i in range(len(gamma)):
        gamma[i] = 2 * gamma[i] // len(inlist)
    epsilon = [(i + 1) % 2 for i in gamma]
    return "".join(list(map(str, gamma))), "".join(list(map(str, epsilon)))


class Diagnostics:
    def __init__(self, rawstr: str):
        self.__lines = rawstr.splitlines()
        self.__mostcommon = ""
        self.__leastcommon = ""

    def getpowerconsumption(self) -> int:
        self.__mostcommon, self.__leastcommon = get_most_and_least_common(self.__lines)
        return int(self.__mostcommon, 2) * int(self.__leastcommon, 2)

    def getlifesupportrating(self) -> int:
        return self.__getrating(0) * self.__getrating(1)

    def __getrating(self, most_least: int) -> int:
        nbrlist = self.__lines.copy()
        for i in range(len(nbrlist[0])):
            if len(nbrlist) <= 1:
                break
            bufferlist = []
            matchnbr = get_most_and_least_common(nbrlist)
            for line in nbrlist:
                if line[i] == matchnbr[most_least][i]:
                    bufferlist.append(line)
            nbrlist = bufferlist.copy()
        return int(nbrlist[0], 2)


def main() -> int:
    with open('../Inputfiles/aoc3.txt', 'r') as file:
        mydiag = Diagnostics(file.read().strip('\n'))
    print("Part 1: ", mydiag.getpowerconsumption())
    print("Part 2: ", mydiag.getlifesupportrating())
    return 0


if __name__ == "__main__":
    sys.exit(main())
