"""
"""
import sys
from pathlib import Path
from dataclasses import dataclass
from intcode import Intcode, IntResult

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day23.txt')


@dataclass
class Computer:
    cpu: Intcode
    output_buffer: list[int]
    input_buffer: list[tuple[int, int]]


class Network:
    def __init__(self, rawstr: str) -> None:
        nic = list(map(int, rawstr.split(',')))
        self.__computers = {i: Computer(Intcode(nic), [], []) for i in range(50)}

    def get_first_packets_y_value(self) -> tuple[int, int]:
        [self.__computers[i].cpu.add_input(i) for i, _ in enumerate(self.__computers)]
        i = -1
        p1 = p2 = None
        nat = None
        nat_previous_y = -1
        network_idle = True
        while not p1 or not p2:
            i = (i + 1) % len(self.__computers)
            if i == 0:
                if network_idle and nat:
                    x = nat.pop(0)
                    y = nat.pop(0)
                    self.__computers[0].cpu.add_input(x)
                    self.__computers[0].cpu.add_input(y)
                    network_idle = False
                    if y == nat_previous_y:
                        p2 = y
                        break
                    else:
                        nat_previous_y = y
                else:
                    network_idle = True
            while True:
                val, res = self.__computers[i].cpu.run_program()
                if res == IntResult.OUTPUT:
                    self.__computers[i].output_buffer.append(val)
                    if len(self.__computers[i].output_buffer) == 3:
                        dest = self.__computers[i].output_buffer.pop(0)
                        x = self.__computers[i].output_buffer.pop(0)
                        y = self.__computers[i].output_buffer.pop(0)
                        if dest == 255:
                            if not p1:
                                p1 = y
                            nat = [x, y]
                        else:
                            self.__computers[dest].input_buffer.append((x, y))
                            network_idle = False
                elif res == IntResult.WAIT_INPUT:
                    if self.__computers[i].input_buffer:
                        x, y = self.__computers[i].input_buffer.pop(0)
                        self.__computers[i].cpu.add_input(x)
                        self.__computers[i].cpu.add_input(y)
                        network_idle = False
                    else:
                        self.__computers[i].cpu.add_input(-1)
                    break
                else:
                    print("halted", i)
                    break
        return p1, p2


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        net = Network(file.read().strip('\n'))
    p1, p2 = net.get_first_packets_y_value()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
