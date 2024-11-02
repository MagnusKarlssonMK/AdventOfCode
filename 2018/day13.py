"""
Store the carts and make them sortable, and keep the grid in a dict to easily be able to find the track for a certain
point.
For part 1, keep moving step-by-step until first collision is registered.
For part 2, keep going until there is only one cart left.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from copy import deepcopy


@dataclass(frozen=True)
class Point:
    row: int
    col: int

    def rotate_left(self) -> "Point":
        return Point(-self.col, self.row)

    def rotate_right(self) -> "Point":
        return Point(self.col, -self.row)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.row + other.row, self.col + other.col)

    def __lt__(self, other: "Point") -> bool:
        return self.row < other.row if self.row != other.row else self.col < other.col


class Cart:
    __FACING_MAP = {'<': Point(0, -1), '>': Point(0, 1), '^': Point(-1, 0), 'v': Point(1, 0)}

    def __init__(self, point: Point, facing: str) -> None:
        self.__pos = point
        self.__facing: Point = Cart.__FACING_MAP[facing]
        self.__turncount = 0

    def move(self) -> Point:
        self.__pos += self.__facing
        return self.__pos

    def update_rotation(self, track: str) -> None:
        match track:
            case '+':
                if self.__turncount == 0:
                    self.__facing = self.__facing.rotate_left()
                elif self.__turncount == 2:
                    self.__facing = self.__facing.rotate_right()
                self.__turncount = (self.__turncount + 1) % 3
            case '/':
                if self.__facing.row == 0:
                    self.__facing = self.__facing.rotate_left()
                else:
                    self.__facing = self.__facing.rotate_right()
            case '\\':
                if self.__facing.row == 0:
                    self.__facing = self.__facing.rotate_right()
                else:
                    self.__facing = self.__facing.rotate_left()

    def get_pos(self) -> Point:
        return self.__pos

    def __lt__(self, other: "Cart") -> bool:
        return self.__pos < other.__pos

    def __repr__(self):
        return f"Cartpos: {self.__pos}, Facing: {self.__facing}"


class TrackSystem:
    def __init__(self, rawstr: str) -> None:
        self.__carts = set()
        self.__tracks: dict[Point: str] = {}
        for row, line in enumerate(rawstr.splitlines()):
            for col, char in enumerate(line):
                if char in ('>', '<', '^', 'v'):
                    self.__carts.add(Cart(Point(row, col), char))
                    self.__tracks[Point(row, col)] = '-' if char in ('<', '>') else '|'
                elif char != " ":
                    self.__tracks[Point(row, col)] = char

    def get_first_crash_location(self) -> str:
        carts = list(sorted(deepcopy(self.__carts)))
        while True:
            taken: list[Point] = [c.get_pos() for c in carts]
            for i, cart in enumerate(carts):
                newpos = cart.move()
                if newpos in taken:
                    return f"{newpos.col},{newpos.row}"
                else:
                    taken[i] = newpos
                cart.update_rotation(self.__tracks[newpos])
            carts.sort()

    def get_last_cart_location(self) -> str:
        carts = list(sorted(deepcopy(self.__carts)))
        while len(carts) > 1:
            taken: list[Point] = [c.get_pos() for c in carts]
            deadcarts = set()
            for i, cart in enumerate(carts):
                if i in deadcarts:
                    continue
                newpos = cart.move()
                if newpos in taken:
                    deadcarts.add(i)
                    deadcarts.add(taken.index(newpos))
                else:
                    taken[i] = newpos
                    cart.update_rotation(self.__tracks[newpos])
            carts = sorted([cart for i, cart in enumerate(carts) if i not in deadcarts])
        p = carts[0].get_pos()
        return f"{p.col},{p.row}"


def main(aoc_input: str) -> None:
    tracks = TrackSystem(aoc_input)
    print(f"Part 1: {tracks.get_first_crash_location()}")
    print(f"Part 2: {tracks.get_last_cart_location()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day13.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
