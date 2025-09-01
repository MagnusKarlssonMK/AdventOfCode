"""
Part 1: Run the intcode program to generate the map, then store the scaffold tiles as an adjacency list. The answer
can then be determined by finding the tiles that have more than 2 neighbors.

Part 2: An attempt to make a generic solution, rather than manually creating the functions and program by visually
inspecting the map. It assumes that the functions always starts with a direction command, and that we always need all
three programs. Needs to be tested with more inputs to see if it holds up.
Also, some room for improvement in the juggling between string and list formats of the scaffold / function
representations, particularly in the functon for generating the A/B/C-functions.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from intcode import Intcode, IntResult
import re
from collections.abc import Generator


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_neighbors(self) -> Generator["Point"]:
        for n in (Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)):
            yield self + n

    def get_alignment(self) -> int:
        return self.x * self.y

    def turn_left(self) -> "Point":
        return Point(self.y, -self.x)

    def turn_right(self) -> "Point":
        return Point(-self.y, self.x)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


@dataclass(frozen=True)
class Route:
    steps: list[tuple[str, int]]

    def create_function(self, length: int) -> tuple[str, "Route"]:
        newfunction = Route(list(self.steps[0: length])).get_string()
        return newfunction, Route(list(self.steps[length:]))

    def split(self, fn: str) -> list["Route"]:
        fragments = self.get_string().split(fn)
        return [Route.get_from_str(f) for f in fragments if f]

    def get_string(self) -> str:
        return ''.join([d + str(v) for d, v in self.steps])

    def create_program(self, fn_a: str, fn_b: str, fn_c: str) -> str:
        fn_a = ''.join([c for c in fn_a if c != ','])
        fn_b = ''.join([c for c in fn_b if c != ','])
        fn_c = ''.join([c for c in fn_c if c != ','])
        fn_map = {fn_a: 'A', fn_b: 'B', fn_c: 'C'}
        result = ''
        total_steps = self.get_string()
        i = 1
        while total_steps and i <= len(total_steps):
            if total_steps[:i] in fn_map:
                result += fn_map[total_steps[:i]]
                result += ','
                total_steps = total_steps[i:]
                i = 1
            else:
                i += 1
        return result.strip(',')

    @staticmethod
    def get_from_str(step_string: str) -> "Route":
        result = re.findall(r"([L, R])(\d+)", step_string)
        return Route([(d, int(v)) for d, v in result])


class Scaffold:
    __MAX_PROG_LEN = 20

    def __init__(self, rawstr: str) -> None:
        self.__cpu = Intcode(list(map(int, rawstr.split(','))))
        self.__map: dict[Point, set[Point]] = {}
        self.__vacuum_pos = Point(-1, -1)
        self.__vacuum_dir = Point(-1, -1)
        self.__route: Route = Route([])

    def __build_map(self) -> None:
        vacuum_dirs = {'^': Point(0, -1), '>': Point(1, 0), 'v': Point(0, 1), '<': Point(-1, 0)}
        x = y = 0
        # Generate the map tiles using the intcode
        while True:
            val, res = self.__cpu.run_program()
            if res == IntResult.WAIT_INPUT:
                break
            elif res == IntResult.OUTPUT:
                tile = chr(val)
                if tile == "#":
                    self.__map[Point(x, y)] = set()
                    x += 1
                elif tile in vacuum_dirs:
                    self.__map[Point(x, y)] = set()
                    self.__vacuum_pos = Point(x, y)
                    self.__vacuum_dir = vacuum_dirs[tile]
                    x += 1
                elif tile == "\n":
                    y += 1
                    x = 0
                else:
                    x += 1
            else:
                break
        self.__cpu.reboot()

        # Fill in the neighbors in the map
        for p in self.__map:
            for n in p.get_neighbors():
                if n in self.__map:
                    self.__map[p].add(n)

    def __build_route(self) -> None:
        vpos: Point = self.__vacuum_pos
        vdir: Point = self.__vacuum_dir
        result: list[str] = []
        done = False
        while not done:
            if vpos + vdir in self.__map[vpos]:
                vpos += vdir
                if result and result[-1] not in ('L', 'R'):
                    result[-1] = str(1 + int(result[-1]))
                else:
                    result.append('1')
            elif vpos + vdir.turn_left() in self.__map[vpos]:
                vdir = vdir.turn_left()
                result.append('L')
            elif vpos + vdir.turn_right() in self.__map[vpos]:
                vdir = vdir.turn_right()
                result.append('R')
            else:
                done = True
        self.__route = Route([(result[i], int(result[i + 1])) for i in range(0, len(result), 2)])

    def get_alignment_sum(self) -> int:
        self.__build_map()
        return sum([p.get_alignment() for p in self.__map if len(self.__map[p]) > 2])

    def __build_functions(self) -> tuple[str, str, str]:
        # Note: the step representation is itself 2 characters plus one comma, and multiple steps also need to be comma
        # separated. So 20 characters means max 5 steps ()
        max_steps = Scaffold.__MAX_PROG_LEN // 4
        for a_len in range(1, min(max_steps + 1, len(self.__route.steps))):
            fn_a, a_remainder = self.__route.create_function(a_len)
            a_fragments = a_remainder.split(fn_a)
            # Note: Theoretically, fragments can be empty if we can solve it entirely with a single program
            # Assume that we always need all three programs
            a_fragments.sort(key=lambda x: len(x.steps))
            for b_len in range(1, len(a_fragments[0].steps) + 1):
                fn_b, _ = a_fragments[0].create_function(b_len)
                if b_len > max_steps:
                    continue

                b_remainder_set: set[str] = set()
                for f in a_fragments:
                    b_remainder_set.update(set([c.get_string() for c in f.split(fn_b)]))
                b_remainder: list[str] = sorted(list(b_remainder_set), key=lambda x: len(x))
                # Reduce the remainder with the shortest (first) entry and see if anything remains
                c_remainder: list[str] = []
                for r in b_remainder:
                    rest = r.split(b_remainder[0])
                    for part in rest:
                        if len(part) > 0:
                            c_remainder.append(part)

                if not c_remainder:
                    fn_c = b_remainder.pop(0)
                    if len(Route.get_from_str(fn_c).steps) > max_steps:
                        continue
                    fn_a = ''.join([c + ',' for c in re.split(r"(\d+)", fn_a)]).strip(',')
                    fn_b = ''.join([c + ',' for c in re.split(r"(\d+)", fn_b)]).strip(',')
                    fn_c = ''.join([c + ',' for c in re.split(r"(\d+)", fn_c)]).strip(',')
                    return fn_a, fn_b, fn_c
        return '', '', ''

    def get_dust_collected(self) -> int:
        self.__build_route()
        functions = self.__build_functions()
        prog = self.__route.create_program(*functions)
        self.__cpu.override_program(0, 2)
        for c in prog:
            self.__cpu.add_input(ord(c))
        self.__cpu.add_input(10)
        for fn in functions:
            for c in fn:
                self.__cpu.add_input(ord(c))
            self.__cpu.add_input(10)
        self.__cpu.add_input(ord('n'))
        self.__cpu.add_input(10)
        outputbuffer: list[int] = []
        while True:
            val, res = self.__cpu.run_program()
            if res == IntResult.WAIT_INPUT:
                break
            elif res == IntResult.OUTPUT:
                outputbuffer.append(val)
            else:
                break
        return outputbuffer[-1]


def main(aoc_input: str) -> None:
    scaffold = Scaffold(aoc_input)
    print(f"Part 1: {scaffold.get_alignment_sum()}")
    print(f"Part 2: {scaffold.get_dust_collected()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day17.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
