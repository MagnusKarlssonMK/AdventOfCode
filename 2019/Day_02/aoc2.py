"""
Build a computer class to hold the data and run the program, with the ability to do a 'factory reset' to run through
all the different start values for Part 2.
"""
import sys


class Intcode:
    def __init__(self, program: list[int]):
        self.program: list[int] = list(program)
        self.__startprogram = list(program)
        self.__head: int = 0

    def set_initialstate(self, value1: int, value2: int) -> None:
        self.program[1] = value1
        self.program[2] = value2

    def reset_program(self) -> None:
        self.program = list(self.__startprogram)
        self.__head = 0

    def run_program(self) -> int:
        while self.__head < len(self.program):
            match self.program[self.__head]:
                case 99:
                    break
                case 1:
                    self.program[self.program[self.__head + 3]] = (self.program[self.program[self.__head + 1]] +
                                                                   self.program[self.program[self.__head + 2]])
                    self.__head += 4
                case 2:
                    self.program[self.program[self.__head + 3]] = (self.program[self.program[self.__head + 1]] *
                                                                   self.program[self.program[self.__head + 2]])
                    self.__head += 4
        return self.program[0]


def main() -> int:
    with open('../Inputfiles/aoc2.txt', 'r') as file:
        computer = Intcode(list(map(int, file.read().strip('\n').split(','))))
    computer.set_initialstate(12, 2)
    print("Part 1:", computer.run_program())
    computer.reset_program()

    for noun in range(100):
        for verb in range(100):
            computer.set_initialstate(noun, verb)
            if computer.run_program() == 19690720:
                print("Part 2:", noun * 100 + verb)
                break
            computer.reset_program()
        else:
            continue
        break
    return 0


if __name__ == "__main__":
    sys.exit(main())
