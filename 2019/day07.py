"""
Taking the Intcode from day 5, but rewriting it to be persistent.
Using permutations to generate the combinations of amp settings.
"""
import sys
from enum import Enum
from itertools import permutations


class OpCode(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    HALT = 99


class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1


class Intcode:
    def __init__(self, rawstr: str) -> None:
        self.__program = [int(nbr) for nbr in rawstr.split(',')]
        self.__startstate = list(self.__program)
        self.__inputbuffer = []
        self.__head = 0

    def reboot(self) -> None:
        self.__program = list(self.__startstate)
        self.__inputbuffer = []
        self.__head = 0

    def add_input(self, value: int) -> None:
        self.__inputbuffer.append(value)

    def run_program(self) -> tuple[int, bool]:
        def __get_value(m: Mode, param: int) -> int:
            if m == Mode.POSITION:
                return self.__program[param]
            elif m == Mode.IMMEDIATE:
                return param
            return -1

        while 0 <= self.__head < len(self.__program):
            op = self.__program[self.__head]
            modes = [0, 0, 0]
            modes[2] = Mode(op // 10000)
            op %= 10000
            modes[1] = Mode(op // 1000)
            op %= 1000
            modes[0] = Mode(op // 100)
            op_code = OpCode(op % 100)
            p = self.__program[self.__head + 1: self.__head + 4]
            match op_code:
                case OpCode.ADD:
                    self.__program[p[2]] = __get_value(modes[0], p[0]) + __get_value(modes[1], p[1])
                    self.__head += 4
                case OpCode.MULTIPLY:
                    self.__program[p[2]] = __get_value(modes[0], p[0]) * __get_value(modes[1], p[1])
                    self.__head += 4
                case OpCode.INPUT:
                    if self.__inputbuffer:
                        self.__program[p[0]] = self.__inputbuffer.pop(0)
                        self.__head += 2
                    else:
                        print("Input buffer empty")
                        return -1, True
                case OpCode.OUTPUT:
                    self.__head += 2
                    return __get_value(modes[0], p[0]), False
                case OpCode.JUMP_IF_TRUE:
                    if __get_value(modes[0], p[0]) != 0:
                        self.__head = __get_value(modes[1], p[1])
                    else:
                        self.__head += 3
                case OpCode.JUMP_IF_FALSE:
                    if not __get_value(modes[0], p[0]):
                        self.__head = __get_value(modes[1], p[1])
                    else:
                        self.__head += 3
                case OpCode.LESS_THAN:
                    self.__program[p[2]] = 1 if __get_value(modes[0], p[0]) < __get_value(modes[1], p[1]) else 0
                    self.__head += 4
                case OpCode.EQUALS:
                    self.__program[p[2]] = 1 if __get_value(modes[0], p[0]) == __get_value(modes[1], p[1]) else 0
                    self.__head += 4
                case OpCode.HALT:
                    break
        return -1, True


class AmplifierArray:
    def __init__(self, rawstr: str) -> None:
        self.__amps = [Intcode(rawstr) for _ in range(5)]

    def get_max_thruster_signal(self) -> int:
        result = 0
        for phase_inputs in permutations(range(0, 5)):
            out = 0
            for i, p_i in enumerate(phase_inputs):
                self.__amps[i].add_input(p_i)
                self.__amps[i].add_input(out)
                out, _ = self.__amps[i].run_program()
                self.__amps[i].reboot()
            result = max(result, out)
        return result

    def get_max_feedback_loop_signal(self) -> int:
        result = 0
        for phase_inputs in permutations(range(5, 10)):
            for i, amp in enumerate(self.__amps):
                amp.reboot()
                amp.add_input(phase_inputs[i])
            out = 0
            amp = 0
            done = False
            while not done:
                self.__amps[amp].add_input(out)
                outval, done = self.__amps[amp].run_program()
                if not done:
                    out = outval
                amp = (amp + 1) % len(self.__amps)
            result = max(result, out)
        return result


def main() -> int:
    with open('../Inputfiles/aoc7.txt', 'r') as file:
        amps = AmplifierArray(file.read().strip('\n'))
    print(f"Part 1: {amps.get_max_thruster_signal()}")
    print(f"Part 2: {amps.get_max_feedback_loop_signal()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
