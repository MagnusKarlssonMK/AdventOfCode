import sys


class Directions:
    def __init__(self, rawstr: str) -> None:
        self.__steps = [1 if c == '(' else -1 for c in rawstr]

    def get_final_floor(self) -> int:
        return sum(self.__steps)

    def get_basement_step(self) -> int:
        floor = 0
        for i, v in enumerate(self.__steps):
            floor += v
            if floor < 0:
                return i + 1
        return -1


def main() -> int:
    with open('../Inputfiles/aoc1.txt', 'r') as file:
        directions = Directions(file.read().strip('\n'))
    print(f"Part 1: {directions.get_final_floor()}")
    print(f"Part 2: {directions.get_basement_step()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
