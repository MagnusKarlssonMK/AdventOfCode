"""
Part 1: Parse the input and store in a dict, use recursion to extrtact the root value.
Part 2: Remove 'humn' from the known dict, and update root operation to '-': root = lhs-rhs = 0
Then extract all the monkeys not dependent on 'humn' through recursion similar to Part 1 and add those to known dict.
Finally, add root=0 as a known value, then 'reverse' the remaining operations (all dict keys should now have one
known value on the 'items' side of the dict), then one final round of recursion to calculate the remaining values.

Note: The implementation for Part 2 is really messy and can likely be cleaned up significantly / add a bit of structure.
"""
import sys
from pathlib import Path
import operator

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day21.txt')


class MonkeyMath:
    __OPS = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.floordiv}
    __REV_OPS = {'+': '-', '-': '+', '*': '/', '/': '*'}

    def __init__(self, rawstr: str) -> None:
        self.__inputdata: dict[str: str] = {left: right for left, right in
                                            [line.split(': ')for line in rawstr.splitlines()]}
        self.__known: dict[str: int] = {}
        self.__unknown: dict[str: tuple[str, str, str]] = {}
        for m in self.__inputdata:
            if self.__inputdata[m].isdigit():
                self.__known[m] = int(self.__inputdata[m])
            else:
                left, op, right = self.__inputdata[m].split()
                self.__unknown[m] = (left, right, op)

    def get_yellnumber(self, monkey: str) -> int:
        known = dict(self.__known)
        unknown = dict(self.__unknown)

        def __extractvalue(m1: str, m2: str, operation: str) -> int:
            nbrs = []
            for n in (m1, m2):
                if n not in known:
                    known[n] = __extractvalue(*unknown[n])
                nbrs.append(known[n])
            return MonkeyMath.__OPS[operation](*nbrs)

        queue = list(unknown.keys())
        while queue:
            next_m = queue.pop(0)
            if next_m not in known:
                known[next_m] = __extractvalue(*unknown[next_m])
        return known[monkey]

    def get_humn_number(self) -> int:
        known = dict(self.__known)
        unknown = dict(self.__unknown)
        known.pop('humn')
        unknown['root'] = unknown['root'][0], unknown['root'][1], '-'

        def __extractnonhuman(m1: str, m2: str, operation: str) -> tuple[bool, int]:
            nbrs = []
            for n in (m1, m2):
                if n == 'humn':
                    return False, -1
                if n not in known:
                    f, v = __extractnonhuman(*unknown[n])
                    if f:
                        known[n] = v
                    else:
                        return False, -1
                nbrs.append(known[n])
            return True, MonkeyMath.__OPS[operation](*nbrs)

        # Evaluate the monkeys not dependent on 'humn'
        queue = list(unknown.keys())
        while queue:
            next_m = queue.pop(0)
            if next_m not in known:
                found, val = __extractnonhuman(*unknown[next_m])
                if found:
                    known[next_m] = val
                    unknown.pop(next_m)

        # Add the root to known and extract the remaining values from the reversed list
        known['root'] = 0
        reverse_unknown: dict[str: tuple[str, str, str]] = {}
        for k in unknown:
            l, r, o = unknown[k]
            if l not in known:
                reverse_unknown[l] = k, r, MonkeyMath.__REV_OPS[o]
            if r not in known:
                match o:
                    case '+':
                        reverse_unknown[r] = k, l, '-'
                    case '-':
                        reverse_unknown[r] = l, k, '-'
                    case '*':
                        reverse_unknown[r] = k, l, '/'
                    case '/':
                        reverse_unknown[r] = l, k, '/'

        def __extractvalue(m1: str, m2: str, operation: str) -> int:
            nbrs = []
            for n in (m1, m2):
                if n not in known:
                    known[n] = __extractvalue(*reverse_unknown[n])
                nbrs.append(known[n])
            return MonkeyMath.__OPS[operation](*nbrs)

        queue = list(reverse_unknown.keys())
        while queue:
            next_m = queue.pop(0)
            if next_m not in known:
                known[next_m] = __extractvalue(*reverse_unknown[next_m])
        return known['humn']


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        monkeymath = MonkeyMath(file.read().strip('\n'))
    print(f"Part 1: {monkeymath.get_yellnumber('root')}")
    print(f"Part 2: {monkeymath.get_humn_number()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
