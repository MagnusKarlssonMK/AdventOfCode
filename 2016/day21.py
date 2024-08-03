"""
Part 1: Mostly straightforward, just parse and store the operations in a generic format and call corresponding
functions on a password class when iterating through the list later.

Part 2: Same thing but in reverse, kind of. Mostly the 'rotate position' operation is a bit funky to reverse; there
might be some more clever way to do this, but basically just try and rotate left one step at a time and see if that
would result in the correct result, and that way we will eventually find the origin string that generated the
result from calling this operation.
"""
import sys
from dataclasses import dataclass
from enum import Enum


class Instr(Enum):
    SWAP_POS = 0
    SWAP_LETTER = 1
    ROTATE = 2
    ROTATE_POS = 3
    REVERSE_POS = 4
    MOVE_POS = 5


@dataclass(frozen=True)
class Operation:
    instr: Instr
    attr1: str = None
    attr2: str = None


@dataclass
class Password:
    pwd: str

    def swap_pos(self, idx1: int, idx2: int) -> None:
        p = [c for c in self.pwd]
        tmp = p[idx1]
        p[idx1] = p[idx2]
        p[idx2] = tmp
        self.pwd = ''.join(p)

    def swap_letter(self, c1: str, c2: str) -> None:
        self.swap_pos(self.pwd.index(c1), self.pwd.index(c2))

    def rotate(self, steps: int) -> None:
        offset = steps % len(self.pwd)
        self.pwd = self.pwd[offset:] + self.pwd[:offset]

    def rotate_pos(self, c1: str) -> None:
        idx = self.pwd.index(c1) + 1
        if idx >= 5:
            idx += 1
        self.rotate(-idx)

    def rotate_pos_reverse(self, c1: str) -> None:
        for i, _ in enumerate(self.pwd):
            tmp = Password(self.pwd)
            # make a temporary copy of the password, try and rotate it 'i' steps and see if rotate_pos will bring it
            # back to where it was.
            tmp.rotate(i)
            p = tmp.pwd
            tmp.rotate_pos(c1)
            if tmp.pwd == self.pwd:
                self.pwd = p
                break

    def reverse_pos(self, idx1: int, idx2: int) -> None:
        self.pwd = self.pwd[:idx1] + ''.join(reversed(self.pwd[idx1: idx2 + 1])) + self.pwd[idx2 + 1:]

    def move_pos(self, idx1: int, idx2: int) -> None:
        tmp = [c for c in self.pwd]
        c = tmp.pop(idx1)
        tmp.insert(idx2, c)
        self.pwd = ''.join(tmp)


class Scrambler:
    def __init__(self, rawstr: str) -> None:
        self.__operations: list[Operation] = []
        for line in rawstr.splitlines():
            tokens = line.split()
            match tokens[0]:
                case 'swap':
                    if tokens[1] == 'position':
                        self.__operations.append(Operation(Instr.SWAP_POS, tokens[2], tokens[5]))
                    else:
                        self.__operations.append(Operation(Instr.SWAP_LETTER, tokens[2], tokens[5]))
                case 'rotate':
                    if tokens[1] == 'left':
                        self.__operations.append(Operation(Instr.ROTATE, tokens[2]))
                    elif tokens[1] == 'right':
                        self.__operations.append(Operation(Instr.ROTATE, '-' + tokens[2]))
                    else:
                        self.__operations.append(Operation(Instr.ROTATE_POS, tokens[6]))
                case 'reverse':
                    self.__operations.append(Operation(Instr.REVERSE_POS, tokens[2], tokens[4]))
                case 'move':
                    self.__operations.append((Operation(Instr.MOVE_POS, tokens[2], tokens[5])))

    def get_scrambled_string(self, start: str) -> str:
        scrambled = Password(start)
        for op in self.__operations:
            match op.instr:
                case Instr.SWAP_POS:
                    scrambled.swap_pos(int(op.attr1), int(op.attr2))
                case Instr.SWAP_LETTER:
                    scrambled.swap_letter(op.attr1, op.attr2)
                case Instr.ROTATE:
                    scrambled.rotate(int(op.attr1))
                case Instr.ROTATE_POS:
                    scrambled.rotate_pos(op.attr1)
                case Instr.REVERSE_POS:
                    scrambled.reverse_pos(int(op.attr1), int(op.attr2))
                case Instr.MOVE_POS:
                    scrambled.move_pos(int(op.attr1), int(op.attr2))
        return scrambled.pwd

    def get_descrambled_string(self, start: str) -> str:
        descrambled = Password(start)
        for op in reversed(self.__operations):
            match op.instr:
                case Instr.SWAP_POS:
                    descrambled.swap_pos(int(op.attr1), int(op.attr2))
                case Instr.SWAP_LETTER:
                    descrambled.swap_letter(op.attr1, op.attr2)
                case Instr.ROTATE:
                    descrambled.rotate(-int(op.attr1))
                case Instr.ROTATE_POS:
                    descrambled.rotate_pos_reverse(op.attr1)
                case Instr.REVERSE_POS:
                    descrambled.reverse_pos(int(op.attr1), int(op.attr2))
                case Instr.MOVE_POS:
                    descrambled.move_pos(int(op.attr2), int(op.attr1))
        return descrambled.pwd


def main() -> int:
    with open('../Inputfiles/aoc21.txt', 'r') as file:
        scrambler = Scrambler(file.read().strip('\n'))
    print(f"Part 1: {scrambler.get_scrambled_string('abcdefgh')}")
    print(f"Part 2: {scrambler.get_descrambled_string('fbgdceah')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
