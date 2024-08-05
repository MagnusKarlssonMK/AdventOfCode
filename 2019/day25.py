"""
I can't be bothered to try to parse and automate this, and besides it feels like part of the adventure to manually
play the game!
"""
import sys
from pathlib import Path
from intcode import Intcode, IntResult

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day25.txt')


class AsciiComputer:
    def __init__(self, rawstr: str) -> None:
        self.__cpu = Intcode(list(map(int, rawstr.split(','))))

    def rescue_santa(self) -> None:
        while True:
            val, res = self.__cpu.run_program()
            if res == IntResult.WAIT_INPUT:
                print('> ')
                userinput = sys.stdin.readline()
                for c in userinput:
                    self.__cpu.add_input(ord(c))
            elif res == IntResult.OUTPUT:
                sys.stdout.write(chr(val))
            else:
                break


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        computer = AsciiComputer(file.read().strip('\n'))
    computer.rescue_santa()
    return 0


if __name__ == "__main__":
    sys.exit(main())
