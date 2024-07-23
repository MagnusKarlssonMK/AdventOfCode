"""
Using the shunting yard algorithm. For part 2, the only difference is to check whether the top item on the operator
stack has higher precedence before popping it and putting it on the output stack.
"""
import sys
import operator


OPMAP = {'+': operator.add, '*': operator.mul}


def shunting_yard(line: str, is_advanced: bool) -> int:
    # Generate the output buffer with shunting yard
    inp = list(line)
    output = []
    opstack = []
    while inp:
        c = inp.pop(0)
        if c.isdigit():
            output.append(int(c))
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
            v1 = evaluated.pop()
            v2 = evaluated.pop()
            evaluated.append(OPMAP[o](v1, v2))
        else:
            evaluated.append(o)
    return evaluated[0]


class Homework:
    def __init__(self, rawstr: str) -> None:
        self.__lines = rawstr.splitlines()

    def get_value_sum(self, isadvanced: bool = False) -> int:
        return sum([shunting_yard(line, isadvanced) for line in self.__lines])


def main() -> int:
    with open('../Inputfiles/aoc18.txt', 'r') as file:
        homework = Homework(file.read().strip('\n'))
    print(f"Part 1: {homework.get_value_sum()}")
    print(f"Part 2: {homework.get_value_sum(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
