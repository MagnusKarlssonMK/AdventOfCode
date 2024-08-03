import sys


class CPU:
    def __init__(self, intervals: list[int]):
        self.cyclenbr = 0
        self.x = 1
        self.commandqueue: list[tuple[str, int]] = []
        self.reportintervals = intervals

    def addcommand(self, command: str):
        if len(cmd := command.split()) > 1:
            self.commandqueue.append((cmd[0], int(cmd[1])))
        else:
            self.commandqueue.append((cmd[0], 0))

    def processqueue(self) -> iter:
        processcount = 0
        currentcmd = ('', 0)
        crt_string = ""
        while len(self.commandqueue) > 0 or processcount > 0:
            self.cyclenbr += 1
            if abs(self.x - ((self.cyclenbr - 1) % 40)) <= 1:
                crt_string += "#"
            else:
                crt_string += "."
            if processcount == 0:
                if len(self.commandqueue) > 0:
                    currentcmd = self.commandqueue.pop(0)
                    processcount = 1 if currentcmd[0] == 'noop' else 2
            processcount -= 1
            if self.cyclenbr in self.reportintervals:
                yield self.x * self.cyclenbr, crt_string + '\n'
                crt_string = ""
            if processcount == 0 and currentcmd[0] == 'addx':
                self.x += currentcmd[1]


def main() -> int:
    mycpu1 = CPU([20, 60, 100, 140, 180, 220])
    mycpu2 = CPU([40, 80, 120, 160, 200, 240])
    with open('../Inputfiles/aoc10.txt', 'r') as file:
        for line in file.read().strip('\n').splitlines():
            mycpu1.addcommand(line)
            mycpu2.addcommand(line)

    value_count = sum([i[0] for i in mycpu1.processqueue()])
    print("Part1:", value_count, '\n')
    crt = "".join([i[1] for i in mycpu2.processqueue()])
    print(crt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
