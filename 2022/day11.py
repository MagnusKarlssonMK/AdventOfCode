import math
import sys
import re


class Monkey:
    def __init__(self, rawstr: str, applyrelief: bool):
        lines = rawstr.splitlines()
        self.monkeyid = int(re.findall(r'\d+', lines[0])[0])
        self.items = list(map(int, re.findall(r'\d+', lines[1])))
        _, self.operation = lines[2].split(' = ')
        self.testdiv = int(re.findall(r'\d+', lines[3])[0])
        self.truemonkey = int(re.findall(r'\d+', lines[4])[0])
        self.falsemonkey = int(re.findall(r'\d+', lines[5])[0])
        self.inspectioncount = 0
        self.applyrelief = applyrelief

    def inspectitems(self, lcm: int = 1) -> iter:  # Monkey ID, item level
        retlist = []
        while len(self.items) > 0:
            currentitem = self.items.pop(0)
            self.inspectioncount += 1
            left, op, right = self.operation.split()
            nbr = [0, 0]
            for i, n in enumerate([left, right]):
                nbr[i] = currentitem if not n.isdigit() else int(n)
            if op == '+':
                currentitem = nbr[0] + nbr[1]
            elif op == '*':
                currentitem = nbr[0] * nbr[1]
            if self.applyrelief:
                currentitem = currentitem // 3
            else:
                currentitem %= lcm
            if currentitem % self.testdiv == 0:
                yield self.truemonkey, currentitem
            else:
                yield self.falsemonkey, currentitem
        return retlist

    def catchitem(self, newitem: int):
        self.items.append(newitem)

    def __str__(self):
        return (f"ID: {self.monkeyid}\n   Items: {self.items}\n   Op: {self.operation}\n   Testdiv: {self.testdiv}\n   "
                f"True: {self.truemonkey}\n   False: {self.falsemonkey}\n   Count: {self.inspectioncount}\n")


def main() -> int:
    monkeys_p1: list[Monkey] = []
    monkeys_p2: list[Monkey] = []
    with open('../Inputfiles/aoc11.txt', 'r') as file:
        for monk in file.read().strip('\n').split('\n\n'):
            monkeys_p1.append(Monkey(monk, True))
            monkeys_p2.append(Monkey(monk, False))

    for _ in range(20):
        for monkey in monkeys_p1:
            for item in monkey.inspectitems():
                monkeys_p1[item[0]].catchitem(item[1])

    countlist = sorted([monkey.inspectioncount for monkey in monkeys_p1], reverse=True)
    print("Part 1: ", countlist[0] * countlist[1])

    lcm = math.lcm(*[m.testdiv for m in monkeys_p2])

    for _ in range(10000):
        for monkey in monkeys_p2:
            for item in monkey.inspectitems(lcm):
                monkeys_p2[item[0]].catchitem(item[1])

    countlist = sorted([monkey.inspectioncount for monkey in monkeys_p2], reverse=True)
    print("Part 1: ", countlist[0] * countlist[1])

    return 0


if __name__ == "__main__":
    sys.exit(main())
