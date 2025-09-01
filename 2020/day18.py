"""
Using the shunting yard algorithm. For part 2, the only difference is to check whether the top item on the operator
stack has higher precedence before popping it and putting it on the output stack.
"""
import time
from pathlib import Path
import operator


OPMAP = {'+': operator.add, '*': operator.mul}


def shunting_yard(line: str, is_advanced: bool) -> int:
    # Generate the output buffer with shunting yard
    output: list[str] = []
    opstack: list[str] = []
    for c in line:
        if c.isdigit():
            output.append(c)
        elif c in OPMAP:
            while opstack:
                if opstack[-1] != '(' and (not is_advanced or not (opstack[-1] == '*' and c == '+')):
                    output.append(opstack.pop())
                else:
                    break
            opstack.append(c)
        elif c == '(':
            opstack.append(c)
        elif c == ')':
            while (o := opstack.pop()) != '(':
                output.append(o)
    while opstack:
        output.append(opstack.pop())
    # Evaluate the output buffer
    evaluated = []
    while output:
        o = output.pop(0)
        if o in OPMAP:
            v1 = int(evaluated.pop())
            v2 = int(evaluated.pop())
            evaluated.append(OPMAP[o](v1, v2))
        else:
            evaluated.append(o)
    return evaluated[0]


class Homework:
    def __init__(self, rawstr: str) -> None:
        self.__lines = rawstr.splitlines()

    def get_value_sum(self, isadvanced: bool = False) -> int:
        return sum([shunting_yard(line, isadvanced) for line in self.__lines])


def main(aoc_input: str) -> None:
    homework = Homework(aoc_input)
    print(f"Part 1: {homework.get_value_sum()}")
    print(f"Part 2: {homework.get_value_sum(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day18.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
