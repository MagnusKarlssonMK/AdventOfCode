import time
from pathlib import Path
from itertools import combinations

class Grid:
    def __init__(self, rawstr: str) -> None:
        lines = rawstr.splitlines()
        self.x_max = len(lines[0])
        self.y_max = len(lines)
        self.__elements = [c for c in rawstr if c != "\n"]

    def get_element(self, x: int, y: int) -> str:
        return self.__elements[self.x_max * y + x]

    def is_contained(self, x: int, y: int) -> bool:
        return 0 <= x < self.x_max and 0 <= y < self.y_max

    def find(self, val: str) -> iter:
        for i, v in enumerate(self.__elements):
            if v == val:
                yield i % self.x_max, i // self.y_max


class Garden:
    def __init__(self, rawstr: str) -> None:
        self.__map = Grid(rawstr)

    def get_costs(self) -> tuple[int, int]:
        total_perimeter = total_sides = 0
        counted: set[tuple[int, int]] = set()
        for y in range(0, self.__map.y_max):
            for x in range(0, self.__map.x_max):
                if (x, y) not in counted:
                    area = perimeter = sides = 0
                    group: set[tuple[int, int]] = set()
                    queue: list[tuple[int, int]] = [(x, y)]
                    neighborstates = []
                    while queue:
                        current_x, current_y = queue.pop(0)
                        if (current_x, current_y) in counted:
                            continue
                        counted.add((current_x, current_y))
                        group.add((current_x, current_y))
                        area += 1
                        element = self.__map.get_element(current_x, current_y)
                        for dir_x, dir_y in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                            neighbor_x, neighbor_y = current_x + dir_x, current_y + dir_y
                            if (self.__map.is_contained(neighbor_x, neighbor_y)):
                                if (neighbor_val := self.__map.get_element(neighbor_x, neighbor_y)) == element:
                                    queue.append((neighbor_x, neighbor_y))
                                    neighborstates.append((dir_x, dir_y, 1))
                                else:
                                    perimeter += 1
                                    neighborstates.append((dir_x, dir_y, 0))
                            else:
                                perimeter += 1
                                neighborstates.append((dir_x, dir_y, 0))
                        # Check the combinations of straight neighbors to evaluate corners
                        for (n1_x, n1_y, v1), (n2_x, n2_y, v2) in combinations(neighborstates, 2):
                            if (n1_x == 0 and n2_x == 0) or (n1_y == 0 and n2_y == 0):
                                continue
                            if ((v1 == 0 and v2 == 0) or
                                (v1 == 1 and v2 == 1 and
                                 self.__map.get_element(current_x + n1_x + n2_x, current_y + n1_y + n2_y) != element)):
                                sides += 1
                        neighborstates.clear()
                    total_perimeter += area * perimeter
                    total_sides += area * sides

        return total_perimeter, total_sides


def main(aoc_input: str) -> None:
    garden = Garden(aoc_input)
    p1, p2 = garden.get_costs()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/day12.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
