import time
from pathlib import Path
from math import prod


class Robot:
    def __init__(self, rawstr: str) -> None:
        left, right = rawstr.split()
        left_x, left_y = left.split(',')
        right_x, right_y = right.split(',')
        self.pos = int(left_x.strip('p=')), int(left_y)
        self.vel = int(right_x.strip('v=')), int(right_y)


class Security:
    def __init__(self, rawstr: str, x_max: int, y_max: int) -> None:
        self.__robots = [Robot(r) for r in rawstr.splitlines()]
        self.__x_max = x_max
        self.__y_max = y_max

    def get_safety_factor(self) -> int:
        middle_x = (self.__x_max - 1) // 2
        middle_y = (self.__y_max - 1) // 2
        quadrants = [0, 0, 0, 0]
        for r in self.__robots:
            x_100 = (r.pos[0] + 100 * r.vel[0]) % self.__x_max
            y_100 = (r.pos[1] + 100 * r.vel[1]) % self.__y_max
            if x_100 != middle_x and y_100 != middle_y:
                quadrants[x_100 // (middle_x + 1) + 2 * (y_100 // (middle_y + 1))] += 1
        return prod(quadrants)

    def get_egg_seconds(self) -> int:
        points: set[tuple[int, int]] = set()
        time = 0
        overlap = True
        while overlap:
            time += 1
            overlap = False
            for r in self.__robots:
                newpoint_x = (r.pos[0] + time * r.vel[0]) % self.__x_max
                newpoint_y = (r.pos[1] + time * r.vel[1]) % self.__y_max
                if (newpoint_x, newpoint_y) in points:
                    overlap = True
                    break
                else:
                    points.add((newpoint_x, newpoint_y))
            points.clear()
        return time


def main(aoc_input: str) -> None:
    sec = Security(aoc_input, 101, 103)
    print(f"Part 1: {sec.get_safety_factor()}")
    print(f"Part 2: {sec.get_egg_seconds()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/day14.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
