"""
Store the wires in a dict and use operator class to represent gates, then get the answer recursively.
"""
import time
from pathlib import Path
from dataclasses import dataclass
import operator


@dataclass
class Gate:
    op: operator
    values: list[str]


class Circuit:
    def __init__(self, rawstr: str) -> None:
        self.__wires: dict[str, Gate] = {}
        self.__cache: dict[str, int] = {}
        for line in rawstr.splitlines():
            left, right = line.split(' -> ')
            l_tokens = left.split()
            if left.find('NOT') >= 0:
                self.__wires[right] = Gate(operator.invert, [l_tokens[1]])
            elif left.find('AND') >= 0:
                self.__wires[right] = Gate(operator.and_, [l_tokens[0], l_tokens[2]])
            elif left.find('OR') >= 0:
                self.__wires[right] = Gate(operator.or_, [l_tokens[0], l_tokens[2]])
            elif left.find('RSHIFT') >= 0:
                self.__wires[right] = Gate(operator.rshift, [l_tokens[0], l_tokens[2]])
            elif left.find('LSHIFT') >= 0:
                self.__wires[right] = Gate(operator.lshift, [l_tokens[0], l_tokens[2]])
            else:
                self.__wires[right] = Gate(None, [left])

    def __get_value(self, wire: str) -> int:
        if wire in self.__cache:
            return self.__cache[wire]
        values: list[int] = []
        for v in self.__wires[wire].values:
            if v.isdigit():
                values.append(int(v))
            else:
                values.append(self.__get_value(v))
        if self.__wires[wire].op:
            retval = self.__wires[wire].op(*values)
        else:
            retval = values[0]
        self.__cache[wire] = retval
        return retval

    def get_a_wire_value(self, override_b: bool = False) -> int:
        if override_b:
            a = self.__cache['a']
            self.__cache.clear()
            self.__cache['b'] = a
        retval = self.__get_value('a')
        return retval


def main(aoc_input: str) -> None:
    mycircuit = Circuit(aoc_input)
    print(f"Part 1: {mycircuit.get_a_wire_value()}")
    print(f"Part 2: {mycircuit.get_a_wire_value(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day07.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
