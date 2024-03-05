import sys


class Computer:
    def __init__(self):
        self.__bitmask = 0, 0
        self.__memory: dict[int: int] = {}

    def run_command(self, left: str, right: str) -> None:
        if left == 'mask':
            mask1 = ''
            mask2 = ''
            for i in range(len(right)):
                if right[i] == 'X':
                    mask1 += '1'
                    mask2 += '0'
                else:
                    mask1 += '0'
                    mask2 += right[i]
            self.__bitmask = int(mask1, 2), int(mask2, 2)
        else:
            mem = int(left.strip('mem[').strip(']'))
            val = int(right)
            self.__memory[mem] = (val & self.__bitmask[0]) | self.__bitmask[1]

    def get_memorysum(self) -> int:
        return sum(list(self.__memory.values()))


class ComputerV2:
    def __init__(self):
        self.__bitmask = ''
        self.__xmask = 0
        self.__memory: dict[int: int] = {}

    def run_command(self, left: str, right: str) -> None:
        if left == 'mask':
            self.__bitmask = right
            xmask = ''
            for c in self.__bitmask:
                if c == 'X':
                    xmask += '0'
                else:
                    xmask += '1'
            self.__xmask = int(xmask, 2)
        else:
            addr = int(left.strip('mem[').strip(']'))
            for mask in self.__mask_value(self.__bitmask):
                self.__memory[(addr & self.__xmask) | mask] = int(right)

    def __mask_value(self, val: str) -> list[int]:
        if (idx := val.find('X')) != -1:
            return (self.__mask_value(val[:idx] + '0' + val[idx + 1:]) +
                    self.__mask_value(val[:idx] + '1' + val[idx + 1:]))
        else:
            return [int(val, 2)]

    def get_memorysum(self) -> int:
        return sum(list(self.__memory.values()))


def main() -> int:
    mycomputer = Computer()
    myv2computer = ComputerV2()
    with open('../Inputfiles/aoc14.txt') as file:
        commands = file.read().strip('\n').splitlines()
    for line in commands:
        mycomputer.run_command(*line.split(' = '))
        myv2computer.run_command(*line.split(' = '))
    print("Part 1:", mycomputer.get_memorysum())
    print("Part 2:", myv2computer.get_memorysum())
    return 0


if __name__ == "__main__":
    sys.exit(main())
