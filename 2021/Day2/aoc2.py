import sys


class Submarine:
    def __init__(self, init_x: int, init_y: int):
        self.x = init_x
        self.y = init_y

    def movecommand(self, direction: str, value: int):
        match direction:
            case 'up':
                self.y -= value
            case 'down':
                self.y += value
            case 'forward':
                self.x += value
            case _:
                pass

    def getscore(self) -> int:
        return self.x * self.y


class AimedSubmarine(Submarine):
    def __init__(self, init_x: int, init_y: int):
        self.__aim = 0
        super().__init__(init_x, init_y)

    def movecommand(self, direction: str, value: int):
        match direction:
            case 'up':
                self.__aim -= value
            case 'down':
                self.__aim += value
            case 'forward':
                self.x += value
                self.y += self.__aim * value
            case _:
                pass


def main() -> int:
    mysub = Submarine(0, 0)
    myaimedsub = AimedSubmarine(0, 0)
    with open('../Inputfiles/aoc2.txt', 'r') as file:
        lines = file.read().strip('\n').split('\n')
    for line in lines:
        direction, value = line.split()
        mysub.movecommand(direction, int(value))
        myaimedsub.movecommand(direction, int(value))
    print("Part 1: ", mysub.getscore())
    print("Part 2: ", myaimedsub.getscore())
    return 0


if __name__ == "__main__":
    sys.exit(main())
