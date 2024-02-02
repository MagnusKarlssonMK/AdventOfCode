import sys
import re


class ValveNetwork:
    def __init__(self, rawstr: str):
        self.__adjlist: dict[str: tuple[int, list[str]]] = {}
        for line in rawstr.splitlines():
            valves = re.findall(r'[A-Z]{2}', line.strip('Valve'))
            flow = int(re.findall(r'\d+', line)[0])
            self.__adjlist[valves[0]] = (flow, valves[1:])

    def getmaxflow(self) -> int:
        return 1


def main() -> int:
    with open('../Inputfiles/aoc16_example.txt', 'r') as file:
        myvalves = ValveNetwork(file.read().strip('\n'))
    p1 = myvalves.getmaxflow()
    print("Part1: ", p1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
