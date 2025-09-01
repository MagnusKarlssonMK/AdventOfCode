"""
Another assembly simulator of sorts. Nothing special about part 1, but a bit more tricky with part 2 since we now have
two programs running in parallel and communcicating with messages. Mostly just a matter of having two instances of
everything, keeping track of the progam states and toggling the 'running' program.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Instr:
    op: str
    attr1: str = None
    attr2: str = None


class State(Enum):
    IDLE = 1
    RECEIVING = 2
    DONE = 3


class Register:
    def __init__(self, regs: set[str], pval: int) -> None:
        self.__regs: dict[str, int] = {r: 0 for r in regs}
        self.__regs['p'] = pval

    def get_value(self, attr: str) -> int:
        if attr in self.__regs:
            return self.__regs[attr]
        return int(attr)

    def set_value(self, reg: str, val: int) -> None:
        self.__regs[reg] = val

    def add_value(self, reg: str, val: int) -> None:
        self.__regs[reg] += val

    def mul_value(self, reg: str, val: int) -> None:
        self.__regs[reg] *= val

    def mod_value(self, reg: str, val: int) -> None:
        self.__regs[reg] %= val


class Duet:
    def __init__(self, rawstr: str) -> None:
        self.__registers: set[str] = set()
        self.__instr: list[Instr] = []
        for line in rawstr.splitlines():
            t = line.split()
            self.__instr.append(Instr(*t))
            for w in t[1:]:
                if not w[-1].isdigit():
                    self.__registers.add(w)

    def get_recovered_freq(self) -> int:
        sp = 0
        regs = Register(self.__registers, 0)
        sound = None
        while 0 <= sp < len(self.__instr):
            i = self.__instr[sp]
            match i.op:
                case 'snd':
                    sound = regs.get_value(i.attr1)
                case 'set':
                    regs.set_value(i.attr1, regs.get_value(i.attr2))
                case 'add':
                    regs.add_value(i.attr1, regs.get_value(i.attr2))
                case 'mul':
                    regs.mul_value(i.attr1, regs.get_value(i.attr2))
                case 'mod':
                    regs.mod_value(i.attr1, regs.get_value(i.attr2))
                case 'rcv':
                    if regs.get_value(i.attr1) != 0 and sound:
                        return sound
                case 'jgz':
                    if regs.get_value(i.attr1) > 0:
                        sp += regs.get_value(i.attr2)
                        continue
                case _:
                    pass
            sp += 1
        return -1

    def get_duet_send_count(self) -> int:
        sp = [0, 0]
        regs = [Register(self.__registers, 0), Register(self.__registers, 1)]
        states = [State.IDLE, State.IDLE]
        inbox: list[list[int]] = [[], []]
        running = 0
        send_count = 0
        while states[running] == State.IDLE or (states[running] == State.RECEIVING and inbox[running]):
            i = self.__instr[sp[running]]
            match i.op:
                case 'snd':
                    inbox[(running + 1) % 2].append(regs[running].get_value(i.attr1))
                    sp[running] += 1
                    if running == 1:
                        send_count += 1
                case 'set':
                    regs[running].set_value(i.attr1, regs[running].get_value(i.attr2))
                    sp[running] += 1
                case 'add':
                    regs[running].add_value(i.attr1, regs[running].get_value(i.attr2))
                    sp[running] += 1
                case 'mul':
                    regs[running].mul_value(i.attr1, regs[running].get_value(i.attr2))
                    sp[running] += 1
                case 'mod':
                    regs[running].mod_value(i.attr1, regs[running].get_value(i.attr2))
                    sp[running] += 1
                case 'rcv':
                    if inbox[running]:
                        regs[running].set_value(i.attr1, regs[running].get_value(inbox[running].pop(0)))
                        states[running] = State.IDLE
                        sp[running] += 1
                    else:
                        states[running] = State.RECEIVING
                        running = (running + 1) % 2
                case 'jgz':
                    if regs[running].get_value(i.attr1) > 0:
                        sp[running] += regs[running].get_value(i.attr2)
                    else:
                        sp[running] += 1
                case _:
                    pass
            if not 0 <= sp[running] < len(self.__instr):
                states[running] = State.DONE
                running = (running + 1) % 2
        return send_count


def main(aoc_input: str) -> None:
    duet = Duet(aoc_input)
    print(f"Part 1: {duet.get_recovered_freq()}")
    print(f"Part 2: {duet.get_duet_send_count()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day18.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
